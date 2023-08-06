import ast
import os
import re
from abc import abstractmethod
from collections import Counter
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field, replace as dc_replace
from typing import List, Optional

from ovld import ovld

from .parse import Variables, variables
from .utils import ConformException, EventSource, IDSet, conform, dig, locate

current_info = ContextVar("current_info", default=None)


splitlines = ast._splitlines_no_ff
sep_at_start = re.compile(r"^ *[\n;]")
sep_at_end = re.compile(r"[\n;] *$")


class StaleException(Exception):
    pass


class attrproxy:
    def __init__(self, cls):
        self.cls = cls

    def __getitem__(self, item):
        try:
            return getattr(self.cls, item)
        except AttributeError:
            raise KeyError(item)

    def __setitem__(self, item, value):
        return setattr(self.cls, item, value)

    def get(self, item, dflt):
        return getattr(self.cls, item, dflt)


@dataclass
class Info:
    filename: str
    module_name: str
    source: str
    lines: list
    varinfo: Variables = None

    replace = dc_replace

    def get_segment(self, ext):
        lineno = ext.lineno - 1
        col_offset = ext.col_offset
        end_lineno = ext.end_lineno - 1
        end_col_offset = ext.end_col_offset

        lines = self.lines
        if end_lineno == lineno:
            return lines[lineno].encode()[col_offset:end_col_offset].decode()

        first = lines[lineno].encode()[col_offset:].decode()
        last = lines[end_lineno].encode()[:end_col_offset].decode()
        lines = lines[lineno + 1 : end_lineno]

        lines.insert(0, first)
        lines.append(last)
        return "".join(lines)


@contextmanager
def use_info(**fields):
    info = Info(**fields)
    token = current_info.set(info)
    try:
        yield
    finally:
        current_info.reset(token)


def get_info():
    return current_info.get()


@dataclass
class Correspondence:
    original: "Code"
    new: "Code"
    corresponds: bool
    changed: bool = False
    child_correspondences: Optional[List["Correspondence"]] = None

    @staticmethod
    def invalid(original, new):
        return Correspondence(
            original=original,
            new=new,
            corresponds=False,
            changed=False,
            child_correspondences=None,
        )

    @staticmethod
    def valid(original, new, **kwargs):
        return Correspondence(
            original=original,
            new=new,
            corresponds=True,
            **kwargs,
        )

    def fitness(self):
        return (
            int(self.corresponds),
            1 - int(self.changed),
        )

    def walk(self):
        yield self
        for child in self.child_correspondences or []:
            yield from child.walk()

    def summary(self, filter=None):
        (same, changes, additions, deletions) = ([], [], [], [])
        for corr in self.walk():
            if filter is None or filter(corr.original or corr.new):
                if corr.original is None:
                    additions.append(corr.new)
                elif corr.new is None:
                    deletions.append(corr.original)
                elif corr.changed:
                    changes.append(corr.original)
                else:
                    same.append(corr.original)
        return (same, changes, additions, deletions)


@dataclass
class Code:
    node: ast.AST
    name: str = None
    filename: str = None
    parent: Optional["Code"] = None
    objects: IDSet = field(default_factory=IDSet)

    def __post_init__(self):
        self._code = None
        if self.filename is None:
            self.filename = get_info().filename

    #############
    # Hierarchy #
    #############

    def set_parent(self, parent):
        self.parent = parent
        for p in self.hierarchy(skip=1):
            p._code = None

    def hierarchy(self, skip=0):
        if skip <= 0:
            yield self
        if self.parent is not None:
            yield from self.parent.hierarchy(skip - 1)

    def dotpath(self):
        chain = list(self.hierarchy())
        return ".".join(x.name or "<line>" for x in reversed(chain))

    def module_name(self):
        return self.parent and self.parent.module_name()

    def get_globals(self):
        return self.parent and self.parent.get_globals()

    ##############
    # Management #
    ##############

    @property
    def codestring(self):
        if self._code is None:
            self._code = self.reconstruct()
        return self._code

    @property
    def is_whitespace(self):
        return False

    @abstractmethod
    def reconstruct(self):
        pass

    @abstractmethod
    def stash(self, lineno=1, col_offset=0):
        pass

    @abstractmethod
    def prepend_text(self, text):
        pass

    @abstractmethod
    def append_text(self, text):
        pass

    ##################
    # Correspondence #
    ##################

    @abstractmethod
    def correspond(self, other):
        pass

    @abstractmethod
    def apply_correspondence(self, corr, order, controller):
        pass

    ###############
    # Cataloguing #
    ###############

    def catalogue(self, cat=None):
        cat = {} if cat is None else cat
        if self.node is not None:
            ext = self.node.extent
            if ext is not None:
                cat[(ext.filename, ext.lineno)] = self
        return cat

    ##############
    # Evaluation #
    ##############

    def evaluate(self, glb, lcl):
        if self.node is not None:
            node = ast.Module(body=[self.node], type_ignores=[])
            code = compile(node, mode="exec", filename=self.filename)
            exec(code, glb, lcl)

    #############
    # Utilities #
    #############

    def well_separated(self, other):
        a = self.codestring
        b = other.codestring
        return sep_at_end.search(a) or sep_at_start.search(b)


@dataclass
class CodeChunk(Code):
    text: str = ""

    ##############
    # Management #
    ##############

    def reconstruct(self):
        return self.text

    def stash(self, lineno=1, col_offset=0):
        lines = self.text.split("\n")
        last = len(lines[-1])
        self.stashed = Extent(
            lineno=lineno,
            col_offset=col_offset,
            end_lineno=lineno + len(lines) - 1,
            end_col_offset=col_offset + last if len(lines) == 1 else last,
            filename=self.filename,
            content=self.codestring,
        )
        return self.stashed

    def prepend_text(self, text):
        self.text = text + self.text

    def append_text(self, text):
        self.text = self.text + text

    @property
    def is_whitespace(self):
        return not any(substantial(line) for line in self.text.split("\n"))

    ##################
    # Correspondence #
    ##################

    def equiv_src(self, other):
        return self.text == other.text

    def correspond(self, other):
        if type(other) is not type(self) or not self.equiv_src(other):
            return Correspondence.invalid(self, other)
        else:
            return Correspondence.valid(self, other, changed=False)


@dataclass
class CodeHeader(CodeChunk):

    ##################
    # Correspondence #
    ##################

    def equiv_src(self, other):
        return self.text.strip() == other.text.strip()


@dataclass
class GroupedCode(Code):
    variables: Variables = None
    children: List[Code] = field(default=list)

    def __post_init__(self):
        super().__post_init__()
        self.ignore_names = False
        children, self.children = self.children, []
        for child in children:
            self.append(child)

    #############
    # Hierarchy #
    #############

    def set_parent(self, parent):
        super().set_parent(parent)
        if self.variables is not None:
            closable = set()
            for p in self.hierarchy(skip=1):
                if p.variables:
                    closable |= p.variables.assigned
            self.variables.closure = self.variables.free & closable

    def header(self):
        return "".join(
            [
                child.codestring
                for child in self.children
                if isinstance(child, CodeHeader)
            ]
        )

    ##############
    # Management #
    ##############

    def reconstruct(self):
        return "".join([child.codestring for child in self.children])

    def stash(self, lineno=1, col_offset=0):
        self.stashed = Extent(
            lineno=lineno,
            col_offset=col_offset,
            end_lineno=lineno,
            end_col_offset=col_offset,
            filename=self.filename,
            content=self.codestring,
        )
        curr = self.stashed
        for child in self.children:
            curr = child.stash(curr.end_lineno, curr.end_col_offset)
        self.stashed.end_lineno = curr.end_lineno
        self.stashed.end_col_offset = curr.end_col_offset
        return self.stashed

    def prepend_text(self, text):
        if self.children:
            self.children[0].prepend_text(text)
        else:  # pragma: no cover
            # This doesn't seem to ever happen
            self.prepend(
                CodeChunk(node=None, text=text, filename=self.filename)
            )

    def append_text(self, text):  # pragma: no cover
        # This doesn't seem to ever be called
        if self.children:
            self.children[-1].append_text(text)
        else:
            self.append(CodeChunk(node=None, text=text, filename=self.filename))

    def append(self, *children, ensure_separation=False):
        for child in children:
            if (
                ensure_separation
                and self.children
                and not self.children[-1].well_separated(child)
            ):
                ws = CodeChunk(node=None, text="\n", filename=self.filename)
                self.children.append(ws)
                ws.set_parent(self)
            self.children.append(child)
            child.set_parent(self)

    def prepend(self, *children):
        self.children[0:0] = children
        for child in children:
            child.set_parent(self)

    ##################
    # Correspondence #
    ##################

    def correspond(self, other):
        if type(other) is not type(self) or (
            not self.ignore_names and self.name != other.name
        ):
            return Correspondence.invalid(self, other)
        elif self.codestring == other.codestring:
            return Correspondence.valid(self, other, changed=False)
        else:
            childcorr = []
            children = list(self.children)

            for other_child in other.children:
                candidates = [
                    corr
                    for this_child in children
                    if (corr := this_child.correspond(other_child)).corresponds
                ]

                if not candidates:
                    corr = Correspondence.valid(None, other_child, changed=True)
                else:
                    corr = max(candidates, key=lambda corr: corr.fitness())
                    children.remove(corr.original)

                childcorr.append(corr)

            for child in children:
                corr = Correspondence.valid(child, None, changed=True)
                childcorr.append(corr)

            mergeable = not any(
                (
                    isinstance(corr.original, CodeHeader)
                    or isinstance(corr.new, CodeHeader)
                )
                and corr.changed
                for corr in childcorr
            )

            if mergeable:
                return Correspondence.valid(
                    original=self,
                    new=other,
                    changed=True,
                    child_correspondences=childcorr,
                )
            else:
                return Correspondence.invalid(self, other)

    def _process_child_correspondence(self, ccorr, order, controller):
        orig = ccorr.original
        new = ccorr.new

        try:
            if orig is None:
                if controller("pre-add", ccorr):
                    # Addition
                    self.append(new, ensure_separation=True)
                    self.evaluate_child(new)
                    controller("post-add", ccorr)
            elif new is None:
                if controller("pre-delete", ccorr):
                    # Deletion
                    for obj in orig.objects:
                        conform(obj, None)
                    controller("post-delete", ccorr)
                else:
                    self.append(orig, ensure_separation=True)
            elif ccorr.changed:
                # Change
                self.append(orig, ensure_separation=True)
                try:
                    orig.apply_correspondence(
                        ccorr,
                        order=order,
                        controller=controller,
                    )
                except ConformException:
                    self.children.pop()
                    self._process_child_correspondence(
                        Correspondence.valid(None, new),
                        order=order,
                        controller=controller,
                    )
            else:
                self.append(orig, ensure_separation=True)
        except Exception as exc:
            controller("error", ccorr, exc=exc)

    def _apply_corrlist(self, corrs, order, controller):
        def namecounts():
            c = Counter()
            for child in self.children:
                if (name := getattr(child, "name", None)) is not None:
                    c[name] += 1
            return c

        counts1 = namecounts()
        self.children = []

        for corr in corrs:
            self._process_child_correspondence(corr, order, controller)

        counts2 = namecounts()
        for dlt in set(counts1) - set(counts2):
            self.delete_property(dlt)

    def _apply_correspondence_orig_order(self, corr, controller):
        groups = {id(None): []}
        curr = None
        for ccorr in corr.child_correspondences:
            if ccorr.original is not None:
                if ccorr.original.node is not None:
                    if curr is None:
                        init = groups[id(None)]
                        del groups[id(None)]
                    else:
                        init = []
                    curr = ccorr.original
                    groups[id(curr)] = init
                    groups[id(curr)].append(ccorr)
                else:
                    groups[id(ccorr.original)] = [ccorr]
            else:
                groups[id(curr)].append(ccorr)

        ccorrs = []
        for child in self.children:
            ccorrs += groups.get(id(child), [])
        ccorrs += groups.get(id(None), [])
        self._apply_corrlist(
            ccorrs,
            order="original",
            controller=controller,
        )

    def _apply_correspondence_new_order(self, corr, controller):
        self._apply_corrlist(
            corr.child_correspondences, order="new", controller=controller
        )

    def apply_correspondence(self, corr, order, controller):
        assert corr.corresponds

        if not corr.changed:
            return

        if controller("pre-update", corr):
            assert order in ("original", "new")

            if order == "original":
                self._apply_correspondence_orig_order(
                    corr, controller=controller
                )
            elif order == "new":
                self._apply_correspondence_new_order(
                    corr, controller=controller
                )

            controller("post-update", corr)

    ###############
    # Cataloguing #
    ###############

    def catalogue(self, cat=None):
        if cat is None:
            cat = {}
        for child in self.children:
            child.catalogue(cat)
        super().catalogue(cat)
        if (pth := self.dotpath()) is not None:
            cat[pth] = self
        return cat

    ##############
    # Evaluation #
    ##############

    def associate(self, obj, module_name):
        cat = self.catalogue()
        for entry in dig(obj, module_name):
            defn = locate(entry, cat)
            if defn is not None:
                defn.objects.add(entry)

    def evaluate(self, glb, lcl):
        super().evaluate(glb, lcl)
        obj = (lcl or glb).get(self.name, None)
        obj.__qualname__ = ".".join(self.dotpath().split(".")[1:])
        mname = self.module_name()
        self.associate(obj, mname)

    @abstractmethod
    def evaluate_child(self, child):
        pass

    @abstractmethod
    def delete_property(self, prop):
        pass


@dataclass
class ModuleCode(GroupedCode):
    def __post_init__(self):
        super().__post_init__()
        self.ignore_names = True

    #############
    # Hierarchy #
    #############

    def module_name(self):
        return self.name

    def set_globals(self, glb):
        self.objects = [glb]

    def get_globals(self):
        (mod,) = self.objects
        if not isinstance(mod, dict):
            mod = vars(mod)
        return mod

    ##############
    # Evaluation #
    ##############

    def evaluate_child(self, child):
        return child.evaluate(self.get_globals(), None)

    def delete_property(self, prop):
        (mod,) = self.objects
        delattr(mod, prop)


@dataclass
class ClassCode(GroupedCode):

    ##############
    # Evaluation #
    ##############

    def evaluate_child(self, child):
        for obj in self.objects:
            return child.evaluate(self.get_globals(), attrproxy(obj))

    def delete_property(self, prop):
        for obj in self.objects:
            delattr(obj, prop)


@dataclass
class FunctionCode(GroupedCode):

    ##################
    # Correspondence #
    ##################

    def apply_correspondence(self, corr, order, controller):
        assert corr.corresponds and corr.changed

        glb = self.get_globals()
        for ccorr in corr.walk():
            if (
                isinstance(ccorr.original, FunctionCode)
                and ccorr.new is not None
                and ccorr.changed
                and controller("pre-update", ccorr)
            ):
                try:
                    ccorr.original.reevaluate(ccorr.new.node, glb, None)
                    controller("post-update", ccorr)
                except ConformException:
                    # Only re-raise for the top level FunctionCode so that
                    # its parent tries to run it anew
                    if ccorr is corr:
                        raise

        self.children = []
        self.append(*corr.new.children)

    ##############
    # Evaluation #
    ##############

    def reevaluate(self, new_node, glb, lcl):
        if not self.objects:  # pragma: no cover
            return

        ext = new_node.extent
        closure = False
        lcl = {}
        new_node = type(new_node)(
            name=new_node.name,
            args=new_node.args,
            body=new_node.body,
            decorator_list=[],
            returns=new_node.returns,
            type_comment=new_node.type_comment,
            lineno=new_node.lineno,
            col_offset=new_node.col_offset,
            end_lineno=new_node.end_lineno,
            end_col_offset=new_node.end_col_offset,
        )
        previous = lcl.get(self.name, None)
        if self.variables.closure:
            closure = True
            names = tuple(sorted(self.variables.closure))
            wrap = ast.copy_location(
                ast.FunctionDef(
                    name="##create_closure",
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[
                            ast.arg(
                                arg=name, lineno=new_node.lineno, col_offset=0
                            )
                            for name in names
                        ],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[],
                    ),
                    body=[
                        new_node,
                        ast.Return(ast.Name(id=new_node.name, ctx=ast.Load())),
                    ],
                    decorator_list=[],
                    returns=None,
                ),
                new_node,
            )
            ast.fix_missing_locations(wrap)
            node = ast.Module(body=[wrap], type_ignores=[])
        else:
            node = ast.Module(body=[new_node], type_ignores=[])
        code = compile(node, mode="exec", filename=ext.filename)
        exec(code, glb, lcl)
        if closure:
            creator = lcl["##create_closure"]
            # It does not matter what arguments we provide here, because we will move the
            # function's __code__ elsewhere, so it will use a different closure
            new_obj = creator(*names)
        else:
            new_obj = lcl[self.name]
        lcl[self.name] = previous
        for obj in self.objects:
            conform(obj, new_obj)
        node.extent = ext
        self.node = node


@dataclass
class Extent:
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    filename: str = None
    content: str = None

    def __post_init__(self):
        if self.filename is None:
            self.filename = get_info().filename


def _collapse_to_beginning(ext):
    return Extent(
        lineno=ext.lineno,
        col_offset=ext.col_offset,
        end_lineno=ext.lineno,
        end_col_offset=ext.col_offset,
    )


def _collapse_to_end(ext):
    return Extent(
        lineno=ext.end_lineno,
        col_offset=ext.end_col_offset,
        end_lineno=ext.end_lineno,
        end_col_offset=ext.end_col_offset,
    )


def extend_to_line(node):
    return Extent(
        lineno=node.lineno,
        col_offset=0,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )


def fill_real_extent(node):
    extents = [
        ext for n in ast.iter_child_nodes(node) if (ext := fill_real_extent(n))
    ]
    if hasattr(node, "decorator_list"):
        for deco in node.decorator_list:
            extents.append(extend_to_line(deco))

    if hasattr(node, "lineno"):
        extents.append(node)

        lineno, col_offset = min(
            (ext.lineno, ext.col_offset) for ext in extents
        )
        end_lineno, end_col_offset = max(
            (ext.end_lineno, ext.end_col_offset) for ext in extents
        )
        node.extent = Extent(
            lineno=lineno,
            col_offset=col_offset,
            end_lineno=end_lineno,
            end_col_offset=end_col_offset,
        )
    else:
        node.extent = None
    return node.extent


def substantial(s):
    return not re.fullmatch(r" *(#.*)?\n?", s)


def analyze_split(s):
    lines = splitlines(s)
    subst = max(
        [i for i, line in enumerate(lines) if substantial(line)], default=-1
    )
    left = lines[: subst + 1]
    middle = lines[subst + 1 :]
    if middle and not middle[-1].endswith("\n"):
        right = [middle.pop()]
    else:
        right = []
    return "".join(left), "".join(middle), "".join(right)


def delta(node1, node2):
    return get_info().get_segment(
        Extent(
            lineno=node1.end_lineno,
            col_offset=node1.end_col_offset,
            end_lineno=node2.lineno,
            end_col_offset=node2.col_offset,
        )
    )


def distribute(between, defn1, defn2, cls=CodeChunk):
    left, middle, right = analyze_split(between)
    rval = ""
    if left:
        if defn1:
            defn1.append_text(left)
        else:
            rval += left
    if middle:
        rval += middle
    if right:
        if defn2:
            defn2.prepend_text(right)
        else:
            rval += right
    return [cls(node=None, text=rval)] if rval else []


@ovld
def collect_definitions(self, nodes: list):
    if not nodes:
        return []
    defns = [(node.extent, self(node)) for node in nodes]
    results = []
    for (node1, defn1), (node2, defn2) in zip(defns[:-1], defns[1:]):
        between = delta(node1, node2)
        results.append(defn1)
        results.extend(distribute(between, defn1, defn2))
    results.append(defns[-1][1])
    return results


@ovld
def collect_definitions(self, node: (ast.FunctionDef, ast.AsyncFunctionDef)):
    info = get_info()
    defns = self(node.body)
    cg = FunctionCode(
        name=node.name,
        node=node,
        children=defns,
        variables=info.varinfo.get(node, Variables()).replace(),
    )

    prelude = []

    deco0 = _collapse_to_beginning(node.extent)
    between = delta(deco0, node)
    prelude += distribute(between, None, None, cls=CodeHeader)

    fnstart = _collapse_to_beginning(node)
    between = delta(fnstart, node.body[0].extent)
    prelude += distribute(between, None, defns[0])

    cg.prepend(*prelude)

    fnend = _collapse_to_end(node)
    between = delta(node.body[-1].extent, fnend)
    cg.append(*distribute(between, defns[-1], None))

    return cg


@ovld
def collect_definitions(self, node: ast.ClassDef):
    info = get_info()
    defns = self(node.body)
    cg = ClassCode(
        name=node.name,
        node=node,
        children=defns,
        variables=info.varinfo.get(node, Variables()).replace(),
    )

    prelude = []

    deco0 = _collapse_to_beginning(node.extent)
    between = delta(deco0, node.body[0].extent)
    prelude += distribute(between, None, defns[0], cls=CodeHeader)

    cg.prepend(*prelude)

    fnend = _collapse_to_end(node)
    between = delta(node.body[-1].extent, fnend)
    cg.append(*distribute(between, defns[-1], None))

    return cg


@ovld
def collect_definitions(self, node: ast.Module):
    info = get_info()
    begin_node = Extent(lineno=1, col_offset=0, end_lineno=1, end_col_offset=0)
    end_node = Extent(
        lineno=len(info.lines),
        col_offset=len(info.lines[-1]),
        end_lineno=len(info.lines),
        end_col_offset=len(info.lines[-1]),
    )

    cg = ModuleCode(node=node, name=info.module_name, children=self(node.body))

    if node.body:
        if between := delta(begin_node, node.body[0].extent):
            cg.prepend(*distribute(between, None, None))

        if between := delta(node.body[-1].extent, end_node):
            cg.append(*distribute(between, None, None))

    return cg


@ovld
def collect_definitions(self, node: ast.stmt):
    return CodeChunk(node=node, text=get_info().get_segment(node))


class CodeFile:
    def __init__(self, filename, module_name, source=None):
        self.activity = EventSource()
        self.filename = filename
        if not self.filename.startswith("<"):
            self.filename = os.path.abspath(self.filename)
        self.module_name = module_name
        self.saved = open(self.filename).read() if source is None else source
        if not self.saved.endswith("\n"):
            self.saved += "\n"
        tree = ast.parse(self.saved)
        varinfo = {}
        variables(tree, varinfo)
        with use_info(
            filename=self.filename,
            module_name=module_name,
            source=self.saved,
            lines=splitlines(self.saved),
            varinfo=varinfo,
        ):
            fill_real_extent(tree)
            self.code = collect_definitions(tree)
        self.code.stash()
        self.dirty = False

    @property
    def module(self):
        (mod,) = self.code.objects
        return mod

    def associate(self, obj):
        self.code.associate(obj, self.module_name)

    def read_source(self):
        source = open(self.filename).read()
        if not source.endswith("\n"):
            source += "\n"
        return source

    def stale(self):
        return self.read_source() != self.saved

    def merge(self, other, order="original", allow_deletions=True):
        if order == "new":
            assert allow_deletions

        def controller(op, ccorr, exc=None):
            if op == "pre-delete":
                return allow_deletions and (
                    allow_deletions is True or ccorr.original in allow_deletions
                )
            elif op == "post-add":
                if not ccorr.new.is_whitespace:
                    self.activity.emit(AddOperation(self, ccorr.new))
            elif op == "post-delete":
                if not ccorr.original.is_whitespace:
                    self.activity.emit(DeleteOperation(self, ccorr.original))
            elif op == "post-update":
                self.activity.emit(UpdateOperation(self, ccorr.original))
            elif op == "error":
                self.activity.emit(exc)
            else:
                return True

        corr = self.code.correspond(other.code)
        if corr.changed:
            self.dirty = True
        self.code.apply_correspondence(corr, order=order, controller=controller)
        return corr.summary()

    def commit(self, check_stale=True):
        if not self.dirty:
            return
        if check_stale and self.stale():
            raise StaleException(
                f"Cannot commit changes to {self.filename} because the file was changed."
            )
        new_source = self.code.reconstruct()
        if not new_source.endswith("\n"):
            new_source += "\n"
        with open(self.filename, "w") as f:
            f.write(new_source)
        self.code.stash()
        self.saved = new_source
        self.dirty = False

    def refresh(self):
        new_source = self.read_source()
        if new_source != self.code.codestring or self.dirty:
            cf = CodeFile(
                self.filename, source=new_source, module_name=self.module_name
            )
            self.merge(cf)
            self.code.stash()


@dataclass
class CodeFileOperation:
    codefile: CodeFile
    code: Code


@dataclass
class UpdateOperation(CodeFileOperation):
    def __str__(self):
        return f"Update {self.code.dotpath()} @L{self.code.stashed.lineno}"


@dataclass
class AddOperation(CodeFileOperation):
    def __str__(self):
        if isinstance(self.code, CodeChunk):
            return f"Run {self.code.parent.dotpath()} @L{self.code.stashed.lineno}: {self.code.text}"
        else:
            return f"Add {self.code.dotpath()} @L{self.code.stashed.lineno}"


@dataclass
class DeleteOperation(CodeFileOperation):
    def __str__(self):
        return f"Delete {self.code.dotpath()} @L{self.code.stashed.lineno}"

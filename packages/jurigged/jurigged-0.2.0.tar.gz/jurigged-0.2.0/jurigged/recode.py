import linecache
import textwrap
from contextlib import contextmanager
from itertools import count
from types import CodeType, FunctionType, ModuleType

from ovld import ovld

from .codetools import (
    CodeChunk,
    CodeFile,
    CodeFileOperation,
    ModuleCode,
    splitlines,
)
from .register import registry
from .utils import EventSource

_count = count(1)


class OutOfSyncException(Exception):
    pass


def virtual_file(name, contents):
    filename = f"<{name}#{next(_count)}>"
    linecache.cache[filename] = (None, None, splitlines(contents), filename)
    return filename


class Recoder:
    def __init__(self, name, codefile, deletable=False, focus=None):
        self.name = name
        self.codefile = codefile
        self.deletable = deletable
        self.focus = focus
        self.watched = [] if focus is None else [focus]
        self.status = "live"
        self.on_status = EventSource()
        self.codefile.activity.register(self._listen)
        self._current_patch = None
        self._listening = True

    def set_status(self, status):
        self.status = status
        self.on_status.emit(self, self.status)

    def _listen(self, event):
        if self._listening:
            if isinstance(event, CodeFileOperation):
                if event.code in self.watched:
                    self.set_status("out-of-sync")

    @contextmanager
    def _patching(self, new_code):
        new_code = new_code.strip()

        filename = virtual_file(self.name, new_code)
        cf = CodeFile(
            filename=filename,
            source=new_code,
            module_name=self.codefile.module_name,
        )
        registry.cache[filename] = self.codefile

        yield cf

        self._listening = False
        (same, changes, additions, deletions) = self.codefile.merge(
            cf, allow_deletions=self.deletable and self.focus and [self.focus]
        )
        self.watched = [*same, *changes, *additions]
        self.set_status("live")
        self._current_patch = new_code
        self._listening = True

    def patch(self, new_code):
        def _encompasses(defn):
            for x in self.focus.hierarchy():
                if x.correspond(defn).corresponds:
                    return True
            for x in defn.hierarchy():
                if x.correspond(self.focus).corresponds:
                    return True
            return False

        if self.focus is None:
            return self.patch_module(new_code)

        for parent in list(self.focus.hierarchy())[1:]:
            if not isinstance(parent, ModuleCode):
                new_code = textwrap.indent(new_code, "    ")
                new_code = f"{parent.header()}{new_code}"

        with self._patching(new_code) as cf:
            (
                same,
                changes,
                additions,
                deletions,
            ) = self.codefile.code.correspond(cf.code).summary()
            seq = [*changes, *additions]
            seq = [d for d in seq if not isinstance(d, CodeChunk)]
            if not all(_encompasses(culprit := d) for d in seq):
                raise ValueError(
                    f"Recoder for {self.focus.name} cannot be used to define {culprit.name}"  # noqa: F821
                )

    def patch_module(self, new_code):
        with self._patching(new_code):
            pass

    def repatch(self):
        if self.status == "out-of-sync" and self._current_patch is not None:
            self.patch_module(self._current_patch)

    def commit(self):
        if self.status == "out-of-sync":
            raise OutOfSyncException(
                f"File {self.codefile.filename} is out of sync with the patch"
            )
        else:
            self.codefile.commit()
            self.set_status("saved")

    def revert(self):
        self.codefile.refresh()


@ovld
def make_recoder(module: ModuleType, deletable=False):
    cf, _ = registry.find(module)
    return cf and Recoder(
        name=module.__name__, codefile=cf, deletable=deletable
    )


@ovld
def make_recoder(obj: (CodeType, FunctionType, type), deletable=False):
    cf, defn = registry.find(obj)
    return (
        cf
        and defn
        and Recoder(
            name=defn.dotpath(), codefile=cf, focus=defn, deletable=deletable
        )
    )

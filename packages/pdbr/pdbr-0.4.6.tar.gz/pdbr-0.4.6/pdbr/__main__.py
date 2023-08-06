import os
import pdb
import sys

from .utils import pdbr_cls, rdbr_cls

os.environ["PYTHONBREAKPOINT"] = "pdbr.set_trace"


def set_trace(*, header=None, context=None):
    pdb_cls = pdbr_cls(context=context)
    if header is not None:
        pdb_cls.message(header)
    pdb_cls.set_trace(sys._getframe().f_back)


def run(statement, globals=None, locals=None):
    pdbr_cls().run(statement, globals, locals)


def post_mortem(t=None):
    t = t or sys.exc_info()[2]
    if t is None:
        raise ValueError(
            "A valid traceback must be passed if no exception is being handled"
        )

    p = pdbr_cls(return_instance=True)
    p.reset()
    p.interaction(None, t)


def pm():
    post_mortem(sys.last_traceback)


def celery_set_trace(frame=None):
    pdb_cls = rdbr_cls()
    if frame is None:
        frame = getattr(sys, "_getframe")().f_back
    return pdb_cls.set_trace(frame)


if __name__ == "__main__":
    pdb.Pdb = pdbr_cls(return_instance=False)
    pdb.main()

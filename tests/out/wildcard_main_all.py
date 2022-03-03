# from testlib_a.sublib_c.sub_ca import *
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.sublib_c = ModuleType("testlib_a.sublib_c")
testlib_a.sublib_c.sub_ca = ModuleType("testlib_a.sublib_c.sub_ca")
testlib_a.sublib_c.sub_cb = ModuleType("testlib_a.sublib_c.sub_cb")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_a_sublib_c_sub_ca = """
__all__ = ("include_def", "include_variable")


def include_def():
    print(__name__)


def exclude_def():
    print(__name__)


_under_score = "under_score"
include_variable = "include_variable"
exclude_variable = "exclude_variable"
"""
exec(_code_testlib_a_sublib_c_sub_ca, testlib_a.sublib_c.sub_ca.__dict__)

_code_testlib_a_sublib_c_sub_cb = """
def func():
    print(__name__)


_under_score = "under_score"
variable = "variable"
"""
exec(_code_testlib_a_sublib_c_sub_cb, testlib_a.sublib_c.sub_cb.__dict__)

_code_testlib_a_sublib_c = """
# from .sub_ca import *
# from .sub_cb import *
"""
if "__all__" in testlib_a.sublib_c.sub_ca.__dict__:
    for _name in testlib_a.sublib_c.sub_ca.__all__:
        testlib_a.sublib_c.__dict__[_name] = testlib_a.sublib_c.sub_ca.__dict__[_name]
else:
    for _name in testlib_a.sublib_c.sub_ca.__dict__:
        if not _name.startswith("_"):
            testlib_a.sublib_c.__dict__[_name] = testlib_a.sublib_c.sub_ca.__dict__[_name]
if "__all__" in testlib_a.sublib_c.sub_cb.__dict__:
    for _name in testlib_a.sublib_c.sub_cb.__all__:
        testlib_a.sublib_c.__dict__[_name] = testlib_a.sublib_c.sub_cb.__dict__[_name]
else:
    for _name in testlib_a.sublib_c.sub_cb.__dict__:
        if not _name.startswith("_"):
            testlib_a.sublib_c.__dict__[_name] = testlib_a.sublib_c.sub_cb.__dict__[_name]
exec(_code_testlib_a_sublib_c, testlib_a.sublib_c.__dict__)

if "__all__" in testlib_a.sublib_c.sub_ca.__dict__:
    for _name in testlib_a.sublib_c.sub_ca.__all__:
        locals()[_name] = testlib_a.sublib_c.sub_ca.__dict__[_name]
else:
    for _name in testlib_a.sublib_c.sub_ca.__dict__:
        if not _name.startswith("_"):
            locals()[_name] = testlib_a.sublib_c.sub_ca.__dict__[_name]

include_def()
print(include_variable)

# import testlib_a.main_d
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.main_d = ModuleType("testlib_a.main_d")
testlib_b = ModuleType("testlib_b")
testlib_b.other = ModuleType("testlib_b.other")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_b = """

"""
exec(_code_testlib_b, testlib_b.__dict__)

_code_testlib_b_other = """
def print_name_testlib_b():
    print(__name__)
"""
exec(_code_testlib_b_other, testlib_b.other.__dict__)

_code_testlib_a_main_d = """
# from testlib_b import other


def print_name_testlib_b_alias():
    other.print_name_testlib_b()
"""
testlib_a.main_d.__dict__["other"] = testlib_b.other
exec(_code_testlib_a_main_d, testlib_a.main_d.__dict__)


testlib_a.main_d.print_name_testlib_b_alias()

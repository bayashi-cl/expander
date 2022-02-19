# from testlib_a.sublib_b import print_name_sublib_sub_ba
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.sublib_b = ModuleType("testlib_a.sublib_b")
testlib_a.sublib_b.sub_ba = ModuleType("testlib_a.sublib_b.sub_ba")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_a_sublib_b_sub_ba = """
def print_name_sublib_sub_ba():
    print(__name__)
"""
exec(_code_testlib_a_sublib_b_sub_ba, testlib_a.sublib_b.sub_ba.__dict__)

_code_testlib_a_sublib_b = """
# from .sub_ba import print_name_sublib_sub_ba
"""
testlib_a.sublib_b.__dict__["print_name_sublib_sub_ba"] = testlib_a.sublib_b.sub_ba.print_name_sublib_sub_ba
exec(_code_testlib_a_sublib_b, testlib_a.sublib_b.__dict__)

print_name_sublib_sub_ba = testlib_a.sublib_b.print_name_sublib_sub_ba

print_name_sublib_sub_ba()

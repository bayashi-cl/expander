# from testlib_a.sublib_d import sub_da
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.sublib_d = ModuleType("testlib_a.sublib_d")
testlib_a.sublib_d.sub_da = ModuleType("testlib_a.sublib_d.sub_da")
testlib_a.sublib_a = ModuleType("testlib_a.sublib_a")
testlib_a.sublib_a.sub_aa = ModuleType("testlib_a.sublib_a.sub_aa")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_a_sublib_d = """

"""
exec(_code_testlib_a_sublib_d, testlib_a.sublib_d.__dict__)

_code_testlib_a_sublib_a = """

"""
exec(_code_testlib_a_sublib_a, testlib_a.sublib_a.__dict__)

_code_testlib_a_sublib_a_sub_aa = """
def print_name_sub_aa():
    print(__name__)
"""
exec(_code_testlib_a_sublib_a_sub_aa, testlib_a.sublib_a.sub_aa.__dict__)

_code_testlib_a_sublib_d_sub_da = """
# import testlib_a.sublib_a.sub_aa


def print_name_sub_aa_alias():
    testlib_a.sublib_a.sub_aa.print_name_sub_aa()
"""
testlib_a.sublib_d.sub_da.__dict__["testlib_a"] = testlib_a
testlib_a.sublib_d.sub_da.__dict__["testlib_a.sublib_a"] = testlib_a.sublib_a
testlib_a.sublib_d.sub_da.__dict__["testlib_a.sublib_a.sub_aa"] = testlib_a.sublib_a.sub_aa
exec(_code_testlib_a_sublib_d_sub_da, testlib_a.sublib_d.sub_da.__dict__)

sub_da = testlib_a.sublib_d.sub_da

sub_da.print_name_sub_aa_alias()

# import testlib_a.sublib_a.sub_ab
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.sublib_a = ModuleType("testlib_a.sublib_a")
testlib_a.sublib_a.sub_ab = ModuleType("testlib_a.sublib_a.sub_ab")
testlib_a.sublib_a.sub_aa = ModuleType("testlib_a.sublib_a.sub_aa")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_a_sublib_a = """

"""
exec(_code_testlib_a_sublib_a, testlib_a.sublib_a.__dict__)

_code_testlib_a_sublib_a_sub_aa = """
def print_name_sub_aa():
    print(__name__)
"""
exec(_code_testlib_a_sublib_a_sub_aa, testlib_a.sublib_a.sub_aa.__dict__)

_code_testlib_a_sublib_a_sub_ab = """
# from . import sub_aa


def print_name_sub_aa_alias():
    sub_aa.print_name_sub_aa()
"""
testlib_a.sublib_a.sub_ab.__dict__["sub_aa"] = testlib_a.sublib_a.sub_aa
exec(_code_testlib_a_sublib_a_sub_ab, testlib_a.sublib_a.sub_ab.__dict__)


testlib_a.sublib_a.sub_ab.print_name_sub_aa_alias()

# import testlib_a.main_c
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.main_c = ModuleType("testlib_a.main_c")
testlib_a.sublib_a = ModuleType("testlib_a.sublib_a")
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

_code_testlib_a_main_c = """
# from .sublib_a.sub_aa import print_name_sub_aa


def print_name_sub_aa_alias():
    print_name_sub_aa()
"""
testlib_a.main_c.__dict__["print_name_sub_aa"] = testlib_a.sublib_a.sub_aa.print_name_sub_aa
exec(_code_testlib_a_main_c, testlib_a.main_c.__dict__)


testlib_a.main_c.print_name_sub_aa_alias()

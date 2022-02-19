# import testlib_a.sublib_a.sub_ac
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.sublib_a = ModuleType("testlib_a.sublib_a")
testlib_a.sublib_a.sub_ac = ModuleType("testlib_a.sublib_a.sub_ac")
testlib_a.main_b = ModuleType("testlib_a.main_b")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_a_sublib_a = """

"""
exec(_code_testlib_a_sublib_a, testlib_a.sublib_a.__dict__)

_code_testlib_a_main_b = """
def print_name_main_b():
    print(__name__)
"""
exec(_code_testlib_a_main_b, testlib_a.main_b.__dict__)

_code_testlib_a_sublib_a_sub_ac = """
# from .. import main_b


def print_name_main_b_alias():
    main_b.print_name_main_b()
"""
testlib_a.sublib_a.sub_ac.__dict__["main_b"] = testlib_a.main_b
exec(_code_testlib_a_sublib_a_sub_ac, testlib_a.sublib_a.sub_ac.__dict__)


testlib_a.sublib_a.sub_ac.print_name_main_b_alias()

# import testlib_a.main_a as ma
from types import ModuleType

testlib_a = ModuleType("testlib_a")
testlib_a.main_a = ModuleType("testlib_a.main_a")

_code_testlib_a = """
__version__ = "1.0.0"
"""
exec(_code_testlib_a, testlib_a.__dict__)

_code_testlib_a_main_a = """
def print_name():
    print(__name__)
"""
exec(_code_testlib_a_main_a, testlib_a.main_a.__dict__)

ma = testlib_a.main_a

ma.print_name()

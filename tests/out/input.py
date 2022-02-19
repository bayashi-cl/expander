# import testlib_b.read_int
from types import ModuleType

testlib_b = ModuleType("testlib_b")
testlib_b.read_int = ModuleType("testlib_b.read_int")

_code_testlib_b = """

"""
exec(_code_testlib_b, testlib_b.__dict__)

_code_testlib_b_read_int = """
def read_int() -> int:
    return int(input())
"""
exec(_code_testlib_b_read_int, testlib_b.read_int.__dict__)


print(testlib_b.read_int.read_int())

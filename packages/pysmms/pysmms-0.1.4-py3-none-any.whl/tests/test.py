import pytest
from pysmms import help


class TestPysmms(object):

    def test_help(self):
        help_info = help._help()
        print(help_info)

    def
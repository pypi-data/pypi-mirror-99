# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2018-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""silx.gui.utils tests"""


__authors__ = ["T. Vincent"]
__license__ = "MIT"
__date__ = "24/04/2018"


import unittest

from . import test_async
from . import test_glutils
from . import test_image
from . import test_qtutils
from . import test_testutils
from . import test


def suite():
    """Test suite for module silx.image.test"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(test.suite())
    test_suite.addTest(test_async.suite())
    test_suite.addTest(test_glutils.suite())
    test_suite.addTest(test_image.suite())
    test_suite.addTest(test_qtutils.suite())
    test_suite.addTest(test_testutils.suite())
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")

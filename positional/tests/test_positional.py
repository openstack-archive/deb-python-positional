#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

import six
import testtools

import positional


class TestPositional(testtools.TestCase):

    @positional.positional(1)
    def no_vars(self):
        # positional doesn't enforce anything here
        return True

    @positional.positional(3, positional.positional.EXCEPT)
    def mixed_except(self, arg, kwarg1=None, kwarg2=None):
        # self, arg, and kwarg1 may be passed positionally
        return (arg, kwarg1, kwarg2)

    @positional.positional(3, positional.positional.WARN)
    def mixed_warn(self, arg, kwarg1=None, kwarg2=None):
        # self, arg, and kwarg1 may be passed positionally, only a warning
        # is emitted
        return (arg, kwarg1, kwarg2)

    def test_nothing(self):
        self.assertTrue(self.no_vars())

    def test_mixed_except(self):
        self.assertEqual((1, 2, 3), self.mixed_except(1, 2, kwarg2=3))
        self.assertEqual((1, 2, 3), self.mixed_except(1, kwarg1=2, kwarg2=3))
        self.assertEqual((1, None, None), self.mixed_except(1))
        self.assertRaises(TypeError, self.mixed_except, 1, 2, 3)

    def test_mixed_warn(self):
        logger_message = six.moves.cStringIO()
        handler = logging.StreamHandler(logger_message)
        handler.setLevel(logging.DEBUG)

        logger = logging.getLogger(positional.__name__)
        level = logger.getEffectiveLevel()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        self.addCleanup(logger.removeHandler, handler)
        self.addCleanup(logger.setLevel, level)

        self.mixed_warn(1, 2, 3)

        self.assertIn('takes at most 3 positional', logger_message.getvalue())

    @positional.positional(enforcement=positional.positional.EXCEPT)
    def inspect_func(self, arg, kwarg=None):
        return (arg, kwarg)

    def test_inspect_positions(self):
        self.assertEqual((1, None), self.inspect_func(1))
        self.assertEqual((1, 2), self.inspect_func(1, kwarg=2))
        self.assertRaises(TypeError, self.inspect_func)
        self.assertRaises(TypeError, self.inspect_func, 1, 2)

    @positional.positional.classmethod(1)
    def class_method(cls, a, b):
        return (cls, a, b)

    @positional.positional.method(1)
    def normal_method(self, a, b):
        self.assertIsInstance(self, TestPositional)
        return (self, a, b)

    def test_class_method(self):
        self.assertEqual((TestPositional, 1, 2), self.class_method(1, b=2))
        self.assertRaises(TypeError, self.class_method, 1, 2)

    def test_normal_method(self):
        self.assertEqual((self, 1, 2), self.normal_method(1, b=2))
        self.assertRaises(TypeError, self.normal_method, 1, 2)

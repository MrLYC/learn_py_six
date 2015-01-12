#!/usr/bin/env python
# encoding: utf-8

from functools import partial
import six
from unittest import TestCase, main


def pyx_only(func, ver):
    @six.wraps(func)
    def check_ver(*args, **kw):
        if not ver:
            return
        return func(*args, **kw)
    return check_ver


py2_only = partial(pyx_only, ver=six.PY2)
py3_only = partial(pyx_only, ver=six.PY3)


class TestConstants(TestCase):
    @py2_only
    def test_types_2(self):
        # (type, classobj)
        self.assertEqual(len(six.class_types), 2)
        self.assertSetEqual(set(six.integer_types), set([long, int]))
        self.assertSetEqual(set(six.string_types), set([basestring]))
        self.assertEqual(six.text_type, unicode)
        self.assertEqual(six.binary_type, str)

    @py3_only
    def test_types_3(self):
        self.assertSetEqual(set(six.class_types), set([type]))
        self.assertSetEqual(set(six.integer_types), set([int]))
        self.assertSetEqual(set(six.string_types), set([str]))
        self.assertEqual(six.text_type, str)
        self.assertEqual(six.binary_type, bytes)


class TestBinStr(TestCase):
    @py2_only
    def test_2(self):
        self.assertTrue(issubclass(str, basestring))
        self.assertTrue(issubclass(unicode, basestring))
        self.assertIsInstance(b"test", six.binary_type)
        self.assertIsInstance("test", six.binary_type)
        self.assertIsInstance(u"test", six.text_type)

        self.assertEqual(six.b("test"), b"test")
        self.assertEqual(six.b("test"), "test")
        self.assertEqual(six.u("test"), u"test")

        # will convert to unicode directly
        self.assertNotEqual(six.u("刘奕聪"), u"刘奕聪")
        self.assertEqual(six.u("刘奕聪"), "刘奕聪".decode("latin-1"))

    @py3_only
    def test_3(self):
        self.assertIsInstance(b"test", six.binary_type)
        self.assertIsInstance("test", six.text_type)
        self.assertEqual(str, unicode)

        self.assertEqual(six.b("test"), b"test")
        self.assertEqual(six.u("test"), "test")
        self.assertEqual(six.u("test"), u"test")

        # no need to use this actually
        self.assertEqual(six.u("刘奕聪"), u"刘奕聪")


if __name__ == "__main__":
    main()

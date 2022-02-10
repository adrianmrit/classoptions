from typing import Any
from unittest import TestCase

from classoptions import ClassOptionsMetaclass


class MetaclassTestCase(TestCase):
    def setUp(self):
        self.metaclass = ClassOptionsMetaclass.factory(
            "Options", "DefaultOptions", "_options"
        )

    def test_simple_inheritance(self):
        class A(metaclass=self.metaclass):
            _options: Any

            class DefaultOptions:
                color = "red"
                size = 2

        class B(A):
            class Options:
                color = "blue"

        class C(B):
            class Options:
                name = "Pencil"

        self.assertEqual(A._options.color, "red")
        self.assertEqual(A._options.size, 2)

        self.assertEqual(B._options.color, "blue")
        self.assertEqual(B._options.size, 2)

        self.assertEqual(C._options.color, "red")
        self.assertEqual(C._options.size, 2)
        self.assertEqual(C._options.name, "Pencil")

    def test_multiple_inheritance(self):
        class A(metaclass=self.metaclass):
            _options: Any

            class DefaultOptions:
                color = "red"
                size = 2
                hello = "world"
                option1 = "o1"
                option2 = "o2"

        class B(A):
            class DefaultOptions:
                color = "blue"
                size = 3

        class C(A):
            class DefaultOptions:
                color = "black"
                hello = "country"
                other = "another"

        class D(B, C):
            class Options:
                option1 = "other"

        self.assertEqual(A._options.color, "red")
        self.assertEqual(A._options.size, 2)
        self.assertEqual(A._options.hello, "world")

        self.assertEqual(B._options.color, "blue")
        self.assertEqual(B._options.size, 3)

        self.assertEqual(C._options.color, "black")
        self.assertEqual(C._options.size, 2)
        self.assertEqual(C._options.hello, "country")
        self.assertEqual(C._options.other, "another")

        # From B
        self.assertEqual(D._options.color, "blue")
        self.assertEqual(D._options.size, 3)

        # From C
        self.assertEqual(D._options.hello, "country")
        self.assertEqual(D._options.other, "another")
        self.assertEqual(D._options.option2, "o2")

        # From D
        self.assertEqual(D._options.option1, "other")

from typing import Any
from unittest import TestCase

from classoptions import ClassOptionsMetaclass


class MetaclassTestCase(TestCase):
    def setUp(self):
        self.metaclass = ClassOptionsMetaclass.factory("Options", "DefaultOptions")

    def test_simple_inheritance(self):
        class A(metaclass=self.metaclass):
            Options: Any

            class DefaultOptions:
                color = "red"
                size = 2

        class B(A):
            class Options:
                color = "blue"

        class C(B):
            class Options:
                name = "Pencil"

        self.assertEqual(A.Options.color, "red")
        self.assertEqual(A.Options.size, 2)

        self.assertEqual(B.Options.color, "blue")
        self.assertEqual(B.Options.size, 2)

        self.assertEqual(C.Options.color, "red")
        self.assertEqual(C.Options.size, 2)
        self.assertEqual(C.Options.name, "Pencil")

    def test_multiple_inheritance(self):
        class A(metaclass=self.metaclass):
            Options: Any

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

        self.assertEqual(A.Options.color, "red")
        self.assertEqual(A.Options.size, 2)
        self.assertEqual(A.Options.hello, "world")

        self.assertEqual(B.Options.color, "blue")
        self.assertEqual(B.Options.size, 3)

        self.assertEqual(C.Options.color, "black")
        self.assertEqual(C.Options.size, 2)
        self.assertEqual(C.Options.hello, "country")
        self.assertEqual(C.Options.other, "another")

        # From B
        self.assertEqual(D.Options.color, "blue")
        self.assertEqual(D.Options.size, 3)

        # From C
        self.assertEqual(D.Options.hello, "country")
        self.assertEqual(D.Options.other, "another")
        self.assertEqual(D.Options.option2, "o2")

        # From D
        self.assertEqual(D.Options.option1, "other")

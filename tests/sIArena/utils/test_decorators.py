import unittest

from sIArena.utils.decorators import override, pure_virtual, unsupported


class TestDecorators(unittest.TestCase):
    def test_unsupported_raises_not_implemented(self):
        @unsupported
        def missing():
            return "never"

        with self.assertRaisesRegex(NotImplementedError, "Function <missing> is not implemented"):
            missing()

    def test_pure_virtual_raises_not_implemented(self):
        @pure_virtual
        def required():
            return "never"

        with self.assertRaisesRegex(NotImplementedError, "must be implemented from a child class"):
            required()

    def test_override_returns_original_result(self):
        @override
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)

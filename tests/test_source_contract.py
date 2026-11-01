"""Host-side source checks for the frozen MicroPython v1.3 firmware.

These tests only validate repository contents; they do not run on the Pico.
"""

import ast
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "device" / "main.py"


def load_assignments():
    root = ast.parse(SOURCE.read_text(encoding="utf-8"))
    values = {}
    for node in root.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(
                node.value, (ast.Dict, ast.Constant)
            ):
                values[target.id] = ast.literal_eval(node.value)
    return values


class FirmwareContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.values = load_assignments()

    def test_firmware_is_syntactically_valid_python(self):
        self.assertIsNotNone(ast.parse(self.source))

    def test_international_alphabet_and_digits(self):
        codes = self.values["MORSE"]
        expected = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.assertEqual(set(codes.values()), set(expected))
        self.assertEqual(len(codes), len(expected))
        self.assertEqual(codes["..."], "S")
        self.assertEqual(codes["---"], "O")
        self.assertEqual(codes[".-"], "A")

    def test_frozen_timing(self):
        self.assertEqual(self.values["DOT_THRESHOLD"], 200)
        self.assertEqual(self.values["LETTER_GAP"], 700)
        self.assertEqual(self.values["WORD_GAP"], 1700)

    def test_hardware_pin_references(self):
        for snippet in (
            "Pin(14, Pin.IN, Pin.PULL_UP)",
            "Pin(16, Pin.IN, Pin.PULL_UP)",
            "Pin(17, Pin.OUT)",
            "PWM(Pin(15), freq=2000)",
            "sda=Pin(0)",
            "scl=Pin(1)",
            "timeout=500000",
            "addr=0x3C",
        ):
            self.assertIn(snippet, self.source)


if __name__ == "__main__":
    unittest.main()

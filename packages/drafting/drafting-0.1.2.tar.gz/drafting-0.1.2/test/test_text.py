import unittest
from drafting.grid import Grid
from drafting.geometry import *
from drafting.text.reader import StyledString, Style

class TestText(unittest.TestCase):
    def test_glyph_name(self):
        style = Style("assets/ColdtypeObviously-VF.ttf")
        ss = StyledString("CDELOPTY", style)
        ssps = ss.pens()
        self.assertEqual(len(ssps), 8)
        self.assertEqual(ssps[0].glyphName, "C")
        self.assertEqual(ssps[-1].glyphName, "Y")

if __name__ == "__main__":
    unittest.main()
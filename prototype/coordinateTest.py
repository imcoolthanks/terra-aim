import unittest
from math import pi
from CoordinateMap import CoordinateMap

class TestCoordinateMap(unittest.TestCase):
    def setUp(self):
        calibration_coordinates = [{"x": 0, "y": 0, "yaw": 0, "pitch": 0}, {"x": 1, "y": 1, "yaw": pi/4, "pitch": pi/4}]
        self.map = CoordinateMap(calibration_coordinates, 1)

    def test_getPos(self):
        x, y = self.map.getPos(0, 0, pi/4, pi/4)
        self.assertAlmostEqual(x, 0.5, places=2)
        self.assertAlmostEqual(y, 0.5, places=2)

if __name__ == '__main__':
    unittest.main()
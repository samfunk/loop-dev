import unittest
import pandas

from utils import make_grid


class MakeGridTestCase(unittest.TestCase):
    """Test converting a user described payload into a grid of values
    """
    def test_happy_case(self):
        payload = {'params': [{'max': 10, 'name': 'x', 'min': 8, 'type': 'int'},
                              {'options': ['foo', 'bar'], 'name': 'y', 'type': 'enum'},
                              {'max': 1, 'name': 'f', 'min': 0, 'type': 'float', 'num_points': 4}]}
        grid = make_grid(payload)
        self.assertTrue(isinstance(grid, pandas.core.frame.DataFrame))
        self.assertEqual(grid.shape, (24, 3))


if __name__ == '__main__':
    unittest.main()

"""nn_search_test"""

import math
import random
import time
import unittest
import tests.mock_data as mock

from pynn import NearestNeighborIndex
from tests.mock_data import BASIC_GRID, BASIC_POINTS

class constructGridIndexTest(unittest.TestCase):
    def test_basic_grid(self):
        uut = NearestNeighborIndex(BASIC_POINTS, 1)

        grid = uut.construct_grid_index(BASIC_POINTS)
        self.assertEqual(grid, BASIC_GRID)

    def test_grid_with_negative_points(self):
        uut = NearestNeighborIndex(mock.NEGATIVE_POINTS, 10)

        grid = uut.construct_grid_index(mock.NEGATIVE_POINTS)
        self.assertEqual(grid, mock.NEGATIVE_GRID) 

    def test_grid_with_floating_points(self):
        uut = NearestNeighborIndex(mock.FLOATING_POINTS, 20)

        grid = uut.construct_grid_index(mock.FLOATING_POINTS)
        self.assertEqual(grid, mock.FLOATING_POINTS_GRID) 

class cellFunctionsTest(unittest.TestCase):
    def test_basic_cell_diimensions(self):
        uut = NearestNeighborIndex(BASIC_POINTS, 1)

        cell_dimensions = uut.get_cell_dimensions()
        self.assertEqual(cell_dimensions, (1,1))

    def test_bigger_cell_dimensions(self):
        uut = NearestNeighborIndex(mock.FLOATING_POINTS, 20)

        cell_dimensions = uut.get_cell_dimensions()
        self.assertEqual(cell_dimensions, (10.0,10.0))

    def test_basic_point_cell(self):
        uut = NearestNeighborIndex(BASIC_POINTS, 1)

        point_assignedd_cell = uut.get_point_cell((1,1))
        self.assertEqual(point_assignedd_cell, (1,1))

    def test_floating_point_cell(self):
        uut = NearestNeighborIndex(mock.FLOATING_POINTS, 20)

        point_assignedd_cell = uut.get_point_cell((55.0,-33.00))
        self.assertEqual(point_assignedd_cell, (5, -4))

class constructBoundingBoxTest(unittest.TestCase):
    def test_basic_bounding_box(self):
        uut = NearestNeighborIndex(mock.BASIC_GRID, 1)

        box = uut.construct_bounding_box(mock.BASIC_GRID)
        self.assertEqual(box, (0,0,1,1))

    def test_floating_points_bounding_box(self):
        uut = NearestNeighborIndex(mock.BASIC_GRID, 1)

        box = uut.construct_bounding_box(mock.FLOATING_POINTS_GRID)
        self.assertEqual(box, (-10,-10,10,10))

class distanceToPointTest(unittest.TestCase):
    def setUp(self):
        self.grid = NearestNeighborIndex(mock.NEGATIVE_POINTS, 10)


    def test_point_inside_cell(self):
        self.assertEqual(self.grid.cell_distance_to_point((-5, -5), (-5, -5)), 0)

    def test_point_on_corner(self):
        self.assertEqual(self.grid.cell_distance_to_point((0, 0), (1, 1)), 0)

    def test_point_on_boundary(self):
        self.assertEqual(self.grid.cell_distance_to_point((0, 0), (0, 1)), 0)

    def test_point_outside_cell(self):
        self.assertAlmostEqual(self.grid.cell_distance_to_point((0, 0), (8, 9)), 10.6301458)

    def test_negative_coordinates(self):
        self.assertEqual(self.grid.cell_distance_to_point((0, 0), (2,2)), math.sqrt(2))

class NearestNeighborIndexTest(unittest.TestCase):
    def test_basic(self):
        """
        test_basic tests a handful of nearest neighbor queries to make sure they return the right
        result.
        """

        test_points = [
            (1, 2),
            (1, 0),
            (10, 5),
            (-1000, 20),
            (3.14159, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighborIndex(test_points)

        self.assertEqual((1, 0), uut.find_nearest((0, 0)))
        self.assertEqual((-1000, 20), uut.find_nearest((-2000, 0)))
        self.assertEqual((42, 3.14159), uut.find_nearest((40, 3)))

    def test_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            uut = NearestNeighborIndex(mock.BASIC_POINTS, -9)
            self.assertEqual(str(context.exception), "grid_size must be a positive integer.")

    def test_benchmark(self):
        """
        test_benchmark tests a bunch of values using the slow and fast version of the index
        to determine the effective speedup.
        """

        def rand_point():
            return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

        index_points = [rand_point() for _ in range(50000)]
        query_points = [rand_point() for _ in range(1)]

        expected = []
        actual = []

        # Run the baseline slow tests to get the expected values.
        start = time.time()
        for query_point in query_points:
            expected.append(NearestNeighborIndex.find_nearest_slow(query_point, index_points))
        slow_time = time.time() - start

        # don't include the indexing time when benchmarking
        uut = NearestNeighborIndex(index_points)

        # Run the indexed tests
        start = time.time()
        for query_point in query_points:
            actual.append(uut.find_nearest(query_point))
        new_time = time.time() - start

        print(f"slow time: {slow_time:0.2f}sec")
        print(f"new time: {new_time:0.2f}sec")
        print(f"speedup: {(slow_time / new_time):0.2f}x")

if __name__ == "__main__":
    unittest.main()

    # TODO: Add more test cases to ensure your index works in different scenarios

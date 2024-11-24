import math
import random
from typing import Dict, List, Optional


class NearestNeighborIndex:
    """
    TODO give me a decent comment

    NearestNeighborIndex is intended to index a set of provided points to provide fast nearest
    neighbor lookup. For now, it is simply a stub that performs an inefficient traversal of all
    points every time.
    """

    def __init__(self, points: List[(tuple)], grid_size: Optional[int]=20):
        """
        Takes an array of 2d tuples as input points to be indexed. Dynamically generates a 
        grid index based off of those points and the given grid_size parameter.
        If grid_size == 0 default to 20.
        """
        if not isinstance(grid_size, int) or grid_size <= 0:
            raise ValueError("grid_size must be a positive integer.")

        self.points = points
        self.grid_size = grid_size
        self.bounding_square = self.get_bounding_box(points)
        self.cell_width, self.cell_height = self.get_cell_dimensions()
        self.grid = self.construct_grid_index(points)


    @staticmethod
    def find_nearest_slow(query_point, haystack):
        """
        find_nearest_slow returns the point that is closest to query_point. If there are no indexed
        points, None is returned.
        """

        min_dist = None
        min_point = None

        for point in haystack:
            deltax = point[0] - query_point[0]
            deltay = point[1] - query_point[1]
            dist = math.sqrt(deltax * deltax + deltay * deltay)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_point = point

        return min_point
    
    def construct_grid_index(self, points: List[tuple]) -> Dict[tuple, List[tuple]]:
        """
        This method creates a spatial index by mapping 2D points to grid cells
        based on their coordinates and the grid's cell dimensions. Each cell is
        represented as a key in a dictionary, and the associated value is a list
        of points that fall within that cell.

        Args:
            points (List[tuple]):A list of tuples, where each tuple represents 
                              a point's (x, y) coordinates.

        Returns:
            (tuple): _description_
        """
        grid = {}

        for point in points:
            cell_coordinates = self.get_point_cell(point)
            if cell_coordinates in grid:
                grid[cell_coordinates].append(point)
            else:
                grid[cell_coordinates] = [point]

        return grid

    def get_cell_dimensions(self) -> tuple:
        """
        Calculates the dimensions of each grid cell.

        Returns:
            (tuple): A tuple containing the width and height of each cell.
        """
        x_min, y_min, x_max, y_max = self.bounding_square
        shift_x = -x_min if x_min < 0 else 0
        shift_y = -y_min if y_min < 0 else 0

        x_min += shift_x
        x_max += shift_x
        y_min += shift_y
        y_max += shift_y

        cell_width = (x_max - x_min) / self.grid_size
        cell_height = (y_max - y_min) / self.grid_size
        return cell_width, cell_height

    def get_point_cell(self, point: List[tuple]) -> tuple:
        """
        Determines the grid cell coordinates for a given point.

        Args:
            point (List[tuple]): _description_

        Returns:
            (tuple): cell coordinates.
        """
        x, y = point

        cell_x = math.floor(x / self.cell_width)
        cell_y = math.floor(y / self.cell_height)

        return (cell_x, cell_y)

    def get_bounding_box(self, points: List[tuple]) -> tuple:
        """
        Constructs a bounding box for a given set of 2D points.

        Args:
            points (List[tuple]): A list of tuples, where each tuple represents a 
                              point's (x, y) coordinates.

        Raises:
            ValueError: If no points are given return a valueError

        Returns:
            (tuple): tuple containing coordinates of the bounfing box
        """
        if not points:
            raise ValueError("The list of points is empty.")

        x_min = min(point[0] for point in points)
        x_min = min(p[0] for p in points)
        x_max = max(p[0] for p in points)
        y_min = min(p[1] for p in points)
        y_max = max(p[1] for p in points)
        return x_min, y_min, x_max, y_max

    def cell_distance_to_point(self, cell_coords: tuple, query_point: tuple) -> int:
        """    
        Calculates the distance from a grid cell to a given query point. 
        If the query point is within or on the bouindaries of the cell, 
        the distance is 0, otherwise the distance is calculated as:
        sqrt{(closest_x_in_cell - query_x)^2 + (closest_y_in_cell} - query_y)^2
        
        Args:
            cell_coords (tuple): _description_
            query_point (tuple): _description_

        Returns:
            (int): distance from a grid cell to a given query point.
        """
        q_x, q_y = query_point
        i, j = cell_coords

        cell_min_x = i * self.cell_width
        cell_max_x = (i + 1) * self.cell_width
        cell_min_y = j * self.cell_height
        cell_max_y = (j + 1) * self.cell_height

        if cell_min_x <= q_x <= cell_max_x and cell_min_y <= q_y <= cell_max_y:
            return 0

        closest_x = max(cell_min_x, min(q_x, cell_max_x))
        closest_y = max(cell_min_y, min(q_y, cell_max_y))

        return math.sqrt((closest_x - q_x) ** 2 + (closest_y - q_y) ** 2)

    def find_nearest(self, query_point: tuple) -> tuple:
        """
        Finds the nearest point in the grid to a given query point.

        This method searches the grid to find the closest point (in Euclidean
        distance) to the specified query point. It iterates over grid cells,
        prioritizing those closest to the query point based on the distance
        from the cell to the query point.
        Args:
            query_point (tuple): A tuple representing the coordinates of the query point 
            in 2D space.

        Returns:
            (tuple):  A tuple representing the coordinates of the nearest neighbor to the 
            query point.
        """
        distance_map = {}
        for cell in self.grid:
            distance = self.cell_distance_to_point(cell, query_point)
            if distance in distance_map:
                distance_map[distance].append(cell)
            else:
                distance_map[distance] = [cell]

        distances = sorted(distance_map.keys())

        result = math.inf
        min_point = None
        for distance in distances:
            if distance > result:
                break
            for cell in distance_map[distance]:
                for point in self.grid[cell]:
                    deltax = point[0] - query_point[0]
                    deltay = point[1] - query_point[1]
                    dist = math.sqrt(deltax * deltax + deltay * deltay)
                    if result == None or dist < result:
                        result = dist
                        min_point = point

        return min_point

# Used for debugging
if __name__ == "__main__":

    def rand_point():
        return (random.randint(-5, 5), random.randint(-5, 5))
    
    actual = []
    index_points = [rand_point() for _ in range(20)]
    query_points = [rand_point() for _ in range(1)]

    uut = NearestNeighborIndex(index_points)

    for query_point in query_points:
        actual.append(uut.find_nearest(query_point))

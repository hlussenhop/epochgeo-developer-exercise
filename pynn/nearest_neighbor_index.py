from collections import defaultdict
import math
import random


class NearestNeighborIndex:
    """
    TODO give me a decent comment

    NearestNeighborIndex is intended to index a set of provided points to provide fast nearest
    neighbor lookup. For now, it is simply a stub that performs an inefficient traversal of all
    points every time.
    """

    def __init__(self, points):
        """
        takes an array of 2d tuples as input points to be indexed.
        """
        self.points = points
        self.grid_size = 20
        self.bounding_square = self.construct_bounding_square(points)
        self.cell_width, self.cell_height = self.get_cell_width()
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
    
    def construct_grid_index(self, points):
        grid = {}

        for point in points:
            cell_coordinates = self.get_point_square(point)
            if cell_coordinates in grid:
                grid[cell_coordinates].append(point)
            else:
                grid[cell_coordinates] = [point]

        return grid

    def get_cell_width(self):
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

    def get_point_square(self, point):
        x, y = point
        
        cell_x = int(x // self.cell_width)
        cell_y = int(y // self.cell_height)
    
        return (cell_x, cell_y)

    def construct_bounding_square(self, points):
        if not points:
            raise ValueError("The list of points is empty.")
        
        x_min = min(point[0] for point in points)
        x_max = max(point[0] for point in points)
        y_min = min(point[1] for point in points)
        y_max = max(point[1] for point in points)

        side_length = max(x_max - x_min, y_max - y_min)

        x_max = x_min + side_length
        y_max = y_min + side_length

        return x_min, y_min, x_max, y_max

    def cell_distance_to_point(self, cell_coords, query_point):
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

    def process_grid_by_distance(self, query_point):
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

    def find_nearest(self, query_point):
        """
        TODO comment me.
        """
        min_point = self.process_grid_by_distance(query_point)
        return min_point

# Used for debugging
if __name__ == "__main__":

    def rand_point():
        return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))
    
    actual = []
    index_points = [rand_point() for _ in range(1000)]
    query_points = [rand_point() for _ in range(1)]

    uut = NearestNeighborIndex(index_points)

    for query_point in query_points:
        actual.append(uut.find_nearest(query_point))

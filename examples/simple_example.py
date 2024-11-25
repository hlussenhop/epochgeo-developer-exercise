# NOTE: run with python -m examples.simple_example
import csv

from pynn import NearestNeighborIndex

# Step 1: Load points from a CSV file
# Assume a file `points.csv` exists with rows like: x,y
points = []
with open('examples/points.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row != ['x', 'y']:
            x, y = map(float, row)  # Convert values to floats
            points.append((x, y))

# Step 2: Create a PyNN graph and add points to it
nearest_neighbors_index = NearestNeighborIndex(points)

# Step 3: Query the graph to find the nearest neighbors
query_points = [(55, 2), (3, 90), (1, 7), (89, 98)]  # Example query point
nearest_neighbors = []
for point in query_points:
    nearest_neighbors.append(nearest_neighbors_index.find_nearest(point))

# Step 4: Print the results
print("Nearest Neighbors:")
for neighbor in nearest_neighbors:
    print(neighbor)

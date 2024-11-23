import math
import threading
from queue import Queue
import random

class BruteForceNNS:
    def __init__(self, data, num_threads=4):

        self.data = data
        self.num_threads = num_threads

    def _euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def _worker(self, query_point, queue, results):
        print("start")
        while not queue.empty():
            try:
                idx = queue.get_nowait()
                distance = self._euclidean_distance(self.data[idx], query_point)
                results.append((distance, idx))
            except Exception:
                break

    def find_nearest(self, query_point):
        queue = Queue()
        results = []

        # Fill the queue with data indices
        for i in range(len(self.data)):
            queue.put(i)

        # Create threads
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._worker, args=(query_point, queue, results))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Find the nearest neighbor from the results
        nearest = min(results, key=lambda x: x[0])
        return nearest


# Example Usage
if __name__ == "__main__":
    # Generate a large random dataset of 2D points (x, y)
    num_points = 10000  # Adjust this value for a larger dataset
    data_points = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(num_points)]

    # Query point
    query = (500, 500)

    # Create an instance of the brute-force NNS
    nns = BruteForceNNS(data_points, num_threads=4)

    # Find the nearest neighbor
    distance, index = nns.find_nearest(query)
    print(f"Nearest neighbor: Index {index}, Distance {distance}")

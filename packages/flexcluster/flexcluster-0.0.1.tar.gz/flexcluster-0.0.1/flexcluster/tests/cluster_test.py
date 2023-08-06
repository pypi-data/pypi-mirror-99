import unittest
import numpy as np
from flexcluster import clustering
from flexcluster import kmeans
from flexcluster import kmedoids

class KmedoidsTestCase(unittest.TestCase):
    def test_clustering(self):
        data = np.array([1, 104, 51, 105, 4, 53, 9, 103, 52])
        initial_centroids = [20, 70, 100]

        centroids, centroid_labels = kmedoids(
            data,
            k=3,
            stop_criteria=0.1,
            initial_centroids=initial_centroids)

        assert {4, 52, 104} == set(centroids)
        assert {0, 4, 6} == set(centroid_labels[0])
        assert {2, 5, 8} == set(centroid_labels[1])
        assert {1, 3, 7} == set(centroid_labels[2])


class KmeansTestCase(unittest.TestCase):
    def test_clustering(self):
        data = np.array([3, 104, 51, 105, 4, 53, 8, 103, 52])
        initial_centroids = [20, 70, 100]

        centroids, centroid_labels = kmeans(
            data,
            k=3,
            stop_criteria=0.1,
            initial_centroids=initial_centroids)

        assert {5, 52, 104} == set(centroids)
        assert {0, 4, 6} == set(centroid_labels[0])
        assert {2, 5, 8} == set(centroid_labels[1])
        assert {1, 3, 7} == set(centroid_labels[2])


class ClusteringTestCase(unittest.TestCase):
    def test_clustering(self):
        data = np.array([2, 104, 51, 105, 4, 53, 3, 103, 52])
        dissimilarity_fn = lambda item1, item2: np.abs(item2 - item1)
        centroid_calc_fn = lambda arr: np.mean(arr)
        initial_centroids = [20, 70, 100]

        centroids, centroid_labels = clustering(
            data,
            k=3,
            dissimilarity_fn=dissimilarity_fn,
            centroid_calc_fn=centroid_calc_fn,
            stop_criteria=0.1,
            initial_centroids=initial_centroids)

        assert {3, 52, 104} == set(centroids)
        assert {0, 4, 6} == set(centroid_labels[0])
        assert {2, 5, 8} == set(centroid_labels[1])
        assert {1, 3, 7} == set(centroid_labels[2])


if __name__ == '__main__':
    unittest.main()

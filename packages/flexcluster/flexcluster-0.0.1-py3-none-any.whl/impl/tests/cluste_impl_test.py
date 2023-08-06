import unittest
import numpy as np
from flexcluster.impl.cluster_impl import _average_centroids_move
from flexcluster.impl.cluster_impl import _calculate_new_centroid
from flexcluster.impl.cluster_impl import _calculate_new_centroids
from flexcluster.impl.cluster_impl import _find_nearest_centroid
from flexcluster.impl.cluster_impl import _choose_initial_centroids
from flexcluster.impl.cluster_impl import _clustering

class ClusteringTestCase(unittest.TestCase):
    def test_clustering(self):
        data = np.array([2, 104, 51, 105, 4, 53, 3, 103, 52])
        dissimilarity_fn = lambda item1, item2: np.abs(item2 - item1)
        centroid_calc_fn = lambda arr: np.mean(arr)
        initial_centroids = [20, 70, 100]

        centroids, centroid_labels = _clustering(
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



class ChooseInitialCentroidsTestCase(unittest.TestCase):
    def test_choose_initial_centroids(self):
        data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        initial_centroids = _choose_initial_centroids(data, k=3)
        assert 3 == len(initial_centroids)
        assert initial_centroids[0] in data
        assert initial_centroids[1] in data
        assert initial_centroids[2] in data


class FindNearestCentroidTestCase(unittest.TestCase):
    def test_find_nearest_centroid(self):
        data = np.array([0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24])
        centroids = np.array([3, 13, 23])
        dissimilarity_fn = lambda item1, item2: np.abs(item2 - item1)
        centroid_labels = _find_nearest_centroid(data, centroids, dissimilarity_fn)

        assert centroid_labels[0] == [0, 1, 2, 3, 4]
        assert centroid_labels[1] == [5, 6, 7, 8, 9]
        assert centroid_labels[2] == [10, 11, 12, 13, 14]


class CalculateNewCentroidsTestCase(unittest.TestCase):
    def test_calculate_new_centroids(self):
        data = np.array([10, 11, 12, 20, 21, 22, 30, 31, 32])
        centroid_labels = {
            0: [2, 1, 0],
            1: [3, 4, 5],
            2: [7, 8, 6]}

        average_fn = lambda data: np.mean(data)
        original_centroids = [15, 25, 35]
        new_centroids = _calculate_new_centroids(data, centroid_labels, average_fn, original_centroids)
        assert 3 == len(new_centroids)
        assert 11 == new_centroids[0]
        assert 21 == new_centroids[1]
        assert 31 == new_centroids[2]


class CalculateNewCentroidTestCase(unittest.TestCase):
    def test_calculate_new_centroid(self):
        cluster_data = [1, 2, 3]
        centroid_calc_fn = lambda cluster_data: np.mean(cluster_data)
        original_centroid = 1
        new_centroid = _calculate_new_centroid(cluster_data, centroid_calc_fn, original_centroid)
        assert 2 == new_centroid

    def test_keep_original_centroid_if_cluster_data_is_empty(self):
        cluster_data = []
        average_fn = lambda cluster_data: np.mean(cluster_data)
        original_centroid = 1
        new_centroid = _calculate_new_centroid(cluster_data, average_fn, original_centroid)
        assert 1 == new_centroid


class AverageCentroidsMoveTestCase(unittest.TestCase):
    def test_average_centroid_move(self):
        centroids = np.array([10, 20, 30, 40])
        new_centroids = np.array([20, 30, 40, 50])
        avg_dist = _average_centroids_move(centroids, new_centroids)
        assert 10 == avg_dist

    def test_average_centroid_move_with_dissimilarity_func(self):
        centroids = np.array([10, 20, 30, 40])
        new_centroids = np.array([20, 30, 40, 50])
        dist_func = lambda a, b: np.square(a - b)
        avg_dist = _average_centroids_move(centroids, new_centroids, dissimilarity_fn=dist_func)
        assert 100 == avg_dist


if __name__ == '__main__':
    unittest.main()

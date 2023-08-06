import numpy as np

def _clustering(data, k, dissimilarity_fn, centroid_calc_fn, stop_criteria=0.1, initial_centroids=None):
    if initial_centroids is None:
        centroids = _choose_initial_centroids(data, k)
    else:
        centroids = initial_centroids

    centroid_labels = None
    diff = 100000

    while diff > stop_criteria:
        centroid_labels = _find_nearest_centroid(data, centroids, dissimilarity_fn)
        new_centroids = _calculate_new_centroids(data, centroid_labels, centroid_calc_fn, centroids)
        diff = _average_centroids_move(centroids, new_centroids)
        centroids = new_centroids

    return centroids, centroid_labels


def _choose_initial_centroids(data, k):
    centroid_idxs = np.random.randint(data.shape[0], size=k)
    return data[centroid_idxs]


def _find_nearest_centroid(data, centroids, dissimilarity):
    centroid_labels = {}
    for idx in range(len(centroids)):
        centroid_labels[idx] = []

    for item_idx, item in enumerate(data):
        min_dist = None
        centroid_id = None
        for centroid_idx, c in enumerate(centroids):
            distance = dissimilarity(item, c)
            if min_dist == None or distance < min_dist:
                min_dist = distance
                centroid_id = centroid_idx
        centroid_labels[centroid_id].append(item_idx)

    return centroid_labels


def _calculate_new_centroids(data, centroid_labels, centroid_calc_fn, original_centroids):
    centroids = []

    for centroid_idx in range(len(original_centroids)):
        cluster_data = data[centroid_labels[centroid_idx]]
        original_centroid = original_centroids[centroid_idx]
        new_centroid = _calculate_new_centroid(cluster_data, centroid_calc_fn=centroid_calc_fn, original_centroid=original_centroid)
        centroids.append(new_centroid)

    return np.array(centroids)



def _calculate_new_centroid(cluster_data, centroid_calc_fn, original_centroid):
    if len(cluster_data) == 0:
        return original_centroid
    else:
        return centroid_calc_fn(cluster_data)

def _average_centroids_move(centroids, new_centroids, dissimilarity_fn=None):
    if dissimilarity_fn is None:
        dissimilarity_fn = lambda a, b: np.abs(a - b)
    result = []
    for index in range(len(centroids)):
        result.append(dissimilarity_fn(centroids[index], new_centroids[index]))
    return np.mean(result)

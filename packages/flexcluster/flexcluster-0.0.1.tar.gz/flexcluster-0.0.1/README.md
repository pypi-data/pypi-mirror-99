# flexcluster 

flexcluster is a python package that provides a flexible implementation for clustering algorithms based on K-means.

The package provides a generic clustering function that allows customization with callback parameters:
* **dissimilarity function** - *function(datapoint1, datapoint2) : int* - function that defines the distance between 2 data points.
* **centroid calculation function** - *function(datapoints : np.array) : datapoint* - function that calculates a centroid given an array of datapoints.

```
centroids, centroid_labels = clustering(
            data,
            k=3,
            dissimilarity_fn=dissimilarity_fn, <---- dissimilarity function
            centroid_calc_fn=centroid_calc_fn, <---- centroid calculation function)
            
centroids => calculated centroids per cluster
centroid_labels => map with a numeric key for each cluster and value is an array of item indexes
```

Kmeans and kmedoids are also provided in this package as shortcuts to specific cluster configuration.

```
centroids, centroid_labels = kmeans(data, k=3)
```
```
centroids, centroid_labels = kmedoids(data, k=3)
```



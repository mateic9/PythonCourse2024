import numpy as np

# Points in Cluster A
A = np.array([[-4, 0], [-3, 0]])

# Points in Cluster B
B = np.array([[-2, 0]])

# Compute pairwise distances
from scipy.spatial.distance import cdist
distances = cdist(A, B, metric='euclidean')

# Find the minimum distance
height = np.min(distances)

print(f"Height of the merged cluster: {height}")

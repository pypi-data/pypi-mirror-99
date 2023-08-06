from scipy.spatial import distance_matrix
from scipy.stats import pearsonr, spearmanr


def embedding_distance_correlation(original_distances, embedding, quiet=False):
    """
    params:
        original_distances: A pandas DataFrame of distances between objects
        embedding: e.g. a fitted TSNE object
    """
    transformed_distances = distance_matrix(embedding.embedding_, embedding.embedding_)
    transformed_distances = transformed_distances.ravel()
    original_distances = original_distances.values.ravel()
    r, p_r = pearsonr(original_distances, transformed_distances)
    rho, p_rho = spearmanr(original_distances, transformed_distances)
    if not quiet:
        print("R = %.3f; rho = %.3f" % (r, rho))
    return r, rho

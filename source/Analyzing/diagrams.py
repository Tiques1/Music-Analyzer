from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def kmeans(x_train_pca, kmeans=None):
    if kmeans is None:
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(x_train_pca)
    else:
        clusters = kmeans.predict(x_train_pca)
    return clusters, kmeans


def tsne_plot(x_train_pca, clusters):
    tsne = TSNE(random_state=42)
    x_train_tsne = tsne.fit_transform(x_train_pca)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(x_train_tsne[:, 0], x_train_tsne[:, 1], c=clusters, cmap='tab10', alpha=0.7)
    plt.colorbar(scatter, label='Cluster')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.title('Clusters in t-SNE Space')

    plt.show()


if __name__ == '__main__':
    x_train_pca =

    clusters, kmeans = kmeans(x_train_pca)
    tsne_plot(x_train_pca, clusters)

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA


class PrincipalComponentAnalysis:
    """Principal Component Analysis """

    def __init__(self):
        """Constructor"""

    def execute(self, df, features, target, covariance_percentage, plot_path, graphs=False):
        """Execute PCA"""
        feat_range = len(features) - 1
        for num in range(2, feat_range):
            try:
                pca = PCA(n_components=num)
                col_range = num + 1
                col_names = ['component_' + str(i) for i in range(1, col_range)]
                principal_components = pca.fit_transform(features)
                df_principal = pd.DataFrame(data=principal_components, columns=col_names)
                df_final = pd.concat([df_principal, df[target]], axis=1)
                info_percent = round(pca.explained_variance_ratio_.sum() * 100, 2)
                print('Principal Components: ', num, 'information percentage: ', info_percent, '%')
                if info_percent > covariance_percentage:
                    if graphs:
                        self.generate_graph(df_final, target, col_names, plot_path)

                    return df_final

            except Exception as e:
                """Exception"""
                print(e)
                break

        return df_final

    def generate_graph(self, df, target, feature_list, path):
        """Visualize PCA"""
        targets = pd.DataFrame(df[target].value_counts())
        targets = targets.index.to_list()

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        for feature1 in feature_list:
            for feature2 in feature_list:
                if feature1 != feature2:
                    fig = plt.figure(figsize=(8, 8))
                    ax = fig.add_subplot(1, 1, 1)
                    ax.set_xlabel(feature1, fontsize=15)
                    ax.set_ylabel(feature2, fontsize=15)
                    ax.set_title('Components Covariance ', fontsize=20)
                    for target, color in zip(targets, colors):
                        indicesToKeep = df['readmitted'] == target
                        ax.scatter(df.loc[indicesToKeep, feature1]
                                   , df.loc[indicesToKeep, feature2]
                                   , c=color
                                   , s=50)
                    ax.legend(targets)
                    ax.grid()
                    title = 'PCA ' + feature1 + ' vs ' + feature2
                    file_name = path + title + '.png'
                    fig.savefig(file_name, bbox_inches='tight', dpi=100, title=plt.title)
                    plt.close(fig)

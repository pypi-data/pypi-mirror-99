from palettable.matplotlib import matplotlib

# Import Libraries
import pandas as pd
import numpy as np


import matplotlib as mtl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns

from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler


class MissingValues:
    """Missing Values Operations"""

    def __init__(self):
        """Constructor"""

    def generate_missing_value_plots(self, df, title, path):
        """Visualize the missing plots"""
        self.visualize_null_plot(df, title, path)
        self.visualize_missing_density(df, title, path)
        self.visualize_missing_bar(df, title, True, path)
        self.visualize_missing_bar(df, title, False, path)
        self.visualize_missing_heatmap(df, title, path)
        self.visualize_missing_dendrogram(df, title, path)

    def visualize_null_plot(self, df, title, path=None):
        """To Visualize the null values from DataFrame"""
        title = 'Pandas Missing Values ' + title
        df.isnull().sum().plot(kind='bar')
        plt.title(title, fontsize=20, color='#3dcd58')
        file_name = path + title + '.png'
        plt.savefig(file_name, bbox_inches='tight', dpi=100, title=plt.title)
        plt.close()

    def visualize_missing_density(self, df, title, path=None):
        """To visualize the missing value density of given dataframe"""
        title = 'Missing Data Density ' + title
        msno.matrix(df)
        plt.title(title, fontsize=20, color='#3dcd58')
        file_name = path + title + '.png'
        plt.savefig(file_name, bbox_inches='tight', dpi=100, title=plt.title)
        plt.close()

    def visualize_missing_bar(self, df, title, log, path=None):
        """Visualize the missing data in Bar Chart"""
        title = 'Missing Data Bar ' + title
        msno.bar(df, color="blue", log=log)
        plt.title(title, fontsize=20, color='#3dcd58')
        file_name = path + title + '.png'
        plt.savefig(file_name, bbox_inches='tight', dpi=100, title=plt.title)
        plt.close()

    def visualize_missing_heatmap(self, df, title, path=None):
        """Visualize the missing data in Heatmap"""
        title = 'Heat Map Missing Data Correlation ' + title
        msno.heatmap(df)
        plt.title(title, fontsize=20, color='#3dcd58')
        file_name = path + title + '.png'
        plt.savefig(file_name, bbox_inches='tight', dpi=100, title=plt.title)
        plt.close()

    def visualize_missing_dendrogram(self, df, title, path=None):
        """Visualize the missing data in Dendrogram"""
        title = 'Dendrogram Missing Data ' + title
        msno.dendrogram(df)
        plt.title(title, fontsize=20, color='#3dcd58')
        file_name = path+ title + '.png'
        plt.savefig(file_name, bbox_inches='tight', dpi=100, title=plt.title)
        plt.close()

    def get_null_counts(self, df):
        """Tabulate the Null Counts"""
        nulls = df.isnull().sum()
        total_rows = df.shape[0]
        null_list = []
        for series in nulls.iteritems():
            if series[1] > 0:
                type = df[series[0]].dtype
                percentage = round((series[1] / total_rows) * 100, 2)
                null_list.append([series[0], series[1], percentage, type])
        dfNull = pd.DataFrame(null_list)
        dfNull.columns = ['Column', 'Missing Values', 'Missing %', 'Type']
        dfNullSorted = dfNull.sort_values(by='Missing Values', ascending=False)
        return dfNullSorted

    def get_missing_columns_by_value(self, df, percent):
        """Getting the List of columns values equal or more than given percent"""
        dfNull = self.get_null_counts(df)
        high_missing = dfNull[dfNull['Missing %'] <= percent].index
        dfNull.drop(high_missing, inplace=True)
        column_list = dfNull[dfNull.columns[0]].values
        return dfNull, column_list

    def remove_columns(self, df, columns_list):
        """Remove Columns from DataFrame"""
        df = df.drop(columns_list, axis=1)
        return df

    def impute_by_mean(self, df, column):
        """To Impute Missing Values by Mean"""
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        df[column] = imputer.fit_transform(df[[column]]).ravel()
        return df

    def impute_by_median(self, df, column):
        """To Impute Missing Values by Median"""
        imputer = SimpleImputer(missing_values=np.nan, strategy='median')
        df[column] = imputer.fit_transform(df[[column]]).ravel()
        return df

    def impute_by_most_frequent(self, df, column):
        """To Impute Missing Values by Median"""
        imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        df[column] = imputer.fit_transform(df[[column]]).ravel()
        return df





def main():
    """Main Function"""
    print('-------------------------------------\n')










    # Outlier
    outlier_data = mv.find_outlier_zscore(df_missing_dropped, 3)
    print('\nOutlier Points:\n', outlier_data)
    print('-------------------------------------\n')





if __name__ == '__main__':
    main()

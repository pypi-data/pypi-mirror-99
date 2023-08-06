from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
from pylab import rcParams
from sklearn.cluster import DBSCAN

rcParams['figure.figsize'] = 5, 4
sb.set_style('whitegrid')


class Outlier:
    """Outlier Object"""

    def __init__(self):
        """Constructor"""

    def get_outlier_by_zscore(self, df, columns, threshold):
        """Need to Update"""
        print("Dropping Outliers - ZScore")
        info = []
        df_out = df.copy()
        for col in columns:
            try:
                mean_1 = np.mean(df)
                std_1 = np.std(df)
                outliers = []
                for y in df:
                    z_score = (y - mean_1) / std_1
                    if np.abs(z_score) > threshold:
                        """df_out = df_out[df_out[column] < upper_bound]"""

            except:
                print(col)

        return outliers

    def drop_outliers_by_iqr(self, df, columns, drop_percent):
        """Drop Outlier Rows By IQR"""
        print('Processing outliers:')
        info = []
        df_out = df.copy()
        df_out_rows = pd.DataFrame()
        for column in columns:
            try:
                details = df_out[column].describe()
                count = details[0]
                mean = details[1]
                std = details[2]
                min = details[3]
                q1 = details[4]
                q2 = details[5]
                q3 = details[6]
                max = details[7]

                iqr = q3 - q1
                upper_bound = round(q3 + (1.5 * iqr), 5)
                lower_bound = round(q1 - (1.5 * iqr), 5)

                # Ourlier Rows
                df_upper_rows = df_out[df_out[column] > upper_bound]
                df_lower_rows = df_out[df_out[column] < lower_bound]

                total_rows = df_out.shape[0]

                df_drop_check = df_out.copy()
                df_drop_check = df_drop_check[df_drop_check[column] < upper_bound]
                df_drop_check = df_drop_check[df_drop_check[column] > lower_bound]

                rows_dropped = total_rows - df_drop_check.shape[0]
                outlier_percent = round((rows_dropped / total_rows) * 100, 3)

                if outlier_percent < drop_percent:
                    df_out = df_out[df_out[column] < upper_bound]
                    df_out = df_out[df_out[column] > lower_bound]
                    info.append(
                        [column, 'dropped', outlier_percent, rows_dropped, total_rows, lower_bound, upper_bound, iqr,
                         min, q1, q2, q3,
                         max, mean, std])

                    df_out_rows = pd.concat([df_upper_rows, df_lower_rows, df_out_rows])

                    debug = 0
                else:
                    info.append(
                        [column, 'not dropped', outlier_percent, rows_dropped, total_rows, lower_bound, upper_bound,
                         iqr, min, q1, q2, q3,
                         max, mean, std])


            except Exception as e:
                print(column, '\tError: ', e)

        print('Outlier Rows', df_out_rows.shape)
        df_out_rows.to_csv('data/outlier_rows.csv', index=False)

        df_drop_info = pd.DataFrame(info)
        df_drop_info.columns = ['Feature', 'Status', 'Percent', 'Dropped', 'Total Rows', 'Lower', 'Upper', 'IQR', 'Min',
                                'Q1',
                                'Q2', 'Q3', 'Max', 'Mean', 'Std']

        return df_out, df_drop_info

    def generate_outlier_graphs(self, df, columns, target, path):
        """"Generate Outlier Graphs for Visualization """
        for col in columns:
            try:
                fig = plt.figure(figsize=(20, 6))
                main_title = col + ' Outlier'
                fig.suptitle(main_title, fontsize=18, color='#304FFE')

                ax1 = fig.add_subplot(121)
                ax1.set_title('Univariate', fontdict={'fontsize': 15, 'fontweight': 'medium'})
                df_outlier = df.filter([col])
                df_outlier.boxplot(return_type='dict')

                ax2 = fig.add_subplot(122)
                ax2.set_title('Multivariate', fontdict={'fontsize': 15, 'fontweight': 'medium'})
                sb.boxplot(x=col, y=target, data=df, palette='hls')

                file_name = path + col + '_outlier.png'
                plt.savefig(file_name, bbox_inches='tight', dpi=100)
                plt.close()
            except:
                print(col)
                continue

    def detect_outliers_by_dbscan(self, df, columns, target, path, eps, min_samples):
        """Generate Outlier Graphs by DBSCAN"""
        print('Outliers DBSCAN')
        for col in columns:
            try:
                y = df[target].values.reshape(-1, 1)
                x = df[col].values.reshape(-1, 1)
                model = DBSCAN(eps=eps, min_samples=min_samples).fit(x)
                outliers_df = pd.DataFrame(x)
                print(Counter(model.labels_))
                print(outliers_df[model.labels_ == -1])

                fig = plt.figure()
                ax = fig.add_axes([.1, .1, .1, .1])
                colors = model.labels_
                ax.scatter(x[:, 2], x[:, 1], c=colors, s=120)
                ax.et_xlabel('Petal Length')
                plt.title('DBScan for Outlier Detection')

                file_name = path + col + '_DBSCAN.png'
                plt.savefig(file_name, bbox_inches='tight', dpi=100)
                plt.close()


            except:
                print(col)

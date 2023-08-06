import pandas as pd
import matplotlib.pyplot as plt


class FeatureEngineering:
    """Feature Engineering Operations"""

    def __init__(self):
        '''Constructor'''

    def has_null_values(self, df, column_list):
        status = True
        val = df[column_list].isnull().sum()
        sum = val.sum()
        if sum == 0:
            status = False

        return status

    def get_missing_value_columns(self, df):
        col_list = []
        val = df[df.columns].isnull().sum()
        for series in val.iteritems():
            if series[1] > 0:
                col_list.append(series[0])

        return col_list

    def fill_missing_value_with_unknown(self, df, column_list):
        missing_cols = self.get_missing_value_columns(df)
        for col in column_list:
            if col in missing_cols:
                df[col] = df[col].fillna('UNK')  # UNK - Unknown Value

    def get_items_count(self, df, feature, ascending):
        count_list = []
        val = df.groupby(feature).size()
        for series in val.iteritems():
            count_list.append([series[0], series[1]])

        df = pd.DataFrame(count_list)
        df.columns = ['item', 'count']
        df = df.sort_values(by='count', ascending=ascending)
        return df

    def get_top_items(self, df, feature, count, ascending):
        count_list = []
        val = df.groupby(feature).size()
        for series in val.iteritems():
            count_list.append([series[0], series[1]])

        df = pd.DataFrame(count_list)
        df.columns = ['item', 'count']
        df = df.sort_values(by='count', ascending=ascending)
        count_list = df['item'].values
        return count_list[:count]

    def add_categorical_column(self, df, column, bin_list, include_right):
        bin_values = pd.cut(x=df[column], bins=bin_list, right=include_right)
        bin_name = column + '_bin'
        df[bin_name] = bin_values
        return df

    def convert_to_binary_column(self, df, column):
        """Create new columns """
        binary_values = []
        for value in df[column]:
            if value == 0:
                binary_values.append(0)
            else:
                binary_values.append(1)

        df = df.drop(columns=[column], axis=1)
        df[column] = binary_values

        return df

    def get_unique_info(self, df, column):
        ndf = df.copy()
        unique_list = ndf[column].unique()
        column_values = ndf[column].to_list()
        total = df.shape[0]

        unique = []
        for item in unique_list:
            count = column_values.count(item)
            percent = round((count / total) * 100, 2)
            unique.append([item, count, percent])

        dfUnique = pd.DataFrame(unique)
        dfUnique.columns = ['item', 'Count', 'percent']

        return dfUnique

    def summerize_items_frequency(self, df, column_list, value_list):
        ndf = df.copy()
        total = df.shape[0]

        rows = []
        for column in column_list:
            column_values = ndf[column].to_list()

            status = True
            for val in value_list:
                if not val in column_values:
                    status = False

            if status:
                item_percent = []
                item_count = []
                for item in value_list:
                    count = column_values.count(item)
                    percent = round((count / total) * 100, 2)
                    item_percent.append(percent)
                    item_count.append(count)

                row = [column]
                for num in range(0, len(value_list)):
                    row.append(item_percent[num])

                for num in range(0, len(value_list)):
                    row.append(item_count[num])

                rows.append(row)

        df_summary = pd.DataFrame(rows)

        col_names = ['column']
        for val in value_list:
            percent = val + ' (%)'
            col_names.append(percent)

        for val in value_list:
            count = val + ' (Nos.)'
            col_names.append(count)

        df_summary.columns = col_names
        return df_summary

    def generate_frequency_distribution_graphs(self, df, target, path):
        """Visulize the frequency distribution charts"""
        for col in df.columns:
            title = 'Frequeny of ' + col + ' against ' + target
            pd.crosstab(df[col], df[target]).plot(kind='bar')
            plt.title(title)
            plt.xlabel(col)
            plt.ylabel(target)
            plt.title(title, fontsize=18, color='#626469')

            file_name = path + title + '.png'
            plt.savefig(file_name, bbox_inches='tight', dpi=100)
            plt.close()

            title = 'Frequeny of ' + target + ' against ' + col
            pd.crosstab(df[target], df[col]).plot(kind='bar')
            plt.title(title)
            plt.xlabel(col)
            plt.ylabel(target)
            plt.title(title, fontsize=18, color='#626469')

            file_name = path + title + '.png'
            plt.savefig(file_name, bbox_inches='tight', dpi=100)
            plt.close()
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport


class Preprocessor:

    def __init__(self):
        """Constructor"""

    def import_data(self, path, file, missing_values=None, data_types=None):

        # Concatenating Path and File
        data_file = path + file
        df = pd.read_csv(data_file, na_values=missing_values,
                         low_memory=False,
                         dtype=data_types)
        return df

    def get_unique_values(self, df, column_list):
        list_unique = []
        for col in column_list:
            list_unique.append([col, df[col].nunique()])

        df = pd.DataFrame(list_unique)
        df.columns = ['feature', 'unique_items']
        df = df.sort_values(by='unique_items', ascending=False)
        return df

    def remove_constant_columns(self, df):
        """Automatically remove constant columns from the data set"""
        for col in df.columns:
            if df[col].nunique() == 1:
                """Drop"""
                df = df.drop([col], axis=1)

        return df

    def set_column_type(self, df, column_list, category):
        """Set Columns Data Type"""
        for col in df.columns:
            if col in column_list:
                df[col]= df[col].astype(category)
        return df

    def convert_object_to_category_columns(self, df):
        """Automatically convert object data types into Categorical data types"""
        df.loc[:, df.dtypes == 'object'] = df.select_dtypes(['object']).apply(lambda x: x.astype('category'))
        return  df

    def generate_profile_report(self, df, report_name):
        # Method Using Profiling
        profile = ProfileReport(df, minimal=True,
                                plot={'histogram': {'bins': 8}},
                                title='Hospital Care Report',
                                html={'style': {'full_width': True}})
        profile.to_file(output_file=report_name)

    def get_numerical_cols(self, df):
        """Collect numerical columns from the given dataset"""
        ncols = df.iloc[:, (np.where((df.dtypes == np.int64) | (df.dtypes == np.float64)))[0]].columns
        return ncols

    def validate_data_type(self, df, column_list):
        """Automatically categorize the columns by it unique counts"""
        list_unique = []
        for col in column_list:
            data_type = 'object'
            if df[col].nunique() > 2:
                if df[col].dtype == 'int64':
                    data_type = 'numerical'
                else:
                    data_type = 'categorical'
            elif df[col].nunique() > 1:
                data_type = 'binary'
            else:
                data_type = 'constant'

            list_unique.append([data_type, col, df[col].nunique()])

        df = pd.DataFrame(list_unique)
        df.columns = ['data_type', 'feature', 'unique_items']
        df = df.sort_values(by='unique_items', ascending=False)
        return df

    def get_binary_columns(self, df):
        """Collect numerical columns from the given dataset"""
        list_binary_cols = []
        for col in df.columns:
            data_type = 'object'
            if df[col].nunique() == 2:
                data_type = 'binary'
                list_binary_cols.append(col)

        return list_binary_cols

    def get_categorical_columns(self, df):
        """Collect categorical column from the given dataset"""
        list_categorical_cols = []
        for col in df.columns:
            data_type = 'object'
            if df[col].nunique() > 2:
                if not df[col].dtype == 'int64':
                    data_type = 'categorical'
                    list_categorical_cols.append(col)

        return list_categorical_cols










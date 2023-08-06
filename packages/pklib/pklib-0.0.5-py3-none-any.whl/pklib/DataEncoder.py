import category_encoders as ce
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from pklib.Preprocessor import Preprocessor


class DataEncoder:
    """Data Encoding Operations"""

    def __init__(self):
        """Constructor"""
        self.pp = Preprocessor()

    def do_target_encoding(self, df, columns, target, target_true_val):
        """Do Target Encoding for the given columns"""

        # Get Unique Values
        for col in columns:
            unique_vals = df[col].unique()

            for val in unique_vals:
                is_val = df[col] == val
                df_col = df[is_val]
                all_val_items = df_col.shape[0]

                is_true = df_col[target] == target_true_val
                is_true_df_col = df_col[is_true]
                true_val_items = is_true_df_col.shape[0]

                if all_val_items > 0:
                    mean = round(true_val_items / all_val_items, 5)
                else:
                    mean = 0

                df[col] = df[col].replace(val, mean)


            df[col] = pd.to_numeric(df[col])
        return df

    def do_label_target_encoding(self, df, columns, target):
        """Do Target Encoding for Given Columns - Here Using Label and Target Encoder used"""
        df_lable_encoding = self.do_label_encoding(df, columns)
        te = ce.TargetEncoder(cols=columns)
        data = te.fit_transform(df_lable_encoding, df_lable_encoding[target])
        return data

    def do_label_encoding(self, df, columns):
        """Do Label Encoding for given columns"""
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col])

        df[col] = pd.to_numeric(df[col])
        return df

    def do_ordinal_encoding(self, df, column, order_list, start_no):
        """Do Ordinal Encoding By Given Order"""
        data = df.copy()
        for item in order_list:
            data[column] = data[column].replace(item, start_no)
            start_no = start_no + 1

        data[column] = pd.to_numeric(data[column])
        return data

    def do_onehot_encoding(self, df, columns):
        """Do OneHot Encoding for given columns"""
        onehotencoder = ce.OneHotEncoder(cols=columns)
        data = onehotencoder.fit_transform(df)
        feat_names = onehotencoder.get_feature_names()
        data.columns = feat_names
        return data

    def do_dummy_encoding(self, df, columns):
        """Do dummy encoding for given columns"""
        df_concate = df.copy()
        for col in columns:
            df_ohe = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df_drop = df_concate.drop(columns=[col], axis=1)
            df_concate = pd.concat([df_drop, df_ohe], axis=1, sort=False)
        return df_concate



    def do_binary_encoding(self, df, column, true_value ):
        """Do Binary Encoding for given Column"""
        unique_vals = df[column].unique()
        for val in unique_vals:
            if val == true_value:
                df[column] = df[column].replace(val, 1)
            else:
                df[column] = df[column].replace(val, 0)

        #df[column] = pd.to_numeric(df[column])
        df[column] = df[column].astype(np.uint8)
        return df


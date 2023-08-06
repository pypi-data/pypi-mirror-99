import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


class DataScaling:
    """Scale Data Features"""

    def __init__(self):
        """Constructor"""

    def z_scale(self, df, columns):
        """Scale only the numerical columns using Standard Scaler"""
        df_z = df.copy()
        scaler = StandardScaler()
        for col in columns:
            scaled_col = scaler.fit_transform(df[col].values.reshape(-1, 1))
            df_z.drop(col, axis=1)
            df_z[col] = scaled_col
        return df_z

    def min_max_scale(self, df, columns):
        """Scale only the numerical columns using Min-Max Normalization"""
        df_m = df.copy()
        scaler = MinMaxScaler()
        for col in columns:
            scaled_col = scaler.fit_transform(df[col].values.reshape(-1, 1))
            df_m.drop(col, axis=1)
            df_m[col] = scaled_col
        return df_m

    def robust_scale(self, df, columns):
        """Scale only the numerical columns using Robust Normalization"""
        df_r = df.copy()
        scaler = RobustScaler()
        for col in columns:
            scaled_col = scaler.fit_transform(df[col].values.reshape(-1, 1))
            df_r.drop(col, axis=1)
            df_r[col] = scaled_col
        return df_r

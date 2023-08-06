import pandas as pd
import numpy as np
import seaborn as sb
from ggplot import *
import matplotlib.pyplot as plt


class DataVisualization:
    """Visualize the Data"""

    def __init__(self):
        """Constructor"""


    def generate_count_plots(self, df, path):
        """Generate Count Plots"""
        plt.figure(figsize=(20, 10))
        for col in df.columns:
            title = col + ' Count Plot'
            title = title.replace('>', 'greater')
            title = title.replace('<', 'lesser')
            title = title.replace('/', '_')
            plot = qplot(x=col, data=df) + ggtitle(title)
            file_name = path + title + '.png'
            plot.save(file_name, dpi=300)
            plt.title(title, fontsize=14, color='#3dcd58')


    def generate_density_plots(self, df, color, path):
        """Generate Density Plots"""
        plt.figure(figsize=(20, 10))
        for col in df.columns:
            try:
                title = col + ' Density Plot'
                title = title.replace('>', 'greater')
                title = title.replace('<', 'lesser')
                title = title.replace('/', '_')

                plot = ggplot(df, aes(x=col, color=color)) + \
                       geom_density() + ggtitle(title)
                file_name = path + title + '.png'
                plot.save(file_name, dpi=300)
                plt.title(title, fontsize=14, color='#3dcd58')
            except Exception as e:
                print('Density Plot Error: ', col, ' ', e)

    def generate_violin_plots(self, df, target, color, path):
        """Generate Density Plots"""
        plt.figure(figsize=(20, 10))
        for col in df.columns:
            try:
                title = col + ' Violin Plot'
                title = title.replace('>', 'greater')
                title = title.replace('<', 'lesser')
                title = title.replace('/', '_')

                plot = ggplot(df, aes(x=col, y=target,
                                      color=color)) + \
                       geom_violin() + ggtitle(title)
                file_name = path + title + '.png'
                plot.save(file_name, dpi=300)
                plt.title(title, fontsize=14, color='#3dcd58')
            except Exception as e:
                print('Violin Plot Error: ', col, ' ', e)


    def generate_histograms(self, df, target, fill, path):
        """Generate Density Plots"""
        plt.figure(figsize=(20, 10))
        for col in df.columns:
            try:
                title = col + ' Histogram'
                title = title.replace('>', 'greater')
                title = title.replace('<', 'lesser')
                title = title.replace('/', '_')

                plot = ggplot(df, aes(x=col, y=target,
                                      fill=fill)) + \
                       geom_histogram() + ggtitle(title)
                file_name = path + title + '.png'
                plot.save(file_name, dpi=300)
                plt.title(title, fontsize=14, color='#3dcd58')
            except Exception as e:
                print('Histogram Error: ', col, ' ', e)

    def generate_jitter_plot(self, df, target,  path):
        """Generate Density Plots"""
        plt.figure(figsize=(20, 10))
        for feat1 in df.columns:
            for feat2 in df.columns:
                if feat1 != feat2:
                    try:
                        title = feat1 + '_' + feat2 + ' Jitter Plot'
                        title = title.replace('>', 'greater')
                        title = title.replace('<', 'lesser')
                        title = title.replace('/', '_')

                        plot = ggplot(df, aes(x=feat1, y=feat2, color=target)) + \
                               geom_jitter() + ggtitle(title)
                        file_name = path + title + '.png'
                        plot.save(file_name, dpi=300)
                        plt.title(title, fontsize=14, color='#3dcd58')
                    except Exception as e:
                        print('Jitter Plot Error: ', feat1, ' ', e)




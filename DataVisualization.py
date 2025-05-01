'''This is a module for visualizing and analyzing graph data. It includes the following class: DataVisualization.'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Literal
from typing import List
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


class DataVisualization:
    '''This class is used to visualize and analyze graph data. It includes methods for plotting correlation heatmaps, distributions, and relationships between metrics.\n
    inputs\n
        data_file: str'''
    def __init__(self, data_file):
        self.df = pd.read_csv(data_file)
        self.__feild_to_title = {
            'subject_id': 'Subject ID',
            'control_or_patient': 'Control or Patient',
            'nodes': 'Number of Nodes',
            'edges': 'Number of Edges',
            'possible_edges': 'Possible Edges',
            'density': 'Density',
            'average_degree': 'Average Degree',
            'symmetric': 'Symmetric',
            'CCrand': 'Clustering Coefficient (Random)',
            'CCreal': 'Clustering Coefficient (Real)',
            'CPLrand': 'Characteristic Path Length (Random)',
            'CPLreal': 'Characteristic Path Length (Real)',
            'CCdiff': 'Clustering Coefficient Difference',
            'CPLdiff': 'Characteristic Path Length Difference',
            'small_world_coefficient': 'Small World Coefficient',
            'number_of_subgraphs': 'Number of Subgraphs',
            'biggest_subgraph_nodes': 'Nodes in the Largest Subgraph',
            'biggest_subgraph_edges': 'Edges in the Largest Subgraph'
        }

    def plot_correlation_heatmap(self):
        '''This method plots a correlation heatmap for the numeric columns in the DataFrame.'''
        numeric_df = self.df.select_dtypes(include=['number'])
        corr = numeric_df.corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.show()
    
    def plot_distribution(
        self,
        metric: Literal[
            'density', 'average_degree', 'CCrand', 'CCreal',
            'CPLrand', 'CPLreal', 'small_world_coefficient',
            'number_of_subgraphs', 'biggest_subgraph_nodes',
            'biggest_subgraph_edges', 'nodes', 'edges', 'possible_edges'
        ],
        kind: Literal['box', 'violin'] = 'box',
        save: bool = False
        ):
        '''This method plots the distribution of a specified metric, either as a boxplot or violin plot.\n
        inputs\n
            metric: str - The metric to plot.\n
            kind: str - The type of plot ('box' or 'violin').\n
            save: bool - Whether to save the plot as a PNG file.'''
        plt.figure(figsize=(8, 6))
        if kind == 'violin':
            sns.violinplot(data=self.df, x='control_or_patient', y=metric)
        else:
            sns.boxplot(data=self.df, x='control_or_patient', y=metric)
        if save:
            plt.tight_layout()
            plt.savefig(f"{metric}_distribution.png", dpi=300)
        plt.title(f'{self.__feild_to_title[metric]} distribution by group')
        plt.tight_layout()
        plt.show()
    
    def plot_multiple_vs_x(
        self,
        x_metric: Literal[
            'density', 'average_degree', 'CCrand', 'CCreal',
            'CPLrand', 'CPLreal', 'small_world_coefficient',
            'number_of_subgraphs', 'biggest_subgraph_nodes',
            'biggest_subgraph_edges', 'nodes', 'edges', 'possible_edges'
        ],
        y_metrics: List[Literal[
            'density', 'average_degree', 'CCrand', 'CCreal',
            'CPLrand', 'CPLreal', 'small_world_coefficient',
            'number_of_subgraphs', 'biggest_subgraph_nodes',
            'biggest_subgraph_edges', 'nodes', 'edges', 'possible_edges'
        ]],
        kind: Literal['line', 'scatter'] = 'scatter',
        highlight_groups: bool = False
        ):
        '''This method plots multiple metrics against a specified x metric.\n
        inputs\n
            x_metric: str - The x metric to plot.\n
            y_metrics: list[str] - A list of y metrics to plot.\n
            kind: str - The type of plot ('line' or 'scatter').\n
            highlight_groups: bool - Whether to highlight control and patient groups.'''
        plt.figure(figsize=(10, 6))
        palette = sns.color_palette(n_colors=len(y_metrics))

        for i, metric in enumerate(y_metrics):
            color = palette[i]
            if highlight_groups and kind == 'scatter':
                sns.scatterplot(
                    data=self.df,
                    x=x_metric,
                    y=metric,
                    hue='control_or_patient',
                    style='control_or_patient',
                    markers={'control': 'o', 'patient': 'X'},
                    palette=[color, color],
                    legend=False,  
                    alpha=0.7,
                    label=f"{self.__feild_to_title[metric]}"
                )
            elif kind == 'line':
                sns.lineplot(
                    data=self.df,
                    x=x_metric,
                    y=metric,
                    color=color,
                    label=f"{self.__feild_to_title[metric]}"
                )
            else:
                sns.scatterplot(
                    data=self.df,
                    x=x_metric,
                    y=metric,
                    color=color,
                    label=f"{self.__feild_to_title[metric]}"
                )
        y_label_format = ''
        
        if len(y_metrics) == 2:
            y_label_format += f"{self.__feild_to_title[y_metrics[0]]} and {self.__feild_to_title[y_metrics[1]]}"
        elif len(y_metrics) > 2:
            for metric in y_metrics:
                if metric == y_metrics[-1]:
                    y_label_format += f"and {self.__feild_to_title[metric]}"
                else:
                    y_label_format += f"{self.__feild_to_title[metric]}, "
        else:
            raise ValueError("y_metrics must contain 2 or more metrics.")
        plt.title(f'{y_label_format} vs {self.__feild_to_title[x_metric]}')
        plt.xlabel(self.__feild_to_title[x_metric])
        plt.ylabel(f"{y_label_format}")
        plt.legend(title="Metrics")
        plt.tight_layout()
        plt.show()

    def plot_metric_vs_metric(
        self,
        x_metric,
        y_metric,
        trend: Literal[
            'linear', 'log', 'power_law', 'exponential',
            'logarithmic', 'reciprocal'
        ] = 'linear', 
        highlight_groups=False,
        save=False
        ):
        '''This method plots a specified x metric against a specified y metric with a trend line.\n
        inputs\n
            x_metric: str - The x metric to plot.\n
            y_metric: str - The y metric to plot.\n
            trend: str - The type of trend line to fit ('linear', 'log', 'power_law', 'exponential', 'logarithmic', 'reciprocal').\n
            highlight_groups: bool - Whether to highlight control and patient groups.\n
            save: bool - Whether to save the plot as a PNG file.'''
        df = self.df.copy()

        if trend in ['log', 'power_law', 'exponential', 'logarithmic', 'reciprocal']:
            df = df[(df[x_metric] > 0) & (df[y_metric] > 0)]

        plt.figure(figsize=(8, 6))
        xlabel, ylabel = self.__feild_to_title[x_metric], self.__feild_to_title[y_metric]

        if highlight_groups:
            palette = {'control': 'blue', 'patient': 'orange'}
            for group, group_df in df.groupby("control_or_patient"):
                plt.scatter(
                    group_df[x_metric], group_df[y_metric],
                    label=group,
                    alpha=0.6,
                    marker='o' if group == 'control' else 'X',
                    color=palette[group]
                )
        else:
            plt.scatter(df[x_metric], df[y_metric], alpha=0.6)

        x = df[x_metric].values
        y = df[y_metric].values

        if trend == 'linear':
            coeffs = np.polyfit(x, y, 1)
            y_pred = np.polyval(coeffs, x)
            r2 = r2_score(y, y_pred)

            sns.regplot(
                data=df,
                x=x_metric,
                y=y_metric,
                ci=None,
                scatter=False,
                color='red',
                label=f'Linear Fit\n$R^2$ = {r2:.3f}'
            )
            plt.title(f"{ylabel} vs {xlabel} with linear trend")

        elif trend == 'log':
            df[x_metric] = np.log(df[x_metric])
            df[y_metric] = np.log(df[y_metric])
            x_log = df[x_metric].values
            y_log = df[y_metric].values

            coeffs = np.polyfit(x_log, y_log, 1)
            y_pred = np.polyval(coeffs, x_log)
            r2 = r2_score(y_log, y_pred)

            sns.regplot(
                data=df,
                x=x_metric,
                y=y_metric,
                ci=None,
                scatter=False,
                color='red',
                label=f'Log-Log Fit\n$R^2$ = {r2:.3f}'
            )
            plt.title(f"log({ylabel}) vs log({xlabel}) with log-log trend")

        else:
            fit_func = None
            label_template = ""
            color = 'red'

            if trend == 'power_law':
                def fit_func(x, a, b): return a * np.power(x, -b)
                label_template = 'Power Law Fit\n$y = {:.2f}x^{{-{:.2f}}}$\n$R^2$ = {:.3f}'
            elif trend == 'exponential':
                def fit_func(x, a, b): return a * np.exp(-b * x)
                label_template = 'Exponential Fit\n$y = {:.2f}e^{{-{:.2f}x}}$\n$R^2$ = {:.3f}'
                color = 'green'
            elif trend == 'logarithmic':
                def fit_func(x, a, b): return a - b * np.log(x)
                label_template = 'Logarithmic Fit\n$y = {:.2f} - {:.2f}\\log(x)$\n$R^2$ = {:.3f}'
                color = 'purple'
            try:
                popt, _ = curve_fit(fit_func, x, y, maxfev=10000)
                if np.any(~np.isfinite(popt)):
                    raise ValueError("Non-finite fit parameters")

                y_pred = fit_func(x, *popt)
                r2 = r2_score(y, y_pred)

                x_fit = np.linspace(np.min(x), np.max(x), 500)
                y_fit = fit_func(x_fit, *popt)

                plt.plot(
                    x_fit, y_fit,
                    linestyle='--',
                    color=color,
                    label=label_template.format(*popt, r2)
                )
                plt.title(f"{self.__feild_to_title[ylabel]} vs {self.__feild_to_title[xlabel]} with {trend} fit")

            except Exception as e:
                plt.title(f"{ylabel} vs {xlabel} — {trend} fit failed")
                print(f"[{trend} fit error]: {e}")

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.tight_layout()
        if save:
            plt.savefig(f"{x_metric}_vs_{y_metric}_{trend}.png", dpi=300)
        plt.show()


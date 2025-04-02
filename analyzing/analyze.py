import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.gridspec as gs

def analyze(feature_df: pd.DataFrame):
    os.makedirs('./results/illustrations',exist_ok=True)

    feature_columns =[col for col in feature_df.columns if not col.startswith(('file_name','attack_type_','attack_subtype_'))]
    x = feature_df[feature_columns]
    attack_columns = [col for col in feature_df.columns if col.startswith(('attack_type_','attack_subtype_'))]
    y= (feature_df[attack_columns].sum(axis=1) > 0).astype(int)

    print("Dataset shape:", x.shape)
    print("\nFeature statistics:")
    print(x.describe())

    #Feature correlation Matrix

    plt.figure(figsize=(14,12))
    correlation_matrix = x.corr()
    sns.heatmap(correlation_matrix,annot=False,cmap='coolwarm')
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig('./results/illustrations/feature_correlation_matrix.png')
    plt.close()

    #Histogram of each feature

    num_features = len(feature_columns)
    cols = 3
    rows = (num_features + cols -1)
    plt.figure(figsize=(16,rows*4))
    for i, feature in enumerate(feature_columns):
        plt.subplot(rows,cols,i+1)
        sns.histplot(x[feature],kde=True)
        plt.title(f"{feature} Distribution")
        plt.tight_layout()
    plt.savefig('./results/illustrations/feature_histograms.png')
    plt.close()

    #Missing values Map
    plt.figure(figsize=(12,8))
    sns.heatmap(x.isnull(),cbar=False, cmap='viridis')
    plt.title('Missing Values Map')
    plt.tight_layout()
    plt.savefig('./results/illustrations/missing_values_map.png')
    plt.close()

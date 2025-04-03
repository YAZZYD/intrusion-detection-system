import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def analyze(feature_df: pd.DataFrame)-> tuple[pd.DataFrame, pd.Series]:
    os.makedirs('./results/illustrations',exist_ok=True)

    print("Analyzing data...")

    feature_columns =[col for col in feature_df.columns if not col.startswith(('file_name','attack_type_','attack_subtype_'))]
    x = feature_df[feature_columns]
    y = feature_df['is_attack']

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

    pair_data=x.copy()
    pair_data['target']=y
    plt.figure(figsize=(16,16))
    g = sns.pairplot(pair_data,hue='target', diag_kind='kde', plot_kws={'alpha':0.6})
    plt.suptitle('Pairplot of Features', y=1.02)
    plt.savefig('./results/illustrations/pairplot.png')
    plt.close()

      # Box Plots
    plt.figure(figsize=(16, rows * 4))
    for i, feature in enumerate(feature_columns):
        plt.subplot(rows, cols, i + 1)
        sns.boxplot(x=y, y=x[feature])
        plt.title(f'Box Plot of {feature} by Target')
        plt.tight_layout()
    plt.savefig('./results/illustrations/feature_boxplots.png')
    plt.close()

    #Scatter Plots 
    corr_matrix = x.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    highest_corrs = upper.stack().sort_values(ascending=False)[:10]  # Top 10 correlations
    
    plt.figure(figsize=(16, 20))
    for i, (idx, val) in enumerate(highest_corrs.items()):
        if i >= 10: 
            break
        plt.subplot(5, 2, i + 1)
        feature1, feature2 = idx
        sns.scatterplot(x=x[feature1], y=x[feature2], hue=y, alpha=0.6)
        plt.title(f'Correlation: {val:.2f}')
        plt.xlabel(feature1)
        plt.ylabel(feature2)
        plt.tight_layout()
    plt.savefig('./results/illustrations/feature_scatter_plots.png')
    plt.close()
    print("Data analysis completed.")

    return x, y
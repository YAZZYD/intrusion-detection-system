import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def analyaze( feature_df:pd.DataFrame):
    feature_columns = [col for col in feature_df.columns if not col.startswith(('file_name', 'attack_type_', 'attack_subtype_'))]
    x = feature_df[feature_columns]

    attack_columns = [col for col in feature_df.columns if col.startswith(('attack_type_', 'attack_subtype_'))]
    y = (feature_df[attack_columns].sum(axis=1)>0).astype(int)
    print("Dataset shape:", x.shape)
    print("\nFeature statistics:")
    print(x.describe())

    plt.figure(figsize=(14, 12))
    correlation_matrix = x.corr()
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm')
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig('./results/illustrations/feature_correlation.png')
    plt.close()
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def train_model(x,y):
    model = LogisticRegression(max_iter=1000,random_state=42)
    model.fit(x, y)
    print("Training Accuracy:", model.score(x, y))

    feature_importances = pd.DataFrame({
        "Feature": x.columns, 
        "Importance": np.abs(model.coef_[0])
    }).sort_values(by="Importance", ascending=False)

    print("\nTop 10 Important Features:")
    print(feature_importances.head(10))

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importances.head(15))
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig('./results/illustrations/feature_importance.png')
    plt.close()
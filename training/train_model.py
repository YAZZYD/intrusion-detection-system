from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def train_model(x:pd.DataFrame, y:pd.Series,columns:list) -> LogisticRegression:

    model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=16)
    model.fit(x, y)
    print(f"Training Accuracy:", model.score(x, y))

    feature_importances = pd.DataFrame({
        "Feature": columns, 
        "Importance": model.coef_[0]
    }).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importances.head(5))
    plt.title('Top 5 Feature Importances')
    plt.tight_layout()
    plt.savefig('./results/illustrations/feature_importance.png')
    plt.close()
    print("Feature importance plot saved as results/illustrations/feature_importance.png")

    print("✅ Model training complete.")
    return model

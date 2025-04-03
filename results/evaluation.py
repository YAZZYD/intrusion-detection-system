from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_model(y_true, y_pred):
    print("Model evaluation...")

    accuracy = accuracy_score(y_true, y_pred)
    print(f"Test Accuracy: {accuracy:.2f}")
    conf_matrix = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix,annot=True,fmt='d',cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig('results/illustrations/confusion_matrix.png')
    plt.close()
    print("Confusion matrix saved as results/illustrations/confusion_matrix.png")
    print("Evaluation complete.")
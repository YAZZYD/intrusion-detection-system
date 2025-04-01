import os
from preprocessing.process_captures import process_captures
from preprocessing.handlers.load_labels import load_labels
import warnings
warnings.filterwarnings('ignore')

def main():
    captured_dir = './dataset/captured'
    description = './dataset/description.csv'
    if not os.path.exists(captured_dir):
        print(f"dir '{captured_dir}' not found")
        return
    df=process_captures(captured_dir,description)
    print(df)


if __name__ == "__main__":
    main()
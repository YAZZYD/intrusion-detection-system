import os
import sys
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from preprocessing.process_captures import process_captures
from analyzing.analyze import analyze
from training.train_model import train_model
from scripts.terminal import select_attack
from results.evaluation import evaluate_model
import warnings
import traceback
warnings.filterwarnings('ignore')

def process_data():
    captured_dir = './dataset/captured'
    description = './dataset/description.csv'
    if not os.path.exists(captured_dir):
        print(f"dir '{captured_dir}' not found")
        return
    return process_captures(captured_dir,description)

def read_preprocessed_data():
    preprocessed_file = './dataset/preprocessed/preprocessed_data.csv'
    return pd.read_csv(preprocessed_file)

def save_processed_data(df:pd.DataFrame):
    preprocessed_file = './dataset/preprocessed/preprocessed_data.csv'
    df.to_csv(preprocessed_file, index=False)
    print(f"Processed data saved to {preprocessed_file}")

def main():
    parser = argparse.ArgumentParser(description="IDS (Intrusion Detection System)")
    parser.add_argument('--pre-processed',action='store_true',help="Use preprocessed data if available")
    args= parser.parse_args()
    df=None
    preprocessed_loaded=False
    if args.pre_processed:
        df=read_preprocessed_data()
        preprocessed_loaded=True
        print('Loaded preprocessed data.')
    else:
        select_attack()
        df= process_data()
        print("Data processed.")

    if df is not None:
        if not preprocessed_loaded:
            res = ''
            while res not in ['y', 'n']:
                res = input("Do you want to save the current processed data? (y/n): ").strip().lower()
                if res == 'y':
                    save_processed_data(df)
                    break
                elif res=='n':
                    print("Processed data not saved.")
                    break
                else:
                    print('(y/n) ?')
        x,y=analyze(df)
        
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,stratify=y, random_state=42)
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        
        model=train_model(x_train, y_train,columns=x.columns)
        
        y_pred=model.predict(x_test)
        
        evaluate_model(y_test, y_pred)
    else:
        print("No data to process.")
        return

if __name__ == "__main__":
  
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)
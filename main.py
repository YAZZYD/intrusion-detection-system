import os
import argparse
import pandas as pd
from preprocessing.process_captures import process_captures
from analyzing.analyze import analyze
import warnings
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
        analyze(df)
    
if __name__ == "__main__":
    main()
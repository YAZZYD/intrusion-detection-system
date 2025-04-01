import os
import argparse
import pandas as pd
from preprocessing.process_captures import process_captures
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

def main():
    parser = argparse.ArgumentParser(description="IDS (Intrusion Detection System)")
    parser.add_argument('--pre-processed',action='store_true',help="Use preprocessed data if available")
    args= parser.parse_args()
    df=None
    if args.pre_processed:
        df=read_preprocessed_data()
        print(df)
    else:
        df= process_data()
   

if __name__ == "__main__":
    main()
import os
import sys
import argparse
import joblib
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

def read_preprocessed_data(path:str=None)-> pd.DataFrame:
    preprocessed_file = './dataset/preprocessed/preprocessed_data.csv' if path is None else path
    return pd.read_csv(preprocessed_file)

def save_processed_data(df:pd.DataFrame):
    preprocessed_file = './dataset/preprocessed/preprocessed_data.csv'
    df.to_csv(preprocessed_file, index=False)
    print(f"Processed data saved to {preprocessed_file}")

def save_model(model):
    model_file = './model/model.pkl'
    joblib.dump(model, model_file)
    print(f"Model saved to {model_file}")

def interactive_question(quest:str,callback,*args):
    res = ''
    while res not in ['y', 'n']:
        res = input("Do you want to save the current processed data? (y/n): ").strip().lower()
        if res == 'y':
            callback(*args)
            return
        elif res=='n':
            print("Processed data not saved.")
            return
        else:
            print('(y/n) ?')

def main():
    parser = argparse.ArgumentParser(description="IDS (Intrusion Detection System)")
    parser.add_argument('--pre-processed',action='store_true',help="Use preprocessed data if available")
    parser.add_argument('--test-model',action='store_true',help="Test the model with preprocessed data")

    args= parser.parse_args()
    df=None
    preprocessed_loaded=False
    if args.pre_processed:
        df=read_preprocessed_data()
        preprocessed_loaded=True
        print('Loaded preprocessed data.')
    elif args.test_model:
        model_file = './model/model.pkl'
        print(f"Loading model from {model_file}...")
        if not os.path.exists(model_file):
            print(f"Model file '{model_file}' not found")
            return
        model = joblib.load(model_file)
        print('Loaded model.')
        df=read_preprocessed_data('./dataset/test/dataset.csv')
        df= df.drop(columns=['is_attack','attack_type','attack_subtype'],errors='ignore')
        predictions = model.predict(df)
        print("Predictions made.")
        for i, pred in enumerate(predictions):
            print(f"Packet {i} → {'Malicious' if pred == 1 else 'Harmless'}")
        print("Model testing completed.")
        return
    else:

        select_attack()
        df= process_data()
        print("Data processed.")

    if df is not None:
        if not preprocessed_loaded:
            interactive_question("Do you want to save the current processed data?",save_processed_data,df)
        x,y=analyze(df)
        
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,stratify=y, random_state=42)
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        
        model=train_model(x_train, y_train,columns=x.columns)
        
        y_pred=model.predict(x_test)
        
        evaluate_model(y_test, y_pred)
        interactive_question("Do you want to save the current model?",save_model,model)
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
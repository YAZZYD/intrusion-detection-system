import os
import json
import pandas as pd
from tqdm import tqdm
from preprocessing.handlers.extract_features import extract_features
from preprocessing.handlers.load_labels import load_labels
from preprocessing.handlers.match_labels import match_labels
from cleaning.clean_data import clean_data

def get_selected_attack():
    try:
        with open('info.json', 'r') as json_file:
            data = json.load(json_file)
            attack_type = data.get("attack_type")
            attack_subtype = data.get("attack_subtype")
            return attack_type, attack_subtype
    except FileNotFoundError:
        print("info.json file not found.")
        return None, None
    except json.JSONDecodeError:
        print("Error decoding JSON from info.json.")
        return None, None

def process_captures(data_dir: str, desc_csv: str) -> pd.DataFrame:
    labels_df = load_labels(desc_csv)
    features = []

    files = [f for f in os.listdir(data_dir) if f.endswith('.pcap')]
    
    for filename in tqdm(files, desc="Processing data", unit="file"):
        file_path = os.path.join(data_dir, filename)
        attack_info = match_labels(filename, labels_df)
        df = extract_features(file_path)
        df['file_name'] = filename
        attack_type, attack_subtype = get_selected_attack()
       
        if not attack_subtype and not attack_type:
            raise ValueError("Attack type and subtype not selected.")

        if attack_info:
            df['attack_type'] = attack_info['attack_type'] 
            df['attack_subtype'] = attack_info['attack_subtype']
            df['is_attack'] = int(attack_type == attack_info['attack_type'] and attack_subtype == attack_info['attack_subtype'])
        else:
            df['attack_type'] = ['Normal']
            df['attack_subtype'] = ['None']
            df['is_attack'] = 0

        features.append(df)
    
    all_features_df = pd.concat(features, ignore_index=True)
    return clean_data(all_features_df)

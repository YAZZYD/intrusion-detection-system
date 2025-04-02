import os
import pandas as pd 
from preprocessing.handlers.extract_features import extract_features
from preprocessing.handlers.load_labels import load_labels
from preprocessing.handlers.match_labels import match_labels
from preprocessing.handlers.encode_attack_info import encode_attack_info
from cleaning.clean_data import clean_data
def process_captures(data_dir:str,desc_csv:str)->pd.DataFrame:
    labels_df= load_labels(desc_csv)
    features=[]
    for filename in os.listdir(data_dir):
        if filename.endswith('.pcap'):
            file_path = os.path.join(data_dir,filename)
            attack_info = match_labels(filename,labels_df)
            df=extract_features(file_path)
            df['file_name'] = filename
            if(attack_info):
                attack_types = '|'.join(attack_info['attack_type']) if attack_info['attack_type'] else 'Normal'
                attack_subtypes = '|'.join(attack_info['attack_subtype']) if attack_info['attack_subtype'] else 'None'
                df['attack_type'] = attack_types
                df['attack_subtype'] = attack_subtypes
            df=encode_attack_info(df)
            features.append(df)
        all_features_df=pd.concat(features, ignore_index=True)
        return clean_data(all_features_df)
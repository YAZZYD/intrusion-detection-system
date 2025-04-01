import os
import pandas as pd 
from preprocessing.handlers.extract_features import extract_features
from preprocessing.handlers.load_labels import load_labels
from preprocessing.handlers.match_labels import match_labels

def process_captures(data_dir,desc_csv):
    labels_df= load_labels(desc_csv)
    features=[]
    for filename in os.listdir(data_dir):
        if filename.endswith('.pcap'):
            file_path = os.path.join(data_dir,filename)
            attack_info = match_labels(filename,labels_df)
            # features+=extract_features(file_path)
    return pd.DataFrame(features)
import pandas as pd

def load_labels(desc:str)->pd.DataFrame:
    column_names = ['id', 'file_name', 'created_at', 'file_size_kb', 'target_device', 
                    'attack_type', 'attack_subtype', 'filter_expr', 'packet_count', 'attack_packet_count']
    labels_df = pd.read_csv(desc,skiprows=2)
    labels_df.columns=column_names
    
    labels_df['file_name'] = labels_df['file_name'].str.strip()
    labels_df['target_device'] = labels_df['target_device'].str.strip()
    labels_df['attack_type'] = labels_df['attack_type'].str.strip()
    labels_df['attack_subtype'] = labels_df['attack_subtype'].str.strip()
    
    labels_df['file_size_kb'] = pd.to_numeric(labels_df['file_size_kb'], errors='coerce')
    labels_df['packet_count'] = pd.to_numeric(labels_df['packet_count'], errors='coerce')
    labels_df['attack_packet_count'] = pd.to_numeric(labels_df['attack_packet_count'], errors='coerce')
    
    labels_df['created_at'] = pd.to_datetime(labels_df['created_at'], errors='coerce')
    
    return labels_df
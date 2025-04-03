import pandas as pd
def match_labels(file_name:str,labels_df:pd.DataFrame)->dict[str,any]:
    matching_labels= labels_df[labels_df['file_name'] == file_name]
    if matching_labels.empty:
        print(f"No labels found for {file_name}")
        return None
    try:
        attack_info = {
            'file_name': file_name,
            'attack_type': matching_labels['attack_type'].dropna().iloc[0],
            'attack_subtype': matching_labels['attack_subtype'].dropna().iloc[0],
            'filters': matching_labels['filter_expr'].dropna().iloc[0]
        } 

    except KeyError as err:
        print(f"invalid key {err}")
    
    return attack_info
def match_labels(file_name,labels_df):
    matching_labels= labels_df[labels_df['file_name'] == file_name]
    if matching_labels.empty:
        print(f"No labels found for {file_name}")
        return None
    try:
        attack_info={
            'file_name':file_name,
            'attack_type': matching_labels['attack_type'].dropna().unique().tolist(),
            'attack_subtype':matching_labels['attack_subtype'].dropna().unique().tolist(),
            'filters':matching_labels['filter_expr'].dropna().tolist()
        }
    except KeyError as err:
        print(f"invalid key {err}")
    
    return attack_info
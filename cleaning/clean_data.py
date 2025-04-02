import pandas as pd

def clean_data(all_features_df:pd.DataFrame)->pd.DataFrame:
    print("Cleaning data...")
    exclude_columns = ['flow_id', 'src_ip', 'dst_ip', 'file_name']
    selected_feature_columns = [col for col in all_features_df.columns if col not in exclude_columns]

    processed_features_df = all_features_df[selected_feature_columns]
    for col in processed_features_df.select_dtypes(include=['object']).columns:
        if col == 'protocol':
            processed_features_df[col] = processed_features_df[col].map({'TCP':0,'UDP':1})
        else:
            processed_features_df[col] = pd.factorize(processed_features_df[col])[0]
    processed_features_df= processed_features_df.fillna(0)
    print(processed_features_df.dtypes)
    return  processed_features_df
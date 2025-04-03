from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

def encode(col: str, df: pd.DataFrame) -> pd.DataFrame:
    if not df[col].apply(lambda x: isinstance(x, (list, set, tuple))).all():
        df[col] = df[col].apply(lambda x: x.split('|') if isinstance(x, str) and '|' in x and pd.notna(x) 
                               else ([x.strip()] if isinstance(x, str) and pd.notna(x) 
                                    else ([x] if pd.notna(x) else [])))
    
    mlb = MultiLabelBinarizer()
    encoded_df = pd.DataFrame(
        mlb.fit_transform(df[col]),
        columns=[f"{col}_{c}" for c in mlb.classes_],
        index=df.index
    )
    
    result_df = pd.concat([df, encoded_df], axis=1)
    result_df = result_df.drop(columns=[col])
    return result_df

def encode_attack_info(df: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    
    if 'attack_type' in result_df.columns:
        result_df = encode('attack_type', result_df)
    if 'attack_subtype' in result_df.columns:
        result_df = encode('attack_subtype', result_df)
    
    return result_df
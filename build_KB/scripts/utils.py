import pandas as pd
import math

def med_data_clean(df):
    df['Claps'] = pd.to_numeric(df['Claps'],errors='coerce',downcast='integer')

    # q c clap

    avg_claps = df['Claps'].mean()
    max_claps = df['Claps'].max()
    min_claps = df['Claps'].min()
    threshould_claps = math.ceil((min_claps + max_claps)/2.0)

    df = df.loc[df['Claps']>=threshould_claps]
    
    # q c comment

    # avg_comments = df['Comment'].mean()
    # max_comments = df['Comment'].max()
    # min_comments = df['Comment'].min()
    # threshould_comments = math.ceil((min_comments + max_comments)/2.0)

    # df = df.loc[df['Comment']>=threshould_comments]
    
        # remove empty entries


    df = df.dropna(how='any')
    
    
    df = df.drop_duplicates(subset=['Title'],keep=False)
    df = df.drop_duplicates(subset=['url'],keep=False)

    # reset index properly 

    df = df.reset_index(drop=True)

    return df
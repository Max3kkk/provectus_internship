import os
import pandas as pd

res_df = pd.DataFrame()
for filename in sorted(os.listdir('src-data')):
    if filename.endswith('.csv'):
        user_id = filename[:-4]
        df = pd.read_csv(os.path.join("src-data", filename))
        df.insert(0, 'user_id', user_id)
        df['img_path'] = f'src-data/{user_id}.jpg'
        df = df.set_index('user_id')
        res_df = res_df.append(df)

res_df.to_csv("processed_data/output.csv")

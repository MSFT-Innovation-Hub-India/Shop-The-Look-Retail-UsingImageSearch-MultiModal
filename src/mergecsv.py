import pandas as pd
file1 = '/home/yohanb/shop-the-look-retail/src/dataset.csv'
file2 = '/home/yohanb/shop-the-look-retail/src/merged1234.csv'
output_path = '/home/yohanb/shop-the-look-retail/src/merged1234.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

merged_df = pd.merge(df1, df2[['img', 'caption']], on = 'img', how = 'left')

merged_df.to_csv('remerged.csv', index = False)
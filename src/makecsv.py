import pandas as pd
import csv
import generate_captions

csv_file_path = '/home/yohanb/shop-the-look-retail/small_dataset.csv'
output_path = '/home/yohanb/shop-the-look-retail/output.csv'

df = pd.read_csv(csv_file_path)

required_columns = ['id', 'img', 'p_attributes']
data_frame = df[required_columns]

column_values = [value for value in df['img']]
attributes_values = [value for value in df['p_attributes']]


with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'img', 'caption'])
    
    for idx, (img, attributes) in enumerate(zip(column_values, attributes_values)):
        caption = generate_captions.gen_caption(img, attributes)
        writer.writerow([idx, img, caption])
    
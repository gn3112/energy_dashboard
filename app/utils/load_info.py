import json
import pandas as pd
import os

def load_info():
    base_path = os.getcwd()

    path_sensors = os.path.join(base_path, 'app/assets/sensors_list.txt')
    path_tags = os.path.join(base_path, 'app/assets/tag_list.csv')

    with open(path_sensors, 'r', encoding="utf-8-sig") as f:
        sensors_info = json.load(f)
    
    tags = pd.read_csv(path_tags).to_dict(orient='records')
    
    return sensors_info["sensors_info"], tags
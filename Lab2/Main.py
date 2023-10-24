import pandas as pd
import requests
from datetime import datetime
import os
from spyre import server
import matplotlib.pyplot as plt
import seaborn as sns

dict_of_areas= {1:"Вінницька",
    2:"Волинська",
    3:"Дніпропетровська",
    4:"Донецька",
    5:"Житомирська",
    6:"Закарпатська",
    7:"Запорізька",
    8:"Івано-Франківська",
    9:"Київська",
    10:"Кіровоградська",
    11:"Луганська",
    12:"Львівська",
    13:"Миколаївська",
    14:"Одеська",
    15:"Полтавська",
    16:"Рівненська",
    17:"Сумська",
    18:"Тернопольска",
    19:"Харківська",
    20:"Херсонська",
    21:"Хмельницька",
    22:"Черкаська",
    23:"Чернігівська",
    24:"Чернівецька",
    25:"Крим",
    26:"Київ",
    27:"Севастополь"}

def download_data():
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for i in range(1, 28):
        url = (f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2023&type=Mean')
        response = requests.get(url)
        text = response.content.decode()
        clean_text = text.replace("b'", "")
        clean_text = clean_text.replace("'", "")
        clean_text = clean_text.replace(",  from 1982 to 2023,", "  from 1982 to 2023")
        clean_text = clean_text.replace(",\n", "\n")
        clean_text = clean_text.replace("</pre></tt>", "")
        clean_text = clean_text.replace("<tt><pre>1982", "1982")
        clean_text = clean_text.replace("<br>", "")
        clean_text = clean_text.replace("weeklyfor", "weekly for")
        clean_text = clean_text.replace(", SMN", ",SMN")
        clean_text = clean_text.replace(", VHI", ",VHI")
        clean_text = clean_text.encode()
        filename = os.path.join(data_dir, f'vhi_data_province_{i}_{time}.csv')
        with open(filename, 'wb') as file:
            file.write(clean_text)


def read_vhi_files(directory):
    vhi_data = pd.DataFrame()

    # Отримуємо список файлів у заданій директорії
    files = os.listdir(directory)

    for file in files:
        if file.startswith('vhi_data_province'):
            # Зчитуємо файл у фрейм pandas
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path, index_col=None, header=1)
            df = df.drop(df.loc[df['VHI'] == -1].index)
            province_id = int(file.split('_')[3])
            df.insert(0, 'area', province_id)
            vhi_data = pd.concat([vhi_data, df], ignore_index=True)
    dict_for_transfer = {
        1: 22,
        2: 24,
        3: 23,
        4: 25,
        5: 3,
        6: 4,
        7: 8,
        8: 19,
        9: 20,
        10: 21,
        11: 9,
        12: 26,
        13: 10,
        14: 11,
        15: 12,
        16: 13,
        17: 14,
        18: 15,
        19: 16,
        20: 27,
        21: 17,
        22: 18,
        23: 6,
        24: 1,
        25: 2,
        26: 7,
        27: 5

    }
    vhi_data["area"].replace(dict_for_transfer, inplace=True)
    vhi_data.sort_values(by=['area', 'year', 'week'], ascending=True, inplace=True)
    vhi_data = vhi_data.reset_index(drop=True)
    return vhi_data

#download_data()
#vhi_data = read_vhi_files(r'data')
class StockExample(server.App):
    title = 'NOAA data vizualization'

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Вибрати дані',
            "options": [{'label': "VCI", "value": 'VCI'},
                        {'label': "TCI", "value": 'TCI'},
                        {'label': "VHI", "value": 'VHI'}],
            "key": 'ticker',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Адміністративна одиниця',
            "options": [
                {'label': "Вінницька", "value": "1"},
                {'label': "Волинська", "value":  "2"},
                {'label': "Дніпропетровська", "value": "3"},
                {'label': "Донецька", "value": "4"},
                {'label': "Житомирська", "value": "5"},
                {'label': "Закарпатська", "value": "6"},
                {'label': "Запорізька", "value": "7"},
                {'label': "Івано-Франківська", "value": "8"},
                {'label': "Київська", "value": "9"},
                {'label': "Кіровоградська", "value": "10"},
                {'label': "Луганська", "value": "11"},
                {'label': "Львівська", "value": "12"},
                {'label': "Миколаївська", "value": "13"},
                {'label': "Одеська", "value": "14"},
                {'label': "Полтавська", "value": "15"},
                {'label': "Рівненська", "value": "16"},
                {'label': "Сумська", "value": "17"},
                {'label': "Тернопольска", "value": "18"},
                {'label': "Харківська", "value": "19"},
                {'label': "Херсонська", "value": "20"},
                {'label': "Хмельницька", "value": "21"},
                {'label': "Черкаська", "value": "22"},
                {'label': "Чернігівська", "value": "23"},
                {'label': "Чернівецька", "value": "24"},
                {'label': "Крим", "value": "25"},
                {'label': "Київ", "value": "26"},
                {'label': "Севастополь", "value": "27"},
            ],
            "key": 'selected_region',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": "Week range",
            "value": "1-48",
            "key": "wrange",
            "action_id": "update_data"

        },
        {
            "type": 'text',
            "label": "Year range",
            "value": "1983-2023",
            "key": "rrange",
            "action_id": "update_data"

        },
        {
            "type": 'text',
            "label": "xticks step",
            "value": "1",
            "key": "step",
            "action_id": "update_data"
        },

    ]
    controls = [{"type": "hidden",
                 "id": "update_data"}]
    tabs = ["Table", "Plot"]
    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True},
               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}
               ]

    def getData(self, params):
        ticker = params['ticker']
        selected_region = params['selected_region']
        wrange = params['wrange']
        rrange = params['rrange']
        start_year = rrange.split('-')[0]
        end_year = rrange.split('-')[1]
        start_week = wrange.split('-')[0]
        end_week = wrange.split('-')[1]
        df = pd.read_csv(f'data/vhi_data_province_{selected_region}_2023-10-20_00-53-14.csv', index_col=False, header=1, skiprows=0)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df = df[(df['year'] >= int(start_year)) & (df['year'] <= int(end_year)) & (df['week'] >= int(start_week)) & (df['week'] <= int(end_week))][['year', 'week', str(ticker)]]
        df['year:week'] = df['year'].astype(str) + ':' + df['week'].astype(str)
        return df

    def getPlot(self, params):
        df = self.getData(params)
        plt.figure(figsize=(16, 6))
        #plt.legend()
        img = sns.lineplot(data=df, x='year:week', y=f'{params["ticker"]}', marker="o", markersize=5)
        plt.xticks(range(0, len(df), int(params['step'])))
        plt.xticks(rotation=55)
        img.set_title('Plot1')
        return img


app = StockExample()
app.launch(port=9099)
"""
df = pd.read_csv(f'data/vhi_data_province_1_2023-10-20_00-53-14.csv', index_col=False, header=1, skiprows=0)
df = df.drop(df.loc[df['VHI'] == -1].index)
start_year = 2020
end_year = 2022
start_week = 20
end_week = 30
print(df)
df["year-week"] = df['year'].astype(str) +"-"+ df["week"].astype(str)
print(df)
print(df[(df['year'] >= start_year) & (df['year'] <= end_year) & (df['week'] >= start_week) & (df['week'] <= end_week)])
"""

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
dict_of_areas_with_0 = dict_of_areas.copy()
dict_of_areas_with_0[0] = 'Нічого'
dict_of_areas_with_0 = dict(sorted(dict_of_areas_with_0.items()))
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

class StockExample(server.App):
    title = 'NOAA data vizualization'

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Вибрати дані(1)',
            "options": [{'label': "VCI", "value": 'VCI'},
                        {'label': "TCI", "value": 'TCI'},
                        {'label': "VHI", "value": 'VHI'}],
            "key": 'ticker1',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Вибрати дані(2)',
            "options": [{'label': "Нічого", "value": '0'},
                        {'label': "VCI", "value": 'VCI'},
                        {'label': "TCI", "value": 'TCI'},
                        {'label': "VHI", "value": 'VHI'}],
            "key": 'ticker2',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Вибрати дані(3)',
            "options": [{'label': "Нічого", "value": '0'},
                        {'label': "VCI", "value": 'VCI'},
                        {'label': "TCI", "value": 'TCI'},
                        {'label': "VHI", "value": 'VHI'}],
            "key": 'ticker3',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Адміністративна одиниця(1)',
            "options": [{'label': dict_of_areas[i], 'value': i} for i in dict_of_areas],
            "key": 'selected_region',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Адміністративна одиниця(2) для порівняння',
            "options": [{'label': dict_of_areas_with_0[i], 'value': i} for i in dict_of_areas_with_0],
            "key": 'selected_region_2',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Адміністративна одиниця(3) для порівняння',
            "options": [{'label': dict_of_areas_with_0[i], 'value': i} for i in dict_of_areas_with_0],
            "key": 'selected_region_3',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": "Week range",
            "value": "1-52",
            "key": "wrange",
            "action_id": "update_data"

        },
        {
            "type": 'text',
            "label": "Year range",
            "value": "1983-2023",
            "key": "yrange",
            "action_id": "update_data"

        },
        {
            "type": 'text',
            "label": "xticks step",
            "value": "27",
            "key": "step",
            "action_id": "update_data"
        },

    ]
    controls = [{"type": "hidden",
                 "id": "update_data"}]
    tabs = ["Table1", "Table2", "Table3", "Plot"]
    outputs = [{"type": "table",
                "id": "data1",
                "control_id": "update_data",
                "tab": "Table1",
                "on_page_load": True},
               {"type": "table",
                "id": "data2",
                "control_id": "update_data",
                "tab": "Table2"},
               {"type": "table",
                "id": "data3",
                "control_id": "update_data",
                "tab": "Table3"},
               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}
               ]

    def data1(self, params):
        ticker1 = params['ticker1']
        ticker2 = params['ticker2']
        ticker3 = params['ticker3']
        selected_region = params['selected_region']
        wrange = params['wrange']
        yrange = params['yrange']

        start_year = yrange.split('-')[0]
        end_year = yrange.split('-')[1]
        start_week = wrange.split('-')[0]
        end_week = wrange.split('-')[1]

        df = pd.read_csv(f'data/vhi_data_province_{selected_region}_2023-10-20_00-53-14.csv',
                        index_col=False, header=1, skiprows=0)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df = df[(df['year'] >= int(start_year)) & (df['year'] <= int(end_year)) & (df['week'] >= int(start_week)) & (
                    df['week'] <= int(end_week))]


        ticker2_checked = None
        ticker3_checked = None
        if ticker2 != '0':
            ticker2_checked = str(ticker2)
        if ticker3 != '0':
            ticker3_checked = str(ticker3)
        list_to_show = ['year', 'week', str(ticker1)]
        if ticker2_checked and ticker2_checked != ticker1:
            list_to_show.append(ticker2_checked)
        if ticker3_checked and ticker3_checked != ticker1:
            list_to_show.append(ticker3_checked)
        if list_to_show[-1] == list_to_show[-2]:
            list_to_show.pop(-1)

        df = df[list_to_show]
        return df
    def data2(self,params):
        ticker1 = params['ticker1']
        ticker2 = params['ticker2']
        ticker3 = params['ticker3']
        selected_region_2 = params['selected_region_2']
        wrange = params['wrange']
        yrange = params['yrange']

        start_year = yrange.split('-')[0]
        end_year = yrange.split('-')[1]
        start_week = wrange.split('-')[0]
        end_week = wrange.split('-')[1]

        df_2 = pd.read_csv(f'data/vhi_data_province_{selected_region_2}_2023-10-20_00-53-14.csv',
                         index_col=False, header=1, skiprows=0)
        df_2 = df_2.drop(df_2.loc[df_2['VHI'] == -1].index)
        df_2 = df_2[(df_2['year'] >= int(start_year)) & (df_2['year'] <= int(end_year)) & (df_2['week'] >= int(start_week)) & (
                df_2['week'] <= int(end_week))]

        ticker2_checked = None
        ticker3_checked = None
        if ticker2 != '0':
            ticker2_checked = str(ticker2)
        if ticker3 != '0':
            ticker3_checked = str(ticker3)
        list_to_show = ['year', 'week', str(ticker1)]
        if ticker2_checked and ticker2_checked != ticker1:
            list_to_show.append(ticker2_checked)
        if ticker3_checked and ticker3_checked != ticker1:
            list_to_show.append(ticker3_checked)
        if list_to_show[-1] == list_to_show[-2]:
            list_to_show.pop(-1)

        df_2 = df_2[list_to_show]
        return df_2
    def data3(self, params):
        ticker1 = params['ticker1']
        ticker2 = params['ticker2']
        ticker3 = params['ticker3']
        selected_region_3 = params['selected_region_3']
        wrange = params['wrange']
        yrange = params['yrange']

        start_year = yrange.split('-')[0]
        end_year = yrange.split('-')[1]
        start_week = wrange.split('-')[0]
        end_week = wrange.split('-')[1]

        df_3 = pd.read_csv(f'data/vhi_data_province_{selected_region_3}_2023-10-20_00-53-14.csv',
                           index_col=False, header=1, skiprows=0)
        df_3 = df_3.drop(df_3.loc[df_3['VHI'] == -1].index)
        df_3 = df_3[(df_3['year'] >= int(start_year)) & (df_3['year'] <= int(end_year)) & (df_3['week'] >= int(start_week)) & (
                    df_3['week'] <= int(end_week))]

        ticker2_checked = None
        ticker3_checked = None
        if ticker2 != '0':
            ticker2_checked = str(ticker2)
        if ticker3 != '0':
            ticker3_checked = str(ticker3)
        list_to_show = ['year', 'week', str(ticker1)]
        if ticker2_checked and ticker2_checked != ticker1:
            list_to_show.append(ticker2_checked)
        if ticker3_checked and ticker3_checked != ticker1:
            list_to_show.append(ticker3_checked)
        if list_to_show[-1] == list_to_show[-2]:
            list_to_show.pop(-1)

        df_3 = df_3[list_to_show]
        return df_3
    def plot(self, params):
        df = self.data1(params)
        df['year:week'] = df['year'].astype(str) + ':' + df['week'].astype(str)
        try:
            df_2 = self.data2(params)
            df_2['year:week'] = df_2['year'].astype(str) + ':' + df_2['week'].astype(str)
        except: print("В другій вибрано нічого")
        try:
            df_3 = self.data3(params)
            df_3['year:week'] = df_3['year'].astype(str) + ':' + df_3['week'].astype(str)
        except: print("В третій вибрано нічого")

        plt.figure(figsize=(16, 6))
        img = sns.lineplot(data=df, x='year:week', y=f'{params["ticker1"]}',
                           label=f'{params["ticker1"]+dict_of_areas[int(params["selected_region"])]}',
                           marker="o", markersize=3)

        if params["selected_region_2"] != '0':
            sns.lineplot(data=df_2, x='year:week', y=f'{params["ticker1"]}',
                         label=f'{params["ticker1"]+dict_of_areas[int(params["selected_region_2"])]}', marker="o", markersize=3, ax=img)
        if params["selected_region_3"] != "0":
            sns.lineplot(data=df_3, x='year:week', y=f'{params["ticker1"]}',
                         label=f'{params["ticker1"]+dict_of_areas[int(params["selected_region_3"])]}', marker="o", markersize=3, ax=img)

        if str(params["ticker2"]) != "0":
            sns.lineplot(data=df, x='year:week', y=f'{params["ticker2"]}',
                         label=f'{params["ticker2"]+dict_of_areas[int(params["selected_region"])]}', marker="o", markersize=3, ax=img)
            if str(params["selected_region_2"]) != "0":
                sns.lineplot(data=df_2, x='year:week', y=f'{params["ticker2"]}',
                             label=f'{params["ticker2"]+dict_of_areas[int(params["selected_region_2"])]}', marker="o", markersize=3, ax=img)
            if str(params["selected_region_3"]) != "0":
                sns.lineplot(data=df_3, x='year:week', y=f'{params["ticker2"]}',
                             label=f'{params["ticker2"]+dict_of_areas[int(params["selected_region_3"])]}', marker="o", markersize=3, ax=img)
        if str(params["ticker3"]) != "0":
            sns.lineplot(data=df, x='year:week', y=f'{params["ticker3"]}',
                         label=f'{params["ticker3"]+dict_of_areas[int(params["selected_region"])]}', marker="o", markersize=3, ax=img)
            if str(params["selected_region_3"]) != "0":
                sns.lineplot(data=df_3, x='year:week', y=f'{params["ticker3"]}',
                             label=f'{params["ticker3"]+dict_of_areas[int(params["selected_region_2"])]}', marker="o", markersize=3, ax=img)
            if str(params["selected_region_2"]) != "0":
                sns.lineplot(data=df_2, x='year:week', y=f'{params["ticker3"]}',
                             label=f'{params["ticker3"]+dict_of_areas[int(params["selected_region_3"])]}', marker="o", markersize=3, ax=img)

        plt.xlabel('Year:Week')  # Label for the x-axis
        plt.ylabel('Value')  # Label for the y-axis
        plt.xticks(range(0, len(df), int(params['step'])))
        plt.xticks(rotation=55)
        plt.legend()
        return img


app = StockExample()
app.launch(port=9105)
"""
df = pd.read_csv(f'data/vhi_data_province_1_2023-10-20_00-53-14.csv', index_col=False, header=1, skiprows=0)
df_2 = pd.read_csv(f'data/vhi_data_province_2_2023-10-20_00-53-14.csv', index_col=False, header=1, skiprows=0)
df = df.drop(df.loc[df['VHI'] == -1].index)
df_2 = df_2.drop(df_2.loc[df_2['VHI'] == -1].index)

start_year = 2020
end_year = 2022
start_week = 20
end_week = 30

df["year:week"] = df['year'].astype(str) + ":" + df["week"].astype(str)
df_2["year:week"] = df_2['year'].astype(str) + ":" + df_2["week"].astype(str)

df = df[(df['year'] >= start_year) & (df['year'] <= end_year) & (df['week'] >= start_week) & (df['week'] <= end_week)]
df_2 = df_2[(df_2['year'] >= start_year) & (df_2['year'] <= end_year) & (df_2['week'] >= start_week) & (df_2['week'] <= end_week)]

plt.figure(figsize=(16, 6))
sns.lineplot(data=df, x='year:week', y="VHI", label="Province 1", marker="o", markersize=5)
sns.lineplot(data=df_2, x='year:week', y="VHI", label="Province 2", marker="o", markersize=5)
plt.xticks(range(0, len(df), 27))
plt.xticks(rotation=55)
plt.title('Plot1')
plt.legend()
plt.show()"""




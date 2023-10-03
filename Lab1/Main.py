import pandas as pd
import requests
from datetime import datetime
import os

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
def change_index(index):
    if index == 1: return 22
    elif index == 2: return 24
    elif index == 3: return 23
    elif index == 4: return 25
    elif index == 5: return 3
    elif index == 6: return 4
    elif index == 7: return 8
    elif index == 8: return 19
    elif index == 9: return 20
    elif index == 10: return 21
    elif index == 11: return 9
    elif index == 12: return 26
    elif index == 13: return 10
    elif index == 14: return 11
    elif index == 15: return 12
    elif index == 16: return 13
    elif index == 17: return 14
    elif index == 18: return 15
    elif index == 19: return 16
    elif index == 20: return 27
    elif index == 21: return 17
    elif index == 22: return 18
    elif index == 23: return 6
    elif index == 24: return 1
    elif index == 25: return 2
    elif index == 26: return 7
    elif index == 27: return 5
# Функція для завантаження файлу VHI-індексу
def download_vhi_file(province_id):

    # Формування URL для завантаження
    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2023&type=Mean'

    # Виконання запиту GET на сервер NOAA
    response = requests.get(url)

    # Перевірка статусу запиту
    if response.status_code == 200:

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

        # Формування імені файлу з датою та часом завантаження
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'vhi_data_province_{change_index(province_id)}_{timestamp}.csv'

        # Збереження файлу на диск
        with open(filename, 'wb') as file:
            file.write(clean_text)

        print(f'Файл для області {province_id} збережено як {filename}')
    else:
        print(f'Помилка при завантаженні файлу для області {province_id}')


# Завантаження файлів для всіх областей
def download():
    for i in range(1, 28):
        download_vhi_file(i)

# Функція для зчитування файлів VHI-індексу у фрейм pandas
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
            #print(list(df.columns.values))
            #print(df[:2])
            vhi_data = pd.concat([vhi_data, df], ignore_index=True)
    return vhi_data


#Функція для видалення файлів з директорії
def delete_files(dir_path):
    # Задайте префікс, з яким повинні починатися файли для видалення
    prefix_to_delete = 'vhi_data_province'

    # Отримайте список файлів у директорії
    files = os.listdir(directory_path)

    # Переберіть файли і видаліть ті, які починаються з вказаного префікса
    for file in files:
        if file.startswith(prefix_to_delete):
            file_path = os.path.join(directory_path, file)
            os.remove(file_path)
            print(f'Файл {file_path} видалено.')

# Задайте шлях до директорії, де збережені файли VHI-індексу
directory_path = r'D:\semestr_3\Prog3\Lab1'

vhi_data_combined = read_vhi_files(directory_path)

def vhi_extremes_by_year(df, area_id, year):
    area_data = df[(df['area'] == area_id) & (df['year'] == year)]
    min_vhi = area_data['VHI'].min()
    max_vhi = area_data['VHI'].max()
    return min_vhi, max_vhi
def vhi_by_area(df, area_id):
    area_data = df[df['area'] == area_id]['VHI']
    return area_data
def extreme_drought_years(df, area_id, percentage):
    extreme_drought_years = df[(df['area'] == area_id) & (df['VHI'] <= percentage)]['year']
    return extreme_drought_years
print(vhi_extremes_by_year(vhi_data_combined, 1, 2006))
print("__")
print(vhi_by_area(vhi_data_combined, 1))
print("__")
for i in range(1, 28):
    area_name = dict_of_areas.get(i)
    extreme_years = extreme_drought_years(vhi_data_combined, i, 15)
    print(f"Область: {area_name}")
    print(f"Роки екстремальних посух: {list(extreme_years)}")

# delete_files(directory_path)
# download()
print(vhi_data_combined.head())

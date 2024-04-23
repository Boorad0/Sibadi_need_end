import json
import requests
import sqlite3
def base():
    atnist=["ЭУб","ГСУб","АПб","ЗОСб","БПб","ТЛб","ОДб","СМб","НСб","ДНГб","АТТ","ПТС","ПОб","АПб","АТб"]
    isy = ["АСб","ПИб","БИб","БИ","УКб","ЦЭб","ЛОГб","Эб","ЛОГб"]
    adpgs = ["АРХб","ПГСб","ИСб","ТГВб","АДб","ИДб","МТб","СУЗ","СЭМ","ГЕОб","СУЗ"]
    data_base = sqlite3.connect('groups1.db', check_same_thread = False)
    sql = data_base.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS ALL_groups(
    groupe TEXT,
    id INT,
    kurs INT,
    UNIQUE ("groupe") ON CONFLICT IGNORE,
    UNIQUE ("id") ON CONFLICT IGNORE
    
    )
        """)
    sql.execute("""CREATE TABLE IF NOT EXISTS atnist(
    groupe TEXT,
    id INT,
    kurs INT,
    UNIQUE ("groupe") ON CONFLICT IGNORE,
    UNIQUE ("id") ON CONFLICT IGNORE
    
    )
    """)
    sql.execute("""CREATE TABLE IF NOT EXISTS isy(
    groupe TEXT,
    id INT,
    kurs INT,
    UNIQUE ("groupe") ON CONFLICT IGNORE,
    UNIQUE ("id") ON CONFLICT IGNORE
    
    )
    """)
    sql.execute("""CREATE TABLE IF NOT EXISTS adpgs(
    groupe TEXT,
    id INT,
    kurs INT,
    UNIQUE ("groupe") ON CONFLICT IGNORE,
    UNIQUE ("id") ON CONFLICT IGNORE
    
    )
    """)
    data_base.commit()
    url2 = requests.get("https://umu.sibadi.org/api/raspGrouplist?year=2023-2024")
    groups = json.loads(url2.text)
    for item in groups['data']:

        sql.execute(f"INSERT INTO ALL_groups VALUES ('{item['name']}', '{int(item['id'])}', '{int(item['kurs'])}')")
        if item['name'][0:3] in isy or item['name'][0:4] in isy:
            sql.execute(f"INSERT INTO isy VALUES ('{item['name']}', '{int(item['id'])}', '{int(item['kurs'])}')")
        if item['name'][0:3] in atnist or item['name'][0:4] in atnist or item['name'][0:2] in atnist:
            sql.execute(f"INSERT INTO atnist VALUES ('{item['name']}', '{int(item['id'])}', '{int(item['kurs'])}')")
        if item['name'][0:3] in adpgs or item['name'][0:4] in adpgs:

            sql.execute(f"INSERT INTO adpgs VALUES ('{item['name']}', '{int(item['id'])}', '{int(item['kurs'])}')")

    data_base.commit()



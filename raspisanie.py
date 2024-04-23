import requests
import json#13689#2024-3-4
def raspisanie(id_groupe, data):
    test = f"https://umu.sibadi.org/api/Rasp?idGroup={id_groupe}&sdate={data}"
    url1 = requests.get(test)
    raspisanie = json.loads(url1.text)
    proverka =""
    msg = ""
    raspi = []
    for item in raspisanie['data']['rasp']:
        if item['день_недели'] != proverka:
            raspi.append(msg)
            msg = ""
            msg += "\n" + item['дата'][:10] + "\n" + item['день_недели'] + "\n"
            proverka = item['день_недели']
        if "пр. Элективные курсы по физической культуре" in item["дисциплина"]:
            msg += item['начало'] + " " + item['конец'] + " " + "пр. Физическая культура" + " " + item['преподаватель'] + " " + \
                  "\n"
        else: msg += item['начало'] + " " + item['конец'] + " " + item["дисциплина"] + " " + item['преподаватель'] + " " + \
                item['аудитория'] + "\n"
    raspi.append(msg)
    raspi.pop(0)
    return raspi
if __name__ == "__main__":
    raspisanie()


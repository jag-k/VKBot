import urllib.request
from datetime import date
from xml.etree import ElementTree as ET
import time as t
from normal_case import normal_case


def course():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    currency = ET.parse(urllib.request.urlopen(url))
    res = []
    for line in currency.findall('Valute'):
        var = {"id": line.get("ID")}
        for key in map(lambda x: x.tag, line):
            var[normal_case(key)] = line.find(key).text
            key = normal_case(key)
            if key in ['nominal', 'num_code']:
                var[key] = int(var[key])
            elif key == 'value':
                var[key] = float(var[key].replace(',', '.'))
        res.append(var)
    today = date.today()
    time = map(int, t.ctime().split()[3].split(':'))
    time_data = {'day': today.day, 'month': today.month, 'year': today.year,
                 'hour': time.__next__(), 'minutes': time.__next__(), 'seconds': time.__next__()}

    return {'time': time_data, 'course': res}


if __name__ == "__main__":
    from pprint import pprint
    pprint(course())

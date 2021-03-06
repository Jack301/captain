# -*- coding:utf-8 -*-
import sys
import random
import os
import json
import copy
import bs4
import requests
import constants
reload(sys)
sys.setdefaultencoding('utf8')


def get_random_motto():
    all_motto_dict = dict()
    random_motto_type = random.choice(constants.MOTTO_TYPE)

    res = dict()
    if os.path.isfile(constants.MOTTO_PATH):
        with open(constants.MOTTO_PATH) as f:
            all_motto_dict = json.load(f)
        if random_motto_type in all_motto_dict:
            res = random.choice(all_motto_dict[random_motto_type].values())
        else:
            motto_dict = grab_motto(random_motto_type)
            res = random.choice(motto_dict[random_motto_type].values())
            all_motto_dict[random_motto_type] = motto_dict.values()[0]
            with open(constants.MOTTO_PATH, 'w') as f:
                f.write(json.dumps(all_motto_dict, indent=2))
    else:
        motto_dict = grab_motto(random_motto_type)
        res = random.choice(motto_dict[random_motto_type].values())
        with open(constants.MOTTO_PATH, 'w') as f:
            f.write(json.dumps(motto_dict, indent=2))
    return res


def grab_motto(specific_motto_type):
    url = 'http://www.mottos.info/' + specific_motto_type
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'lxml')

    raw_motto = soup.find('div', attrs={'class': 'entry-content'})
    motto_lst = []
    for i, s in enumerate(raw_motto.stripped_strings):
        if i == 0 or i == len(list(raw_motto.stripped_strings)) - 1:
            continue
        s = s.replace('“', '"')
        s = s.replace('”', '"')
        motto_lst.append(s.encode('utf-8'))
    tmp_dict = dict()
    d = dict()
    for i, s in enumerate(motto_lst):
        if s.startswith('"'):
            d.clear()
            d['type'] = specific_motto_type
            d['motto'] = s
        else:
            d['author'] = s
            tmp_dict[d['motto']] = copy.deepcopy(d)
    res_dict = dict()
    res_dict[specific_motto_type] = tmp_dict
    return res_dict


# res = get_random_motto()
# print(res)

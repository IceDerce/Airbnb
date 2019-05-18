import requests
from bs4 import BeautifulSoup
import json
import re
import time

list=[]
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400'
}

for m in range(0,36,18):
    url='https://www.airbnb.cn/api/v2/explore_tabs?version=1.4.5&satori_version=1.1.3&_format=for_explore_search_web&experiences_per_grid=20&items_per_grid=18&guidebooks_per_grid=20&auto_ib=true&fetch_filters=true&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&luxury_pre_launch=false&query_understanding_enabled=false&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&client_session_id=c1dc98aa-5de6-422b-99eb-3ed164e09dc6&metadata_only=false&is_standard_search=true&refinement_paths[]=/homes&selected_tab_id=home_tab&click_referer=t:SEE_ALL|sid:29141e94-7a48-4a7e-a794-0b53c13c272d|st:MAGAZINE_HOMES&title_type=MAGAZINE_HOMES&allow_override[]=&s_tag=PAJAldIi&section_offset=6&items_offset={0}&screen_size=large&query=%E8%8B%8F%E5%B7%9E%E5%8C%97%E7%AB%99&_intents=p1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=zh'.format(m)

    url_json=requests.get(url,headers=headers).text
    url_json=json.loads(url_json)
    url_list=url_json['explore_tabs'][0]['home_tab_metadata']['remarketing_ids']
    for url in url_list:
        list.append(url)

for id in list:
    url='https://www.airbnb.cn/rooms/{0}?location=%E8%8B%8F%E5%B7%9E%E5%8C%97%E7%AB%99&s=PAJAldIi&guests=1&adults=1'.format(id)
    html=requests.get(url,headers=headers).text
    key=re.findall(r"key:(.+?)}",html.replace('&quot;',''))[0]
    id=re.findall(r"rooms/(\d+)?",url)[0]
    nameurl='https://www.airbnb.cn/api/v2/pdp_listing_details/{0}?_format=for_rooms_show&adults=1&key={1}&'.format(id,key)
    name = requests.get(nameurl, headers=headers).text
    name = json.loads(name)
    shopname=name['pdp_listing_detail']['name']
    for number in range(0,100,7):
        try:
            url2='https://www.airbnb.cn/api/v2/reviews?key={0}&currency=CNY&locale=zh&listing_id={1}&role=guest&_format=for_p3&_limit=7&_offset={2}&_order=language_country'.format(key,id,number)
            time.sleep(2)
            html2=requests.get(url2,headers=headers).text
            html2=json.loads(html2)
            try:
                comment_list=html2['reviews']
            except:
                time.sleep(2)
                comment_list = html2['reviews']
            for m in comment_list:
                information={}
                information['shop'] = shopname
                information['username']=m['reviewer']['first_name']
                information['comment']=m['comments']
                information['time']=m['localized_date']
                print(information)
        except:
            break
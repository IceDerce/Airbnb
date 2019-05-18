import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib import parse
from random import randint


class Airbnb:

    def __init__(self,keyword):
        self.keyword = parse.quote(keyword)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400',
        }

    #获取所有房源
    def get_house(self):
        house_list = []
        Flag = True
        page = 0  #初始页
        error_number = 0 # 错误记录
        while Flag:
            #抓包筛选参数 构造api
            url = 'https://zh.airbnb.com/api/v2/explore_tabs?currency=CNY&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&items_offset={1}&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&query={0}&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes'.format(self.keyword,page)
            try:
                url_text = requests.get(url, headers=self.headers).text
                url_json = json.loads(url_text)
                total_sections = url_json['explore_tabs'][0]['sections']
                total_lists = [n for m in total_sections if m['result_type'] == 'listings' for n in m['listings']]
                #获取当页所有房源
                for m in total_lists:
                    house = {}
                    house['price'] = m['pricing_quote']['rate']['amount'] #房屋价钱
                    house['bathroom'] = m['listing']['bathrooms']  #卫生间数量
                    house['bedroom'] = m['listing']['bedrooms']  # 卧室数量
                    house['beds'] = m['listing']['beds']  # 床数量
                    house['url'] = 'https://zh.airbnb.com/rooms/'+str(m['listing']['id'])  #房源url
                    house['guests'] = m['listing']['guest_label']  # 最大入驻房客数量
                    house['city'] = m['listing']['localized_city']  # 房源地区
                    house['lat'] = m['listing']['lat']  # 房源纬度
                    house['lng'] = m['listing']['lng']  # 房源经度
                    house['name'] = m['listing']['name']  # 房源名称标题
                    house['star'] = m['listing']['star_rating']  # 房源评分星级
                    # house['name'] = m['listing']['name']  # 房源名称标题
                    house['master'] = 'https://zh.airbnb.com/users/show/'+str(m['listing']['user']['id'])  # 房东个人主页
                    house['name'] = [n['name'] for n in m['listing']['preview_tags']]  # 房源标签
                    house['serive'] = m['listing']['preview_amenity_names']  # 房源提供
                    house_list.append(house)
                    print(house)
                #切换页
                if url_json['explore_tabs'][0]['pagination_metadata']['has_next_page'] == False:
                    Flag = False
                else:
                    page = url_json['explore_tabs'][0]['pagination_metadata']['items_offset']
                    time.sleep(randint(1,2))
                error_number = 0 #成功访问一次便置零
            except:
                print('error:%s'% url)
                error_number = +1
                if error_number > 5: #连续request 5次错误 终止程序 避免死循环
                    break

    #获取房源下详细评论  待更新
    def get_comment(self):
        pass


if __name__ == '__main__':
    keyword = '上海'
    Airbnb(keyword).get_house()



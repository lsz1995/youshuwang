import  requests
from lxml import etree
import csv
import json
import re
import time
headers = {
        #'Host': 'book.douban.com',
        #'Referer': 'https://www.douban.com/accounts/login?redir=https%3A%2F%2Fbook.douban.com%2Ftag%2F%25E5%25B0%258F%25E8%25AF%25B4%3Fstart%3D0%26type%3DT',
        #'Upgrade-Insecure-Requests': '1',
        'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        
}

proxie = {
     'http' : 'http://122.193.14.102:80'
}
datas=[]
def  get_more_7(url):
    response = requests.get(url,headers=headers)
    selector = etree.HTML(response.text)
    infos = selector.xpath('//table[@class="table"]/tr')[1:]
    for info in infos:
        category=info.xpath('td[1]/text()')[0]
        title=info.xpath('td[1]/a/text()')[0]
        author=info.xpath('td[2]/text()')[0]
        score=info.xpath('td[3]/text()')[0]
        if float(score)>=7:
            data={
                'category':category,
                'title':title,
                'author':author,
                'score':score,
            }
            datas.append(data)
def paixu_up(item,**args):
    total = len(item)
    for i in range(total-1):
        for j in range(total-i-1):
            if item[j]['score']>item[j+1]['score']:
                item[j],item[j+1]= item[j+1],item[j]
    return item
def paixu_down(item,**args):
    total = len(item)-1
    for i in range(total):
        for j in range(total-i):
            if item[j]['score']<item[j+1]['score']:
                item[j],item[j+1]= item[j+1],item[j]
    return item



def toscv(item,**args):#将小说信息储存城csv格式
    with open('more_than_7.csv', 'w', encoding='utf-8',newline='') as f:
                    total=len(item)
                    writer = csv.writer(f)
                    writer.writerow(['total',total ])
                    writer.writerow(['category', 'title', 'author', 'score'])
                    for i in range(total):
                        writer.writerow([item[i]['category'], item[i]['title'], item[i]['author'], item[i]['score']])


'''
def douban():#豆瓣小说


        for i in range(0,2000,20):
            url='https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T'.format(str(i))

            #url='https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=0&type=T'

            response = requests.get(url,headers=headers,proxies = proxie)

            selector = etree.HTML(response.text)

            infos = selector.xpath('//ul[@class="subject-list"]/li')
            for info in infos:
                title =info.xpath('div[2]/h2/a/@title')[0]
                score=info.xpath('div[2]/div/span[2]/text()')[0]
                comment =info.xpath('div[2]/div/span[3]/text()')[0].strip()
                comment =re.findall('\d+',comment)[0]
                if float(score)>=8.5 and int(comment)>5000:
                    data={
                        'title':title,
                        'score':score,
                        'commen':comment
                    }
                    datas.append(data)
            time.sleep(0.5)
        paixu_down(datas)
        with open('douban_more9.csv', 'w', encoding='utf-8',newline='') as f:
                    total=len(datas)
                    writer = csv.writer(f)
                    writer.writerow(['total',len(datas) ])
                    writer.writerow([ '书名', '评分', '评论人数'])
                    for i in range(len(datas)):
                        writer.writerow([datas[i]['title'], datas[i]['score'], datas[i]['commen']])


'''








if __name__ == '__main__':
    #龙空7分以上
    srar_url = 'http://www.yousuu.com/topshow/digest?mobile=yes&page=1'
    for i in range(16):
        url = 'http://www.yousuu.com/topshow/digest?mobile=yes&page={}'.format(str(i+1))
        get_more_7(url)
    paixu_down(datas)
    toscv(datas)



    #douban()


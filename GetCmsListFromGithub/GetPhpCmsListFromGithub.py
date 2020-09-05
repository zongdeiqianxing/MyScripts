#Crawl the CMS list on github

#coding:utf8
import requests,re,time,csv
from lxml import etree

cookies={'user_session':'q1HhOw6GQ6imoXgfHa0sy6rqcK4IdbqMyhT3PNieaoTBoPtC'}
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0)',}
#url='https://github.com/search?l=PHP&p=4&q=cms&type=Repositories'

data=[]
for num in range(1,101):
    url='https://github.com/search?l=PHP&p='+str(num)+'&q=cms&type=Repositories'
    print(url)
    result=requests.get(url=url,headers=headers,cookies=cookies)
    #print(result.text)
    
    tree = etree.HTML(result.text)
    xpath=tree.xpath(r'//ul[@class="repo-list"]/li')
    
    if xpath is None:
        write_md()
        exit("error-_-")
        
        
    for i in xpath:
        i=etree.HTML(etree.tostring(i).decode('utf-8'))
        starNum=''.join(i.xpath(r'//a[@class="muted-link"]/text()'))
        starNum=''.join(re.findall('\S',starNum))
        if 'k' in starNum:
            starNum = int(float(starNum[:-1])*1000)
        #print(starNum)
        
        title=''.join(i.xpath(r'//div[@class="f4 text-normal"]/a//text()'))             
        print(title)
        title=''.join(re.findall('\S',title))
        
        description =''.join(i.xpath(r'//p[@class="mb-1"]//text()')).strip('\r\n')
        description=''.join(re.findall('\S',description))
        description = description.replace('<em>','')
        description = description.replace('</em>','')
        
        href = 'https://github.com/' + title
        
        print(str(starNum),title,description)
        data.append([str(starNum),title,description,href])
    time.sleep(3)
        

with open('result.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
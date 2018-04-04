from lxml import html
import requests
from lxml import etree
import random
import sqlite3
import psycopg2


def pages_counter(div_res):
    page_count = int(div_res) // 30 + 1
    if int(div_res)%30 < 10:
        page_count = page_count-1
    return page_count

def sights_counter(url):
    index_page = requests.get(url)
    tree_index = html.fromstring(index_page.content)
    div = tree_index.xpath('//div[@class="clear-filters-container"]')
    div_res = div[0].attrib['data-obj-count']
    return div_res

def get_information(url):
    pages = []
    tree = []
    names = []
    adress = []
    brief_description = []
    refers = []
    sight_description  = []
    tree_descr = []
    sight_schedule = []
    sight_descr = []
    coordinates = []
    longitude = []
    latitude = []
    images = []
        
    sight_count = sights_counter(url)
    page_count = pages_counter(sight_count)
    for page_num in range(page_count):
        pages.append(requests.get((url+'?page='+str(page_num+1))))
        
    print(page_count)
    print(int(sight_count))
    
    for i in range(page_count):
        tree.append(html.fromstring(pages[i].content))
        names.append(tree[i].xpath('//a[@class="post-title-link"]//span/text()'))    
        for j, n in enumerate(names[i]):
            refers.append((tree[i].xpath('//h2[@class="post-title"]//a'))[j].attrib['href'])
            images.append((tree[i].xpath('//div[@class="post-image-src"]'))[j].attrib['data-echo-background'])
    
    for r in range(int(sight_count)):
        sight_description.append(requests.get('https://kudago.com'+refers[r]))
        tree_descr.append(html.fromstring(sight_description[r].content))      
        adress.append(tree_descr[r].xpath('//div[@class="post-big-address"]/text()'))
        brief_description.append(tree_descr[r].xpath('//div[@id="item-description"]//p/text()'))      
        sight_schedule.append(tree_descr[r].xpath('//div[@class="schedule-item"]/text()'))
        sight_descr.append(tree_descr[r].xpath('//div[@class="post-big-text"][@id="item-body-text"]//p/text()'))
        coordinates.append((tree_descr[r].xpath('//div[@class="ya-taxi-widget"]'))[0].attrib['data-point-b'])
        
    
    for i in coordinates:
        longitude.append(str(i).replace(',',' ').split()[0])
        latitude.append(str(i).replace(',',' ').split()[1])

    for i in range(int(sight_count)):
        if sight_schedule[i] == []:
            sight_schedule.remove([])
            sight_schedule.insert(i, ['none'])
        
    data1 = []
    data = []
    buff =()
    k =1
    l=1
    for i in range(page_count):
        for j, n in enumerate(names[i]):
            data1.append(l)
            data1.append(names[i][j])
            data1.append(adress[k-1][0].strip())
            data1.append("Москва")
            data1.append(brief_description[k-1][0])
            data1.append(sight_schedule[k-1][0])
            data1.append(latitude[k-1])
            data1.append(longitude[k-1])
            data1.append('https://kudago.com/'+images[j])
            buff = tuple(data1)
            data.append(buff)
            data1 = []
            k+=1
            l+=1        
    #db_creation_sglite(data)
    #db_creation_postgresql(data); 

def db_creation_sqlite(data):            
    conn = sqlite3.connect("D:\\test_parsing\\Overall.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO sight VALUES (?,?,?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()
    
def db_creation_postgresql(data):
    try:
        conn = psycopg2.connect("dbname='fn1181_2018' user='student' host='195.19.32.74' password='bmstu' port='5432'")
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.executemany("""INSERT INTO sight VALUES (%s, %s,%s, %s, %s, %s,%s, %s, %s)""", data);
    conn.commit()
    cur.close()
    conn.close()   


get_information('https://kudago.com/ufa/attractions/')   
#get_information('https://kudago.com/krasnoyarsk/attractions/') 
#get_information('https://kudago.com/kzn/attractions/')  
#get_information('https://kudago.com/nsk/attractions/')   
#get_information('https://kudago.com/ekb/attractions/')   
#get_information('https://kudago.com/nnv/attractions/')   
#get_information('https://kudago.com/smr/attractions/')    
#get_information('https://kudago.com/krd/attractions/')    
#get_information('https://kudago.com/sochi/attractions/')   
#get_information('https://kudago.com/spb/attractions/')    
#get_information('https://kudago.com/msk/attractions/') 






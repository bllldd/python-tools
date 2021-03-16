import requests
from lxml import etree
import os
import time
import aiohttp
import asyncio
def dom():
    start = time.time()
    print("声明：所有图片来源于彼岸桌面（http://www.netbian.com/）")
    print("下载的类别有：日历、动漫、风景、美女、游戏、影视、动态、唯美、设计、可爱、汽车、花卉、")
    print("动物、节日、人物、美食、水果、建筑、体育、军事、非主流、其他、王者荣耀、护眼")
    print("4K风景、4K美女、4K游戏、4K动漫、4K影视、4K明星、4K汽车、4K动物、4K人物、4K美食、4K宗教、4K背景")
    lei_xing = input("请输入要下载的类别的全拼：")
    page = input("请输入页码（页码过大可能没有数据，每页20张图片,第一页请直接回车）：")
    if page:
        page = "_" + page
    url = "http://www.netbian.com/"+lei_xing+"/index"+page+".htm"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
    data_html = requests.get(url=url,headers=header).text
    tree = etree.HTML(data_html)
    img_list = tree.xpath("//div[@class='list']/ul/li/a")
    if not os.path.exists(lei_xing):
        os.mkdir(lei_xing)
    for img in img_list:
        img_a = 'http://www.netbian.com/' + img.xpath('./@href')[0]
        img_html = requests.get(url=img_a,headers=header).text
        img_tree = etree.HTML(img_html)
        img_img = img_tree.xpath('//*[@id="main"]/div[3]/div/p/a/img')
        img_name = img_img[0].xpath("./@alt")
        img_name[0] = img_name[0].encode('iso-8859-1').decode('gbk')   # 不知道其编码是什么的情况下先编码后解码，可以解决乱码情况
        src = img_img[0].xpath("./@src")
        print("正在下载色图：%s" %(img_name[0]))
        img_data = requests.get(url=src[0],headers=header).content
        f = open(lei_xing+"/"+img_name[0]+".jpg","wb")
        f.write(img_data)
        f.close()
    return start
start = dom()
end = time.time()
print("总耗时：%ss" % (str(end - start)))
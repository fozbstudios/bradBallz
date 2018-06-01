# -*- coding: utf-8 -*-
import scrapy
class BrooksbaseballSpider(scrapy.Spider):
    name = 'brooksbaseball'
    allowed_domains = ['http://www.brooksbaseball.net']
    lURLs = []
    rURLs = []
    bURLs = []
    checkNamesArr=[]
    def __init__(self):
        for line in open('namesToCheckAgainst.csv', 'r').readlines():
            curID=line.split(',')[0]
            lURL='http://www.brooksbaseball.net/h_tabs.php?player='+curID+'&balls=-1&strikes=-1&b_hand=L&time=month&minmax=ci&var=ra&s_type=2&gFilt=&startDate=&endDate='
            rURL='http://www.brooksbaseball.net/h_tabs.php?player='+curID+'&balls=-1&strikes=-1&b_hand=R&time=month&minmax=ci&var=ra&s_type=2&gFilt=&startDate=&endDate='
            bURL='http://www.brooksbaseball.net/h_tabs.php?player='+curID+'&balls=-1&strikes=-1&b_hand=-1&time=month&minmax=ci&var=ra&s_type=2&gFilt=&startDate=&endDate='
            self.lURLs.append(lURL)
            self.rURLs.append(rURL)
            self.bURLs.append(bURL)
            self.checkNamesArr.append(line.split(',')[1].rstrip('\n'))
    def start_requests(self):
        for lLink,rLink,bLink,name in zip(self.lURLs,self.rURLs,self.bURLs,self.checkNamesArr):
            yield scrapy.Request(url=lLink, meta={'checkName':name,'fNameNoExt':'leftOut'},callback=self.parse)
            yield scrapy.Request(url=rLink, meta={'checkName':name,'fNameNoExt':'rightOut'},callback=self.parse)
            yield scrapy.Request(url=bLink, meta={'checkName':name,'fNameNoExt':'bothOut'},callback=self.parse)
    def parse(self, response):
        print(response.url)
        print(response.meta['checkName'])

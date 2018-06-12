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
        header = []
        header+=response.meta['checkName']
        header+='!NEW_PLAYER!'
        parsedTitle=response.xpath('//title/text()').extract_first()[13:]#strips 'Player Card: ' from page tile leavingf only name
        header+=parsedTitle
        header+=getHeaderList(response)
        
        with open(response.meta['fNameNoExt']+".csv", "a",encoding='iso-8859-1') as out: #append
            out.write(','.join(header)+'\n')
            for row in getTableData(response):
                out.write(',,,'+','.join(row)+'\n') #,,, for 3 empyty csv cells to nest propperly under header

        # print(response.url)
        # print(response.meta['checkName'])
    def getHeaderList(response):
        """returns list containing text of stats tablr <th> elems"""
        return response.xpath('//table/thead//th/text()').extract()

    def getTableData(response):
        """returns 2d list containing text of stats tablr <td> elems"""
        ret =[]
        for row in response.xpath('//table/thead//tr')[1:]: #skip table header
            ret+=row.xpath('.//b/text()').extract()+row.xpath('.//td/text()').extract()
        return ret;

# -*- coding: utf-8 -*-
import scrapy
from bradBallz.items import BradballzItem
class BrooksbaseballSpider(scrapy.Spider):
    name = 'brooksbaseball'
    allowed_domains = ['brooksbaseball.net']
    lURLs = []
    rURLs = []
    bURLs = []
    checkNamesArr=[]
    def __init__(self, inFile=None):
        for line in open('namesToCheckAgainst.csv', 'r').readlines():
            curID=line.split(',')[0]
            lURL='http://www.brooksbaseball.net/h_tabs.php?player='+curID+'&balls=-1&strikes=-1&b_hand=L&time=month&minmax=ci&var=ra&s_type=2&gFilt=&startDate=&endDate='
            rURL='http://www.brooksbaseball.net/h_tabs.php?player='+curID+'&balls=-1&strikes=-1&b_hand=R&time=month&minmax=ci&var=ra&s_type=2&gFilt=&startDate=&endDate='
            bURL='http://www.brooksbaseball.net/h_tabs.php?player='+curID+'&balls=-1&strikes=-1&b_hand=-1&time=month&minmax=ci&var=ra&s_type=2&gFilt=&startDate=&endDate='
            self.lURLs.append(lURL)
            self.rURLs.append(rURL)
            self.bURLs.append(bURL)
            self.checkNamesArr.append(line.split(',')[1].rstrip('\n'))

            #clear all outfiles
            fileToClear=open('leftOut.csv','w',encoding='iso-8859-1')
            fileToClear.write('')
            fileToClear.close()
            fileToClear=open('rightOut.csv','w',encoding='iso-8859-1')
            fileToClear.write('')
            fileToClear.close()
            fileToClear=open('bothOut.csv','w',encoding='iso-8859-1')
            fileToClear.write('')
            fileToClear.close()
    def start_requests(self):
        for lLink,rLink,bLink,name in zip(self.lURLs,self.rURLs,self.bURLs,self.checkNamesArr):
            yield scrapy.Request(url=lLink, meta={'checkName':name,'fNameNoExt':'leftOut'},callback=self.parse)
            yield scrapy.Request(url=rLink, meta={'checkName':name,'fNameNoExt':'rightOut'},callback=self.parse)
            yield scrapy.Request(url=bLink, meta={'checkName':name,'fNameNoExt':'bothOut'},callback=self.parse)
    def getHeaderList(self, response):
        """returns list containing text of stats tablr <th> elems"""
        return response.xpath('//table/thead//th/text()').extract()

    def getTableData(self, response):
        """returns 2d list containing text of stats tablr <td> elems"""
        ret =[]
        for row in response.xpath('//table/thead//tr')[1:]: #skip table header
            retRow=[]
            retRow.append(row.xpath('.//*/font/text()|.//*/b/text()').extract_first())
            retRow+=[st.replace(',','') for st in row.xpath('.//td/text()').extract()]
            ret.append(retRow)
            # print(ret)
        return ret;
    def parse(self, response):
        item = BradballzItem()
        header = []
        header.append('!NEW_PLAYER!')
        header.append(response.url)
        item['url'] = response.url
        item['fileName'] = response.meta['fNameNoExt']+".csv"
        item['lineDict'] = []
        # header.append(response.meta['checkName'])
        parsedTitle=response.xpath('//title/text()').extract_first()[13:]#strips 'Player Card: ' from page tile leavingf only name
        header.append(parsedTitle)
        header+=self.getHeaderList(response)

        item['lineDict'].append(','.join(header)+'\n')
        for row in self.getTableData(response):
            # out.write(',,'+','.join(row)+'\n') #,,, for 3 empyty csv cells to nest propperly under header
            item['lineDict'].append(',,,'+','.join(row)+'\n') #,,, for 3 empyty csv cells to nest propperly under header
        item['lineDict'].append(',,,\n') #to sperate entries
        yield item
        # print(response.url)
        # print(response.meta['checkName'])

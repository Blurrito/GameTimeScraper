from os.path import abspath
from header import readAverageTimes

import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

class CorrectionSpider(scrapy.Spider):
    name = 'CorrectionSpider'

    def correctData(self, response, index):
        readAverageTimes(self, response)

        for headerTime in self.headerTimes:
            if headerTime.categoryName == headerTimesDataframe.loc[index]['name']:
                headerTimesDataframe.at[index, 'value'] = headerTime.value
                break

    def start_requests(self):
        for index in range(0, len(headerTimesDataframe), 1):
            if 'Min' in headerTimesDataframe.loc[index]['value']:
                url = f'https://howlongtobeat.com/game/{headerTimesDataframe.loc[index]["gameId"]} '
                headers = {'User-Agent': 'PostmanRuntime/7.37.3'}
                yield scrapy.Request(url=url, headers=headers, callback=self.correctData, cb_kwargs=dict(index=index))

headerTimesDataframe = pd.read_csv(abspath('./dataframes v1 backup/AverageTimes.csv'))

process = CrawlerProcess()
process.crawl(CorrectionSpider)
process.start()

headerTimesDataframe.to_csv(abspath('./dataframes/AverageTimes.csv'), index=False)
from os.path import abspath
from category import readGameplayCategories

import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

class CorrectionSpider(scrapy.Spider):
    name = 'CorrectionSpider'

    def correctData(self, response, index):
        readGameplayCategories(self, response)

        for category in self.categories:
            if category.name == headerTimesDataframe.loc[index]['categoryName']:
                for playstyle in category.playStyles:
                    if playstyle.name == headerTimesDataframe.loc[index]['playstyleName']:
                        headerTimesDataframe.at[index, 'average'] = playstyle.average
                        headerTimesDataframe.at[index, 'median'] = playstyle.median
                        headerTimesDataframe.at[index, 'fastest'] = playstyle.fastest
                        headerTimesDataframe.at[index, 'slowest'] = playstyle.slowest
                        return

    def start_requests(self):
        for index in range(0, len(headerTimesDataframe), 1):
            if ('Min' in headerTimesDataframe.loc[index]['average'] or
                'Min' in headerTimesDataframe.loc[index]['median'] or
                'Min' in headerTimesDataframe.loc[index]['fastest'] or
                'Min' in headerTimesDataframe.loc[index]['slowest']):
                url = f'https://howlongtobeat.com/game/{headerTimesDataframe.loc[index]["gameId"]} '
                headers = {'User-Agent': 'PostmanRuntime/7.37.3'}
                yield scrapy.Request(url=url, headers=headers, callback=self.correctData, cb_kwargs=dict(index=index))

headerTimesDataframe = pd.read_csv(abspath('./dataframes v1 backup/Categories.csv'))

process = CrawlerProcess()
process.crawl(CorrectionSpider)
process.start()

headerTimesDataframe.to_csv(abspath('./dataframes/Categories.csv'), index=False)
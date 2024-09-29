import os
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class Expansion():
    def __init__(self, tableRow, gameId):
        entryUrl = tableRow.xpath('./td')[0]
        self.name = entryUrl.xpath('./text()').get()
        self.gameId = gameId

        href = entryUrl.xpath('href').extract()
        if href == None:
            return

        splitHref = href.split('/')
        if len(splitHref) < 2:
            return

        self.id = int(splitHref[len(splitHref) - 1])
        self.polled = tableRow.xpath('./td/text()')[1].get()
        self.rated = tableRow.xpath('./td/text()')[2].get()
        self.main = tableRow.xpath('./td/text()')[3].get()
        self.side = tableRow.xpath('./td/text()')[4].get()
        self.complete = tableRow.xpath('./td/text()')[5].get()
        self.all = tableRow.xpath('./td/text()')[6].get()

class CategoryTimeGroup():
    def __init__(self, tableRow):
        self.name = tableRow.xpath('./td/text()')[0].get()
        self.polled = tableRow.xpath('./td/text()')[1].get()
        self.average = tableRow.xpath('./td/text()')[2].get()
        self.median = tableRow.xpath('./td/text()')[3].get()
        self.fastest = tableRow.xpath('./td/text()')[4].get()
        self.slowest = tableRow.xpath('./td/text()')[5].get()

    def print(self):
        print(f"Name: {self.name}\n"
              f"Poll count: {self.polled}\n"
              f"Average time: {self.average}\n"
              f"Median time: {self.median}\n"
              f"Fastest time: {self.fastest}\n"
              f"Slowest time: {self.slowest}\n")

class GameCategory():
    def __init__(self, table):
        self.name = table.xpath('./thead/tr/td/text()')[0].get()

        rows = table.xpath('./tbody/tr')
        self.timeGroups = []
        for row in rows:
            self.timeGroups.insert(len(self.timeGroups), CategoryTimeGroup(row))

    def print(self):
        print(f"\nName: {self.name}")
        for timeGroup in self.timeGroups:
            timeGroup.print()

class GameInfoSpider(scrapy.Spider):
    name = 'GameInfoSpider'
    gameCount = 157352

    def requestGame(self):
        for index in range(self.pageCount + 1):
            url = f'https://howlongtobeat.com/game/{index + 1}'
            yield scrapy.Request(url=url, callback=self.readGameData)


    def readGameData(self, response):

        # Get game ID
        url = response.request.url.split('/')
        gameId = int(url[len(url) - 1])

        # Get header times
        #header = response.css('div.GameStats_game_times__KHrRY')
        header = response.xpath('//div[contains(@class, "GameStats_game_times__KHrRY")]')
        headerTimes = header.css('li.GameStats_short__tSJ6I')
        main = headerTimes[0].xpath('./h5/text()').get()
        side = headerTimes[1].xpath('./h5/text()').get()
        complete = headerTimes[2].xpath('./h5/text()').get()
        all = headerTimes[3].xpath('./h5/text()').get()

        expansionTable = response.xpath('//div[contains(@class, "in scrollable scroll_blue back_primary shadow_box")]')
        expansions = []
        if len(expansionTable) > 0:
            tableRows = expansionTable[0].xpath('./table/tbody')
            for tableRow in tableRows:
                expansions.insert(len(expansions), Expansion(tableRow, gameId))

        tables = response.xpath('//table[contains(@class, "GameTimeTable_game_main_table__7uN3H")]')
        categories = []
        for table in tables:
            categories.insert(len(categories), GameCategory(table))

        print(f"main: {main}\nside: {side}\ncomplete: {complete}\nall: {all}\n")
        for category in categories:
            category.print()

    def  start_requests(self):
        url = 'https://howlongtobeat.com/game/68151'
        headers = {'User-Agent': 'PostmanRuntime/7.37.3'}
        yield scrapy.Request(url=url, headers=headers, callback=self.readGameData)

process = CrawlerProcess()
process.crawl(GameInfoSpider)
process.start()
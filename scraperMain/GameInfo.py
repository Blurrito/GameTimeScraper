import random
import time
from os.path import abspath

import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from game import Game

class GameInfoSpider(scrapy.Spider):
    name = 'GameInfoSpider'
    #gameCount = 157352
    gameCount = 100

    startIndex = 20000
    stopIndex = 20100

    def toCsv(self, game):
        csvData = game.toCsv()

        # Write main game information
        headersDataframe.loc[len(headersDataframe.index)] = csvData[0]

        # Write average times stored in the header to file
        for index in range(0, len(csvData[1])):
            headerTimesDataframe.loc[len(headerTimesDataframe.index)] = csvData[1][index]

        # Write game metadata to file
        for index in range(0, len(csvData[2])):
            metadataDataframe.loc[len(metadataDataframe.index)] = csvData[2][index]

        # Write release dates to file
        for index in range(0, len(csvData[3])):
            releaseDatesDataframe.loc[len(releaseDatesDataframe.index)] = csvData[3][index]

        # Write expansion information to file
        for index in range(0, len(csvData[4])):
            expansionsDataframe.loc[len(expansionsDataframe.index)] = csvData[4][index]

        # Write timed categories to file
        for index in range(0, len(csvData[5])):
            categoriesDataframe.loc[len(categoriesDataframe.index)] = csvData[5][index]

        # Write platform information to file
        for index in range(0, len(csvData[6])):
            platformsDataframe.loc[len(platformsDataframe.index)] = csvData[6][index]

    def scrapeData(self, response):
        # Validate record exists
        notFound = response.xpath('//div[@class="position: absolute;left: 50%;top: 50%;transform: translate(-50%, -50%);margin: 0 auto;max-width: 1300px;width: 100%;"]')
        if len(notFound) > 0:
            return

        game = Game(response)
        self.toCsv(game)

    def requestGame(self):
        for index in range(self.startIndex, self.stopIndex + 1, 1):
            # Create artificial delay to prevent spam
            delaySeconds = float(random.randrange(82, 246)) / 100
            time.sleep(delaySeconds)

            url = f'https://howlongtobeat.com/game/{index}'
            yield scrapy.Request(url=url, callback=self.scrapeData)

    def  start_requests(self):
        url = 'https://howlongtobeat.com/game/68151'
        # url = 'https://howlongtobeat.com/game/21286'
        headers = {'User-Agent': 'PostmanRuntime/7.37.3'}
        yield scrapy.Request(url=url, headers=headers, callback=self.scrapeData)

headersDataframe = pd.DataFrame(columns=['gameId', 'gameName', 'playCount', 'backlogCount', 'replayCount',
                                         'retiredPercentage', 'rating', 'completedCount'])
headerTimesDataframe = pd.DataFrame(columns=['gameId', 'name', 'value'])
metadataDataframe = pd.DataFrame(columns=['gameId', 'name', 'value'])
releaseDatesDataframe = pd.DataFrame(columns=['gameId', 'region', 'date'])
expansionsDataframe = pd.DataFrame(columns=['gameId', 'expansionId', 'name', 'polled', 'rated', 'main', 'side',
                                            'complete', 'all'])
categoriesDataframe = pd.DataFrame(columns=['gameId', 'categoryName', 'playstyleName', 'polled', 'average', 'median',
                                            'fastest', 'slowest'])
platformsDataframe = pd.DataFrame(columns=['gameId', 'name', 'polled', 'main', 'side', 'complete', 'fastest',
                                           'slowest'])

process = CrawlerProcess()
process.crawl(GameInfoSpider)
process.start()

headersDataframe.to_csv(abspath('./dataframes/Games.csv'), index=False)
headerTimesDataframe.to_csv(abspath('./dataframes/AverageTimes.csv'), index=False)
metadataDataframe.to_csv(abspath('./dataframes/Metadata.csv'), index=False)
releaseDatesDataframe.to_csv(abspath('./dataframes/ReleaseDates.csv'), index=False)
expansionsDataframe.to_csv(abspath('./dataframes/Expansions.csv'), index=False)
categoriesDataframe.to_csv(abspath('./dataframes/Categories.csv'), index=False)
platformsDataframe.to_csv(abspath('./dataframes/Platforms.csv'), index=False)
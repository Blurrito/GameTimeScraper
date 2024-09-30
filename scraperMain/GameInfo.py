import scrapy
from scrapy.crawler import CrawlerProcess

class Platform:
    def __init__(self, tableRow, gameId):
        self.gameId = gameId
        platformData = tableRow.xpath('./td')
        if len(platformData) < 7:
            return

        self.name = platformData[0].xpath('./text()').get()
        self.polled = platformData[1].xpath('./text()').get()
        self.main = platformData[2].xpath('./text()').get()
        self.side = platformData[3].xpath('./text()').get()
        self.complete = platformData[4].xpath('./text()').get()
        self.fastest = platformData[5].xpath('./text()').get()
        self.slowest = platformData[6].xpath('./text()').get()

    def print(self):
        print(f"Name: {self.name}\n"
              f"Poll count: {self.polled}\n"
              f"Main: {self.main}\n"
              f"Side: {self.side}\n"
              f"Complete: {self.complete}\n"
              f"Fastest: {self.fastest}\n"
              f"Slowest: {self.slowest}\n")


class Expansion:
    def __init__(self, tableRow, gameId):
        expansionData = tableRow.xpath('./td')
        pageUrl = expansionData[0].xpath('./a')
        self.name = pageUrl.xpath('./text()').get()
        self.gameId = gameId

        href = pageUrl.xpath('@href').get()
        if href is None:
            return

        splitHref = href.split('/')
        if len(splitHref) < 2:
            return

        self.id = int(splitHref[len(splitHref) - 1])
        self.polled = expansionData[1].xpath('./text()').get()
        self.rated = expansionData[2].xpath('./text()').get()
        self.main = expansionData[3].xpath('./text()').get()
        self.side = expansionData[4].xpath('./text()').get()
        self.complete = expansionData[5].xpath('./text()').get()
        self.all = expansionData[6].xpath('./text()').get()

    def print(self):
        print(f"Name: {self.name}\n"
              f"Poll count: {self.polled}\n"
              f"Rating: {self.rated}\n"
              f"Main: {self.main}\n"
              f"Side: {self.side}\n"
              f"Complete: {self.complete}\n"
              f"All: {self.all}\n")


class CategoryPlayStyle:
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


class GameCategory:
    def __init__(self, table):
        self.name = table.xpath('./thead/tr/td/text()')[0].get()

        rows = table.xpath('./tbody/tr')
        self.playStyles = []
        for row in rows:
            self.playStyles.append(CategoryPlayStyle(row))

    def print(self):
        print(f"\nName: {self.name}")
        for playStyle in self.playStyles:
            playStyle.print()


class ReleaseDate:
    def __init__(self, releaseDate, gameId):
        self.gameId = gameId
        self.region = releaseDate.xpath('/strong/text()').get()[:-1]
        self.date = releaseDate.xpath('./text()').get()

    def print(self):
        print(f"Region: {self.region}\nDate: {self.date}\n")


class GameInfoSpider(scrapy.Spider):
    name = 'GameInfoSpider'
    gameCount = 157352

    def readHeader(self, response):
        header = response.xpath('//div[contains(@class, "GameHeader_profile_header_game__CH56Y")]')
        headerComponents = header.xpath('./div')
        if len(headerComponents) == 0:
            return

        self.gameName = headerComponents[0].xpath('./text()').get()
        statistics = headerComponents[2].xpath('./div/ul/li')
        self.playCount = statistics[0].xpath('./text()').get().split(' ')[0]
        self.backlogCount = statistics[1].xpath('./text()').get().split(' ')[0]
        self.replayCount = statistics[2].xpath('./text()').get().split(' ')[0]
        self.retiredPercentage = statistics[3].xpath('./text()').get().split(' ')[0]
        self.rating = statistics[4].xpath('./text()').get().split(' ')[0]
        self.completedCount = statistics[5].xpath('./text()').get().split(' ')[0]

    def readMetadata(self, response):
        self.platforms = []
        self.genres = []
        self.developers = []
        self.publishers = []

        mediumSummaries = response.xpath('//div[contains(@class, "GameSummary_profile_info__HZFQu GameSummary_medium___r_ia")]')
        if len(mediumSummaries) < 4:
            return

        self.platforms = mediumSummaries[0].xpath('./text()').get().split(', ')
        self.genres = mediumSummaries[1].xpath('./text()').get().split(', ')
        self.developers = mediumSummaries[2].xpath('./text()').get().split(', ')
        self.publishers = mediumSummaries[3].xpath('./text()').get().split(', ')

        self.releaseDates = []
        smallSummaries = response.xpath('//div[contains(@class, "GameSummary_profile_info__HZFQu")]')
        if len(smallSummaries) < 1:
            return

        smallSummaries.pop(len(smallSummaries) - 1)
        for smallSummary in smallSummaries:
            self.releaseDates.append(ReleaseDate(smallSummary, self.gameId))

    def readPlatforms(self, response):
        self.platforms = []
        platformTable = response.xpath('//table[contains(@class, "GamePlatformTable_game_main_table__6o6MM")]')
        if len(platformTable) == 0:
            return

        tableRows = platformTable.xpath('./tbody/tr')
        if len(tableRows) == 0:
            return

        for tableRow in tableRows:
            self.platforms.append(Platform(tableRow, self.gameId))

    def readGameplayCategories(self, response):
        self.categories = []
        tables = response.xpath('//table[contains(@class, "GameTimeTable_game_main_table__7uN3H")]')
        for table in tables:
            self.categories.append(GameCategory(table))

    def readExpansions(self, response):
        self.expansions = []
        expansionTable = response.xpath('//div[contains(@class, "in scrollable scroll_blue back_primary shadow_box")]')
        if len(expansionTable) > 0:
            tableRows = expansionTable[0].xpath('./table/tbody/tr')
            for tableRow in tableRows:
                self.expansions.append(Expansion(tableRow, self.gameId))

    def readAverageTimes(self, response):
        timeHeader = response.xpath('//div[contains(@class, "GameStats_game_times__KHrRY")]')
        if len(timeHeader) == 0:
            return

        timeHeaderEntries = timeHeader.xpath('./ul/li')
        if len(timeHeaderEntries) >= 4:
            return

        self.main = timeHeaderEntries[0].xpath('./h5/text()').get()
        self.side = timeHeaderEntries[1].xpath('./h5/text()').get()
        self.complete = timeHeaderEntries[2].xpath('./h5/text()').get()
        self.all = timeHeaderEntries[3].xpath('./h5/text()').get()

    def requestGame(self):
        for index in range(self.pageCount + 1):
            url = f'https://howlongtobeat.com/game/{index + 1}'
            yield scrapy.Request(url=url, callback=self.readGameData)


    def readGameData(self, response):

        # Get game ID
        url = response.request.url.split('/')
        self.gameId = int(url[len(url) - 1])

        # Get header information
        self.readHeader(response)

        # Get al metadata
        self.readMetadata(response)

        # Get average times
        self.readAverageTimes(response)

        # Get expansions
        self.readExpansions(response)

        # Get gameplay categories
        self.readGameplayCategories(response)

        # Get platform information
        self.readPlatforms(response)

    def print(self):
        print(f"main: {self.main}\nside: {self.side}\ncomplete: {self.complete}\nall: {self.all}\n")
        for category in self.categories:
            category.print()

        print("\nExpansions:\n")
        for expansion in self.expansions:
            expansion.print()

    def  start_requests(self):
        url = 'https://howlongtobeat.com/game/68151'
        headers = {'User-Agent': 'PostmanRuntime/7.37.3'}
        yield scrapy.Request(url=url, headers=headers, callback=self.readGameData)

process = CrawlerProcess()
process.crawl(GameInfoSpider)
process.start()
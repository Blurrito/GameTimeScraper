from utilities import toTimestamp, toNumber

class Platform:
    def __init__(self, tableRow):
        platformData = tableRow.xpath('./td')
        if len(platformData) < 7:
            return

        self.name = platformData[0].xpath('./text()').get()
        self.polled = toNumber(self, platformData[1].xpath('./text()').get())
        self.main = toTimestamp(self, platformData[2].xpath('./text()').get())
        self.side = toTimestamp(self, platformData[3].xpath('./text()').get())
        self.complete = toTimestamp(self, platformData[4].xpath('./text()').get())
        self.fastest = toTimestamp(self, platformData[5].xpath('./text()').get())
        self.slowest = toTimestamp(self, platformData[6].xpath('./text()').get())

    def print(self):
        print(f"Name: {self.name}\n"
              f"Poll count: {self.polled}\n"
              f"Main: {self.main}\n"
              f"Side: {self.side}\n"
              f"Complete: {self.complete}\n"
              f"Fastest: {self.fastest}\n"
              f"Slowest: {self.slowest}\n")

    def toCsv(self, gameId):
        return [gameId, self.name, self.polled, self.main, self.side, self.complete, self.fastest, self.slowest]


def readPlatforms(self, response):
    self.platforms = []
    platformTable = response.xpath('//table[contains(@class, "GamePlatformTable_game_main_table__6o6MM")]')
    if len(platformTable) == 0:
        return

    tableRows = platformTable.xpath('./tbody/tr')
    if len(tableRows) == 0:
        return

    for tableRow in tableRows:
        self.platforms.append(Platform(tableRow))

def toPlatformCsv(self):
    platforms = []
    for platform in self.platforms:
        platforms.append(platform.toCsv(self.gameId))
    return platforms
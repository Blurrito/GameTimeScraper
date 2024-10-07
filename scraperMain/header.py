from scraperMain.utilities import toNumber, toTimestamp

class AverageTime:
    def __init__(self, timeHeaderEntry):
        self.categoryName = timeHeaderEntry.xpath('./h4/text()').get()
        self.value = toTimestamp(self, timeHeaderEntry.xpath('./h5/text()').get())

    def print(self):
        print(f"{self.categoryName}: {self.value}\n")

    def toCsv(self, gameId):
        return [gameId, self.categoryName, self.value]

def readHeader(self, response):
    header = response.xpath('//div[@class="GameHeader_profile_header_game__CH56Y"]')
    headerComponents = header.xpath('./div')
    if len(headerComponents) == 0:
        return

    self.gameName = headerComponents[0].xpath('./text()').get()
    statistics = headerComponents[2].xpath('./ul/li')
    if len(statistics) < 6:
        return

    self.playCount = toNumber(self, statistics[0].xpath('./text()').get().split(' ')[0])
    self.backlogCount = toNumber(self, statistics[1].xpath('./text()').get().split(' ')[0])
    self.replayCount = toNumber(self, statistics[2].xpath('./text()').get().split(' ')[0])
    self.retiredPercentage = float(statistics[3].xpath('./text()').get().split(' ')[0].replace('%', ''))
    self.rating = float(statistics[4].xpath('./text()').get().split(' ')[0].replace('%', ''))
    self.completedCount = toNumber(self, statistics[5].xpath('./text()').get().split(' ')[0])

def readAverageTimes(self, response):
    timeHeader = response.xpath('//div[contains(@class, "GameStats_game_times__KHrRY")]')
    if len(timeHeader) == 0:
        return

    timeHeaderEntries = timeHeader.xpath('./ul/li')
    if len(timeHeaderEntries) < 1:
        return

    self.headerTimes = []
    for timeHeaderEntry in timeHeaderEntries:
        self.headerTimes.append(AverageTime(timeHeaderEntry))

def toHeaderCsv(self):
    return [self.gameId, self.gameName, self.playCount, self.backlogCount, self.replayCount, self.retiredPercentage,
            self.rating, self.completedCount]

def toHeaderTimeCsv(self):
    headerTimes = []
    for headerTime in self.headerTimes:
        headerTimes.append(headerTime.toCsv(self.gameId))
    return headerTimes

def printHeader(self):
    print(f"\n{self.gameName}:\n"
          f"Played by {self.playCount} people\n"
          f"Completed by {self.completedCount} people\n"
          f"Replayed by {self.replayCount} people\n"
          f"In {self.backlogCount} people's backlog\n"
          f"Retired by {self.backlogCount} people\n"
          f"Average rating: {self.rating}\n")

    print(f"\nAverage completion times:\n")
    for headerTime in self.headerTimes:
        headerTime.print()
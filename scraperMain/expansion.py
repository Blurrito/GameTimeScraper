from utilities import toNumber, toTimestamp

class Expansion:
    def __init__(self, tableRow):
        expansionData = tableRow.xpath('./td')
        pageUrl = expansionData[0].xpath('./a')
        self.name = pageUrl.xpath('./text()').get()

        href = pageUrl.xpath('@href').get()
        if href is None:
            return

        splitHref = href.split('/')
        if len(splitHref) < 2:
            return

        self.id = int(splitHref[len(splitHref) - 1])
        self.polled = toNumber(self, expansionData[1].xpath('./text()').get())
        self.rated = toNumber(self, expansionData[2].xpath('./text()').get())
        self.main = toTimestamp(self, expansionData[3].xpath('./text()').get())
        self.side = toTimestamp(self, expansionData[4].xpath('./text()').get())
        self.complete = toTimestamp(self, expansionData[5].xpath('./text()').get())
        self.all = toTimestamp(self, expansionData[6].xpath('./text()').get())

    def print(self):
        print(f"Name: {self.name}\n"
              f"Poll count: {self.polled}\n"
              f"Rating: {self.rated}\n"
              f"Main: {self.main}\n"
              f"Side: {self.side}\n"
              f"Complete: {self.complete}\n"
              f"All: {self.all}\n")

    def toCsv(self, gameId):
        return [gameId, self.id, self.name, self.polled, self.rated, self.main, self.side, self.complete, self.all]


def readExpansions(self, response):
    self.expansions = []
    expansionTable = response.xpath('//div[@class="in scrollable scroll_blue back_primary shadow_box"]')
    if len(expansionTable) > 0:
        tableRows = expansionTable[0].xpath('./table/tbody/tr')
        for tableRow in tableRows:
            self.expansions.append(Expansion(tableRow))

def toExpansionCsv(self):
    expansions = []
    for expansion in self.expansions:
        expansions.append(expansion.toCsv(self.gameId))
    return expansions
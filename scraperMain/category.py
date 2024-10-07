from utilities import toNumber, toTimestamp

class PlayStyle:
    def __init__(self, tableRow):
        self.name = tableRow.xpath('./td/text()')[0].get()
        self.polled = toNumber(self, tableRow.xpath('./td/text()')[1].get())
        self.average = toTimestamp(self, tableRow.xpath('./td/text()')[2].get())
        self.median = toTimestamp(self, tableRow.xpath('./td/text()')[3].get())
        self.fastest = toTimestamp(self, tableRow.xpath('./td/text()')[4].get())
        self.slowest = toTimestamp(self, tableRow.xpath('./td/text()')[5].get())

    def print(self):
        print(f"Name: {self.name}\n"
              f"Poll count: {self.polled}\n"
              f"Average time: {self.average}\n"
              f"Median time: {self.median}\n"
              f"Fastest time: {self.fastest}\n"
              f"Slowest time: {self.slowest}\n")

    def toCsv(self, gameId, categoryName):
        return [gameId, categoryName, self.name, self.polled, self.average, self.median, self.fastest, self.slowest]


class Category:
    def __init__(self, table):
        self.name = table.xpath('./thead/tr/td/text()')[0].get()

        rows = table.xpath('./tbody/tr')
        self.playStyles = []
        for row in rows:
            self.playStyles.append(PlayStyle(row))

    def print(self):
        print(f"\nName: {self.name}")
        for playStyle in self.playStyles:
            playStyle.print()

    def toCsv(self, gameId):
        category = []
        for playStyle in self.playStyles:
            playStyle = playStyle.toCsv(gameId, self.name)
            category.append(playStyle)
        return category


def readGameplayCategories(self, response):
    self.categories = []
    tables = response.xpath('//table[contains(@class, "GameTimeTable_game_main_table__7uN3H")]')
    for table in tables:
        self.categories.append(Category(table))

def toCategoryCsv(self):
    categories = []
    for category in self.categories:
        playstyles = category.toCsv(self.gameId)
        for playstyle in playstyles:
            categories.append(playstyle)
    return categories
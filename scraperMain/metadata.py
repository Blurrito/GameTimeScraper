from datetime import datetime

class ReleaseDate:
    def __init__(self, releaseDate):
        self.region = releaseDate.xpath('./strong/text()').get()[:-1]

        dateString = releaseDate.xpath('./text()').extract()[1]
        self.date = datetime.strptime(dateString, '%B %d, %Y').date()

    def print(self):
        print(f"Region: {self.region}\nDate: {self.date}\n")

    def toCsv(self, gameId):
        return [gameId, self.region, self.date]


class Metadata:
    def __init__(self, metadataField):
        self.name = metadataField.xpath('./strong/text()').get()
        self.value = metadataField.xpath('./text()').extract()[1].split(', ')

    def print(self):
        print(f"\n{self.name}:")
        for value in self.value:
            print(f"{value}")

    def toCsv(self, gameId):
        dataframe = []
        for value in self.value:
            dataframe.append([gameId, self.name, value])
        return dataframe

def toReleaseDatesCsv(self):
    releaseDates = []
    for releaseDate in self.releaseDates:
        releaseDates.append(releaseDate.toCsv(self.gameId))
    return releaseDates

def toMetadataCsv(self):
    metadataFields = []
    for metadataField in self.metadataFields:
        categoryFields = metadataField.toCsv(self.gameId)
        for categoryField in categoryFields:
            metadataFields.append(categoryField)
    return metadataFields

def readMetadata(self, response):
    metadata = response.xpath('//div[@class="in back_primary shadow_box"]')
    if len(metadata) == 0:
        return

    self.metadataFields = []
    mediumSummaries = metadata[0].xpath('//div[@class="GameSummary_profile_info__HZFQu GameSummary_medium___r_ia"]')
    if len(mediumSummaries) > 0:
        for summary in mediumSummaries:
            self.metadataFields.append(Metadata(summary))

    self.releaseDates = []
    smallSummaries = metadata[0].xpath('//div[@class="GameSummary_profile_info__HZFQu"]')
    if len(smallSummaries) < 1:
        return

    smallSummaries.pop(len(smallSummaries) - 1)
    for smallSummary in smallSummaries:
        self.releaseDates.append(ReleaseDate(smallSummary))

def printMetadata(self):
    for metadataField in self.metadataFields:
        metadataField.print()

    print("\nRelease dates:\n")
    for releaseDate in self.releaseDates:
        releaseDate.print()
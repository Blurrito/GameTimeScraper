import os
from expansion import readExpansions, toExpansionCsv
from gameSystem import readPlatforms, toPlatformCsv
from category import readGameplayCategories, toCategoryCsv
from metadata import readMetadata, printMetadata, toMetadataCsv, toReleaseDatesCsv
from header import readHeader, readAverageTimes, printHeader, toHeaderCsv, toHeaderTimeCsv
import scrapy

class Game:
    def __init__(self, response):
        # Get game ID
        url = response.request.url.split('/')
        self.gameId = int(url[len(url) - 1])

        # Get header information
        readHeader(self, response)

        # Get al metadata
        readMetadata(self, response)

        # Get average times
        readAverageTimes(self, response)

        # Get expansions
        readExpansions(self, response)

        # Get gameplay categories
        readGameplayCategories(self, response)

        # Get platform information
        readPlatforms(self, response)

        # Print all gathered information
        # self.print()

    def print(self):
        printHeader(self)
        printMetadata(self)

        for category in self.categories:
            category.print()

        print("\nExpansions:\n")
        for expansion in self.expansions:
            expansion.print()

        print("\nPlatforms:\n")
        for platform in self.platforms:
            platform.print()

    def toCsv(self):
        return[toHeaderCsv(self), toHeaderTimeCsv(self), toMetadataCsv(self), toReleaseDatesCsv(self), toExpansionCsv(self), toCategoryCsv(self), toPlatformCsv(self)]

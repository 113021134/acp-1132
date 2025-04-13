import scrapy


class RepositoryItem(scrapy.Item):
    url = scrapy.Field()
    about = scrapy.Field()
    last_updated = scrapy.Field()
    languages = scrapy.Field()
    number_of_commits = scrapy.Field()

    pass

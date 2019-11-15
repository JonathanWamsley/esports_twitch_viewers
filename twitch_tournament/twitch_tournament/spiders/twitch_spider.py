import scrapy
from scrapy.loader import ItemLoader
# scrapy documentation and setup can be found at https://docs.scrapy.org/en/latest/

# class that stores the scraped data into a Field obj
class TwitchTournamentItem(scrapy.Item):
    title = scrapy.Field()
    prize_pool = scrapy.Field()
    event_dates = scrapy.Field()
    average_viewers = scrapy.Field()
    air_time = scrapy.Field()
    peak_viewers = scrapy.Field()
    hours_watched = scrapy.Field()


class Twitch_Tournament_Spider(scrapy.Spider):
    # this spider collects the tournament and twitch stats info
    name = 'twitch'

    def start_requests(self):
        # This starts the web scraper at the correct website
        url = "https://escharts.com/tournaments?order=default&status=recent"
        yield scrapy.Request(url=url, callback=self.parse_tournament_info)

    def parse_tournament_info(self, response):
        # Extracts all the tournament links to step into
        hrefs = response.xpath("//tr[*]/*/*[@class='table_refactored-data_primary']/@href").getall()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url=url, callback=self.parse_tournament_viewers)

        # pagination - will repeat the tournament link gathering for every page
        for page in range(2, 137):
            url = 'https://escharts.com/tournaments?order=default&status=recent&page=' + str(page)
            yield scrapy.Request(url=url, callback=self.parse_tournament_info)

    def parse_tournament_viewers(self, response):
        # gathers more info by stepping into page links
        loader = ItemLoader(TwitchTournamentItem(), response)
        try:
            # data will be used for a machine learning project which wants no missing data, therefore if any of the
            # relevant info is missing then it will not be scraped
            title = response.xpath("//h1/text()").get().strip()
            event_dates = response.xpath("//tr/td/h4/text()").get().replace('.', '/')
            average_viewers = response.xpath("//div[@class='gradient-block blue']/div/text()").get().replace(' ', ',')
            air_time = response.xpath("//div[@class='gradient-block green']/div/text()").get().replace(' ', ',')
            peak_viewers = response.xpath("//div[@class='gradient-block yellow']/div/text()").get().replace(' ', ',')
            hours_watched = response.xpath("//div[@class='gradient-block red']/div/text()").get().replace(' ', ',')
            loader.add_value('title', title)
            loader.add_value('event_dates', event_dates)
            loader.add_value('average_viewers', average_viewers)
            loader.add_value('air_time', air_time)
            loader.add_value('peak_viewers', peak_viewers)
            loader.add_value('hours_watched', hours_watched)
        except IndexError:
            print('bad website format or did not include twitch stats and is not desirable output')
        yield loader.load_item()



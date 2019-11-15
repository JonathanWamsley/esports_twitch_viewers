# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitchTournamentItem(scrapy.Item):
    title = scrapy.Field()
    prize_pool = scrapy.Field()
    event_dates = scrapy.Field()
    average_viewers = scrapy.Field()
    air_time = scrapy.Field()
    peak_viewers = scrapy.Field()
    hours_watched = scrapy.Field()

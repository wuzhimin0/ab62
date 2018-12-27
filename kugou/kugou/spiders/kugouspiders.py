# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from kugou.items import KugouItem
import json

class Kugouspiders(CrawlSpider):
    name = 'kugou'
    allowed_domains = ['kugou.com']
    def start_requests(self):
        for page in range(1,2):
            strat_url = "https://www.kugou.com/yy/rank/home" + "/"+str(page)+ "-8888.html?from=rank"
            yield Request(url=strat_url)
    def parse(self, response):
        infos = response.xpath('//div[@class="pc_temp_songlist "]/ul/li')
        for info in infos:
            item = KugouItem()
            singer_song = info.xpath('a/text()').extract()[0]
            item["singer"] = singer_song.split("-")[0].strip()
            item["song"] = singer_song.split("-")[-1].strip()
            item["time"] = info.xpath('span/span[@class="pc_temp_time"]/text()').extract()[0].strip()
            song_url = "https://songsearch.kugou.com/song_search_v2?keyword={0}+-+{1}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1544671489798".format(item["singer"],item["song"])
            if song_url:
                yield Request(url=song_url,callback=self.song_detail,meta={"data":item,"singer_song":singer_song})
    def song_detail(self,response):
        singer_song = response.meta["singer_song"]
        result = json.loads(response.body)
        for song_result in result["data"]["lists"]:
            if song_result["FileName"].replace("<em>","").replace("</em>","") == singer_song:
                song_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}".format(song_result["FileHash"])
                yield Request(url=song_url,callback=self.download_song,meta={"data":response.meta["data"]})
                break
    def download_song(self,response):
        item = response.meta["data"]
        result = json.loads(response.body)
        item["song_down_url"] = result["data"]["play_url"]
        yield item
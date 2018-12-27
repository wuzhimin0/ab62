# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
class KugouPipeline(object):
    def process_item(self, item, spider):
        with open("1.json","a+",encoding="utf-8") as f:
            f.write(json.dumps(dict(item),ensure_ascii=False) + "\n")
        return item
# 音乐视频文件下载管道
class SongPipeline(FilesPipeline):
    # 自定义文件下载管道
    def get_media_requests(self, item, info):
        # 根据文件的url逐一发送请求
        if item['song_down_url']:
            yield Request(url=item['song_down_url'], meta={"data":item})
    def file_path(self, request, response=None, info=None):
        item = request.meta["data"]
        name = item["singer"] + "-" + item["song"]
        # print(name)
        # 提取url后面的图片名称
        image_guid = name + "." +request.url.split("/")[-1].split(".")[-1]
        filename = u'{}'.format(image_guid)
        return filename
    def item_completed(self, results, item, info):
        video_paths = [x['path'] for ok, x in results if ok]
        print("11111",video_paths)
        item['song_down_url'] = video_paths
        return item
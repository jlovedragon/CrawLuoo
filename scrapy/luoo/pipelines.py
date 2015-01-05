#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from luoo.items import LuooItem
from dataProcess import dataProcess

class LuooPipeline(object):
    def process_item(self, item, spider):
        dirName = '/home/quentin/Entertainment/Music/Luoo/'
        currDirName = 'vol' + item['albumId'] + ' ' +  item['albumName']
        fileName = dirName + currDirName
        #self.file = open('luoo.txt', 'wb')

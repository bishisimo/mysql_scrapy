# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from loguru import logger
import pandas as pd


class MysqlVarsPipeline:
    def __init__(self):
        self.df = pd.DataFrame()

    def close_spider(self, spider):
        logger.debug(f"all data: {len(self.df)}")
        if len(self.df) == 0:
            return
        path = "mysql_vars.csv"
        logger.info(f"write data to file: {path}")
        self.df.to_csv(path, sep="\t", index=False, header=True)

    def process_item(self, item, spider):
        if "name" not in item or item["name"] is None:
            return item
        data = dict(item)
        self.df = self.df.append(data, ignore_index=True)
        return item

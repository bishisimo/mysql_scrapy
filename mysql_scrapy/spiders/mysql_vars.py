import os.path
import time

import scrapy
from loguru import logger

from mysql_scrapy.items import MysqlVarsItem


class MysqlVarsSpider(scrapy.Spider):
    name = "mysql_vars"
    allowed_domains = ["dev.mysql.com"]
    hrefs = ()
    # start_urls = ["https://dev.mysql.com/doc/refman/8.0/en/"]
    start_urls = ["https://dev.mysql.com/doc/refman/8.0/en/dynindex-sysvar.html"]
    # start_urls = ["https://dev.mysql.com/doc/refman/8.0/en/group-replication-options.html"]

    def parse(self, response):
        if len(self.hrefs) == 0:
            hrefs = response.xpath(system_vars_index_xpath).getall()
            self.hrefs = set(hrefs)
            logger.info(f"index has all: {len(hrefs)},  after deduplication is: {len(self.hrefs)}")
            for i, href in enumerate(self.hrefs):
                time.sleep(0.1)
                logger.debug(f"index: {i}, get href: {href}")
                url = response.urljoin(href)
                yield scrapy.Request(url)
            return

        # get data
        href = os.path.basename(response.request.url)
        tables = response.xpath(table_xpath)
        logger.debug(f"{href} page has table: {len(tables)}")
        for t in tables:
            data = {"href": href}
            for k in data_xpath:
                if k in mult:
                    data[k] = t.xpath(data_xpath[k]).getall()
                else:
                    data[k] = t.xpath(data_xpath[k]).get()
            desc = [
                line.strip().replace("\n        ", " ") for line in
                get_describe_xpath(t,data["name"]).getall() if line.strip() != data["name"]
            ]
            desc_str = ""
            desc_str = desc_str.join(desc)
            data["description"] = desc_str
            item = MysqlVarsItem(data)
            yield item


nav_links_xpath = "//a[@class='doctoc']/ul/li/div[@class='docs-sidebar-nav-link']/a"

system_vars_index_xpath = "//a[@class='xref']/@href"

next_href_xpath = "//a[@aria-label='Next']/@href"

table_xpath = "//table[@frame='box']/tbody"

mult = ["validation"]
data_xpath = {
    "name": ".//tr[contains(., 'System Variable')]/td/code/a/text()",
    "format": ".//tr[contains(., 'Command-Line Format')]/td/code/text()",
    "version": ".//tr[contains(., 'Introduced')]/td/text()",
    "scope": ".//tr[contains(., 'Scope')]/td/text()",
    "dynamic": ".//tr[contains(., 'Dynamic')]/td/text()",
    "type": ".//tr[contains(., 'Type')]/td/text()",
    "default": ".//tr[contains(., 'Default Value')]/td/code/text()",
    "min": ".//tr[contains(., 'Minimum Value')]/td/code/text()",
    "max": ".//tr[contains(., 'Maximum Value')]/td/code/text()",
    "unit": ".//tr[contains(., 'Unit')]/td/text()",
    "hint": ".//tr[contains(., 'Hint Applies')]/td/text()",
    "validation": ".//tr[contains(., 'Valid Values')]/td/p/code/text()",
}


def get_describe_xpath(s,name):
    return s.xpath(f"//li/p/a[contains(@href, '{name}')]|//li/p/code[contains(., '{name}')]").xpath("string(..)")


if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl mysql_vars".split()
    cmdline.execute(args)

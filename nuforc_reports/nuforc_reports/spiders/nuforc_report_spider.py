# -*- coding: utf-8 -*-
import scrapy


class NuforcReportSpider(scrapy.Spider):
    name = 'nuforc_report_spider'
    allowed_domains = ['www.nuforc.org']
    start_urls = ['http://www.nuforc.org/webreports/ndxevent.html']

    def parse(self, response):
        
        table_links = response.xpath('//tr/td/font/a')
        for tl in table_links:
            if tl is not None:
                yield response.follow(tl, self.parse_month_index)

    def parse_month_index(self, response):

        table_rows = response.xpath('//table/tbody/tr')
        
        # Each table row comes with structured summary information.
        # Extract this and pass it to the next request as metadata.
        for tr in table_rows:
            table_elements = tr.xpath('.//td')
            date_time_path = table_elements[0] \
                if len(table_elements) > 0 else None
            
            # If the date time path can't be extracted, skil this row.
            if not date_time_path:
                continue
            
            date_time = date_time_path.xpath('./font/a/text()').extract() \
                if len(table_elements) > 0 else None
            city = table_elements[1].xpath('./font/text()').extract() \
                if len(table_elements) > 1 else None
            state = table_elements[2].xpath('./font/text()').extract() \
                if len(table_elements) > 2 else None
            shape = table_elements[3].xpath('./font/text()').extract() \
                if len(table_elements) > 3 else None
            duration = table_elements[4].xpath('./font/text()').extract() \
                if len(table_elements) > 4 else None
            summary = table_elements[5].xpath('./font/text()').extract() \
                if len(table_elements) > 5 else None
            posted = table_elements[6].xpath('./font/text()').extract() \
                if len(table_elements) > 6 else None

            # Passing the summary table contents as metadata so the report 
            # request has access.
            yield response.follow(
                date_time_path.xpath("./font/a")[0],
                self.parse_report_table,
                meta={
                    "report_summary": {
                        "date_time": date_time[0] if date_time else None,
                        "city": city[0] if city else None,
                        "state": state[0] if state else None,
                        "shape": shape[0] if shape else None,
                        "duration": duration[0] if duration else None,
                        "summary": summary[0] if summary else None,
                        "posted": posted[0] if posted else None
                    }
                }
            )

    def parse_report_table(self, response):

        report_table = response.xpath('//table/tbody/tr')

        # The first row is a rehash (sort of) of the table summary.
        # Included for completeness.
        report_stats = \
            " ".join(report_table[0].xpath('./td/font/text()').extract()) \
            if len(report_table) > 0 else None
        # The second row is the text of the report.
        report_text = \
            " ".join(report_table[1].xpath('./td/font/text()').extract()) \
            if len(report_table) > 1 else None
        report_summary = response.meta["report_summary"]
    
        report = {
            "text": report_text,
            "stats": report_stats,
            **report_summary
        }

        yield report
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
import os 

class WebCrawler(scrapy.Spider):
    name = "MySpider"

    def __init__(self, seed_url=None, max_pages=None, max_depth=None, *args, **kwargs):
        super(WebCrawler, self).__init__(*args, **kwargs)
        if seed_url is None:
            raise ValueError("Please provide a seed URL")
        self.seed_url = seed_url
        self.allowed_domains = [self.get_domain(seed_url)]
        self.start_urls = [seed_url]
        self.max_pages = int(max_pages) if max_pages else None
        self.max_depth = int(max_depth) if max_depth else None
        self.current_depth = 0
        self.pages_crawled = 0
        
    def get_domain(self, url):
        return url.split("//")[-1].split("/")[0]

    def parse(self, response):
        self.pages_crawled += 1
        if self.max_pages and self.pages_crawled > self.max_pages:
            self.log('Reached maximum pages limit')
            raise CloseSpider('Reached maximum pages limit')
        
        pageNo = response.url.split("/")[-2]
        project_dir = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(project_dir, 'downloaded_files')
        filename='file-%s.html' % pageNo
        file_path = os.path.join(directory, filename)
        
        try:
            os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
            print(f"Directory '{directory}' created successfully.")
        except OSError as e:
            print(f"Failed to create directory '{directory}'. Reason: {e}")
        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        if self.max_depth is None or self.current_depth < self.max_depth:
            self.current_depth += 1
            links = LinkExtractor(allow_domains=self.allowed_domains).extract_links(response)
            for link in links:
                yield scrapy.Request(url=link.url, callback=self.parse)
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.mail import MailSender
from scrapy.spiders import CrawlSpider, Rule
from ..items import MaoyanItem


class Top100Spider(CrawlSpider):
    name = 'top100'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/board/4']

    rules = (
        Rule(LinkExtractor(allow=r'offset'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        movies = response.css('dd')
        for movie in movies:
            item = MaoyanItem()
            item['name'] = movie.css('a:attr(title)').extract_first()
            item['actors'] = movie.css('.star::text').re_first(r'主演： (.*)')
            item['releasetime'] = movie.css('.releasetime').re_first(r'上映时间： (.*)</p>')
            # 使用正则获取评分的组成部分,如[9,.,7]，分别为评分的整数，'.'，小数部分，组合之后9.7添加到item中
            score = movie.css('.score').re(r'\d|\.')
            item['score'] = ''.join(score)
            yield item
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

    def closed(self, reason):
        # 使用settings中的设置初始化邮件实例
        mail = MailSender.from_settings(self.settings)
        # 将需要发送的邮件数据使用'rb'模式打开
        files = open('./maoyantop100.json', 'rb')
        # 注意attachment是一个迭代器，每一个数据包含三个部分：
        # 1.附件的文件名
        # 2.附件格式
        # 3.需要发送的附件
        attachment = [('maoyan_top_100_movies.json', 'application/json', files)]
        mail.send(
            to=['1515622520@qq.com'],
            subject=u'maoyan movie',
            body=u'this is a test',
            attachs=attachment,
            mimetype='text/plain',
        )
        # 关闭文件
        files.close()

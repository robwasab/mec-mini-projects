import scrapy


class QuotesSpider(scrapy.Spider):
	name = "quotes"

	def start_requests(self):
		urls = [
			'http://quotes.toscrape.com/page/1/',
			#'http://quotes.toscrape.com/page/2/',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		# search for an <a> tag
		next_page_links = response.css('li.next a')

		# get its href attribute
		href = next_page_links.attrib.get('href', None)

		for quote in response.css('div.quote'):
			text = quote.css('span.text::text').get()
			auth = quote.css('small.author::text').get()

			tags = quote.css('div.tags a.tag::text').getall()

			yield {
				'text': text,
				'auth': auth,
				'tags': tags,
				'next': href,
			}


		# following links using url join
		#if href:
		#	url = response.urljoin(href)
		#	yield scrapy.Request(url=url, callback=self.parse)

		# following links using list of <a> tags
		#if next_page_links:
		#	print('')
		#	print('')
		#	print('next page link: %s'%next_page_links)
		#	print('')
		#	print('')
		#	yield from response.follow_all(next_page_links, callback=self.parse)

		# following links using follow_all
		yield from response.follow_all(css='li.next a', callback=self.parse)



import scrapy

class ToScrapeXPATH(scrapy.Spider):
	name = "toscrape-xpath"

	start_urls = [
		'http://quotes.toscrape.com/',
	]

	def parse(self, response):

		# parse quotes
		# quote
		# author
		# tags
		for quote_div in response.xpath("//div[@class='quote']"):
			text = quote_div.xpath(
				"span[@class='text']/text()"
			).get()

			auth = quote_div.xpath(
				"span/small[@class='author']/text()"
			).get()

			tags = quote_div.xpath(
				"div[@class='tags']/a[@class='tag']/text()"
			).getall()

			yield {
				'quot': text,
				'tags': tags,
				'auth': auth,
			}

		# look for the author
		yield from response.follow_all(
			xpath="//div[@class='quote']/span/a",
			callback=self.parse_author
		)

		# look for next page
		yield from response.follow_all(
			xpath="//li[@class='next']/a",
			callback=self.parse
		)


	def parse_author(self, response):
		# Author name
		auth = response.xpath(
			"//h3[@class='author-title']/text()"
		).get()

		# Born
		birthdate = response.xpath(
			"//span[@class='author-born-date']/text()"
		).get()

		# Born location
		birtharea = response.xpath(
			"//span[@class='author-born-location']/text()"
		).get()

		# Description
		desc = response.xpath(
			"//div[@class='author-description']/text()"
		).get()

		yield {
			'auth': auth,
			'bday': birthdate,
			'from': birtharea,
			'desc': desc,
		}

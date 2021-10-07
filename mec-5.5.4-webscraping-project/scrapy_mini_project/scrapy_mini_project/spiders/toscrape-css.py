import scrapy

class ToScrapeCSS(scrapy.Spider):
	name = "toscrape-css"

	start_urls = [
		'http://quotes.toscrape.com/',
	]

	def parse(self, response):

		# parse quotes
		# quote
		# author
		# tags
		for quote_div in response.css('div.quote'):
			text = quote_div.css('span.text::text').get()

			auth = quote_div.css('small.author::text').get()

			tags = quote_div.css('div.tags a.tag::text').getall()

			yield {
				'quot': text,
				'tags': tags,
				'auth': auth,
			}


		# look for the author
		yield from response.follow_all(
			css='small.author + a',
			callback=self.parse_author
		)

		# look for next page
		yield from response.follow_all(
			css='li.next a', 
			callback=self.parse
		)



	def parse_author(self, response):
		# Author name
		author = response.css(
			'h3.author-title::text'
		).get()

		# Born
		birthdate = response.css(
			'span.author-born-date::text'
		).get()

		# Born location
		birtharea = response.css(
			'span.author-born-location::text'
		).get()

		# Descripton
		desc = response.css(
			'div.author-description::text'
		).get()

		yield {
			'auth': author,
			'bday': birthdate,
			'from': birtharea,
			'desc': desc,
		}


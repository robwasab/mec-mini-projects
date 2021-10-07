import scrapy


class AuthorSpider(scrapy.Spider):
	name = "author"

	start_urls = [
		'http://quotes.toscrape.com/',
	]

	def parse(self, response):
		# look for the author
		yield from response.follow_all(
			css='small.author + a',
			callback=self.parse_author
		)

		# look for the next page
		yield from response.follow_all(
			css='li.next a', 
			callback=self.parse
		)


	def parse_author(self, response):
		print('parsing author')
		# Author name
		author_name = response.css(
			'h3.author-title::text'
		).get()

		# Born
		born_date = response.css(
			'span.author-born-date::text'
		).get()

		# Born location
		born_location = response.css(
			'span.author-born-location::text'
		).get()

		# Descripton
		desc = response.css(
			'div.author-description::text'
		).get()


		yield {
			'author': author_name,
			'birth_date': born_date,
			'birth_location': born_location,
			'description': desc,
		}


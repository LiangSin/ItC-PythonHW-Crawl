from crawler import Crawler
from args import get_args
import csv


if __name__ == '__main__':
	args = get_args()
	crawler = Crawler()
	contents = crawler.crawl(args.start_date, args.end_date)
	#write
	with open(args.output, 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		for content in contents:
			writer.writerow(content)
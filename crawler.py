from lxml import etree
import time
import urllib.parse
import requests
from datetime import datetime


class Crawler(object):
    def __init__(self,
                 base_url='https://www.csie.ntu.edu.tw/news/',
                 rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date):
        """Main crawl API
        Note that you need to sleep 0.1 seconds for any request.
        """
        contents = list()  #output
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page='&no='+str(page_num))
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break

        contents.sort(reverse=True)
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num

        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        full_url = self.base_url + self.rel_url + page
        time.sleep(0.1)
        res = requests.get(
            full_url,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        
        root = etree.HTML(res)

        dates = list()
        titles = list()
        rel_urls = list()
        for i in range(1,11):  #crawl the ten rows, record the ones between start_date and end_date
            cur_xpath = "/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr["+str(i)+"]/"
            input_date = str(root.xpath(cur_xpath + "td[1]")[0].text)
            date = datetime.strptime(input_date, '%Y-%m-%d')
            if(date <= end_date and date >= start_date):
                dates.append(input_date)
                titles.append(root.xpath(cur_xpath + "td[2]/a")[0].text)
                rel_urls.append(root.xpath(cur_xpath + "td[2]/a/@href")[0])

        last_path = "/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[10]/td[1]"
        last_date = datetime.strptime(root.xpath(last_path)[0].text, '%Y-%m-%d')

        contents = list()  #output
        l = len(rel_urls)
        for i in range(l):  #crawl content of the pages that are selected
            sub_url = self.base_url + rel_urls[i]
            content = self.crawl_content(sub_url)
            contents.append([dates[i],titles[i],content])

        return contents, last_date

    def crawl_content(self, url):
        """Crawl the content of given url

        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216
        then you are to crawl contents of
        ``Title : 我與DeepMind的A.I.研究之路, My A.I. Journey with DeepMind Date : 2019-12-27 2:20pm-3:30pm Location : R103, CSIE Speaker : 黃士傑博士, DeepMind Hosted by : Prof. Shou-De Lin Abstract: 我將與同學們分享，我博士班研究到加入DeepMind所參與的projects (AlphaGo, AlphaStar與AlphaZero)，以及從我個人與DeepMind的視角對未來AI發展的展望。 Biography: 黃士傑, Aja Huang 台灣人，國立臺灣師範大學資訊工程研究所博士，現為DeepMind Staff Research Scientist。``
        """
        time.sleep(0.1)
        res = requests.get(
            url,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        
        root = etree.HTML(res)
        texts = root.xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]//text()")

        contents = str()
        for text in texts:
            contents += str(text).replace("\xa0"," ")
        return contents

        raise NotImplementedError
#! /home/minghui/anaconda2/envs/py3/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import datetime


class LSubmit ():

    def __init__(self, bs_of_submit):
        self.text = bs_of_submit.text
        list_of_item_raw = self.text.split("\n")
        list_of_item = list(filter(lambda item: len(item) > 0,
                                   map(lambda item: item.strip(),
                                       list_of_item_raw)))
        self.status = list_of_item[0]
        self.language = list_of_item[1]
        self.problem = list_of_item[2]
        self.raw_time = list_of_item[3]
        self.time = datetime.datetime.fromtimestamp(time.time() - self._parse_time(list_of_item[3]))

    def _parse_time(self, time_str):
        """
        parse string like
        ''
        '29 minitues ago'
        '1 week, 4 days ago'
        '4 months, 1 week ago'
        '1 year, 3 months ago'
        """
        time_str = time_str.replace(u'\xa0', u' ')
        commaSplit = time_str.split(',')
        commaTime = 0
        for eachCommaSplit in commaSplit:
            dotSplit = eachCommaSplit.split(' ')
            try:
                dotSplit.remove('')
            except:
                pass
            lasttime = dotSplit[0]
            period = dotSplit[1]
            periodDict = {
                'minutes':60,
                'minute':60,
                'hour':60 * 60,
                'hours':60 * 60,
                'day':60 * 60 * 24,
                'days':60 * 60 * 24,
                'week':60 * 60 * 24 * 7,
                'weeks':60 * 60 * 24 * 7,
                'month':60 * 60 * 24 * 30,
                'months':60 * 60 * 24 * 30,
                'year':60 * 60 * 24 * 365,
                'years':60 * 60 * 24 * 365,
                }
            dotTime = periodDict[period] * int(lasttime)
            commaTime = commaTime + dotTime
        return commaTime

      
    def tostring(self):
        if self.language != 'java' or self.status != 'Accepted':
            return 'None'            
        return 'Right'
    def __str__(self):
        return ("(%s) <%s> [%s] {%s}" % (self.problem, self.language, self.status, self.raw_time))
    def __repr__(self):
        return self.__str__()
class LParser ():

    def __init__(self, html):
        #使用"html.parser"解析器
        self.soup = BeautifulSoup(html, "html.parser")

    def parse(self):
        #模糊全定位，省去确定过多定位条件
        test = self.soup.select("div > ul")
        newAccept = []
        for it in test:
            items = it.select("a.list-group-item")
            if items is not None:
                for submit in items:
                    submitstr = LSubmit(submit)
                    submits = submitstr.tostring()
                    if submits == 'None':
                        pass
                    else:
                        newAccept.append(submitstr)

        return newAccept
    def parse2(self):
        #精确定位，对分析结构的能力要求较高
        chunk_of_submit=self.soup.select_one(".row > div:nth-of-type(2) > div:nth-of-type(2) > ul")
        ansAccept = []
        if chunk_of_submit is not None:
            list_of_submit = chunk_of_submit.select("a.list-group-item")
            for submit in list_of_submit:
                submitstr = LSubmit(submit)
                submits = submitstr.tostring()
                if submits == 'None':
                    pass
                else:
                    ansAccept.append(submitstr)
        else:
            chunk_of_submit=self.soup.select_one(".row > div:nth-of-type(2) > div:nth-of-type(3) > ul")
            if chunk_of_submit is not None:
                list_of_submit = chunk_of_submit.select("a.list-group-item")
                for submit in list_of_submit:
                    submitstr = LSubmit(submit)
                    submits = submitstr.tostring()
                    if submits == 'None':
                        pass
                    else:
                        ansAccept.append(submitstr)
        print(ansAccept)
        return ansAccept

# run test
if __name__ == "__main__":
    def read_page(name):
        with open(name, "r") as f:
            test_html = f.read()
            return test_html

    html = read_page("res/index.html")
    result = LParser(html).parse()
    print(len(result))
    print(result)
    print('*'*40)

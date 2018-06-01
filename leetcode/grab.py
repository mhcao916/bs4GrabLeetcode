#! /home/minghui/anaconda2/envs/py3/bin/python
# -*- coding: utf-8 -*-
import requests
from config import Config


class LGrabber():

    def __init__(self, username):
 
#grab the page with given username

        self.page = requests.get(Config.url_prefix + username)
        self.content = self.page.content
        print(self.content)

if __name__ == "__main__":
    grab = LGrabber("mhcao916")
    assert(grab.page.status_code == 200)

import os
import re
import urllib
from bs4 import *
import threading

class Crawler:
	def __init__(self, keywords, page):
		self.keywords = keywords
		self.url = "http://www.zerochan.net/"+keywords
		self.page = page
		self.img_url = []
		self.num = 0

	def url_crawl(self):
		for i in range(1, self.page+1):
			tmp_url = self.url+"?p="+str(i)
			source = urllib.urlopen(tmp_url).read()
			if "No such tag. Back to" in source:
				return -1;
			source = BeautifulSoup(source, "html5lib")
			imgTagList = source('img')
			for j in range(0, len(imgTagList)):
				try:
					self.img_url.append(imgTagList[j]['src'])
				except:
					return -2;

	def url_setting(self):
		for i in range(len(self.img_url)):
			tmp = self.img_url[i].split('.')
			self.img_url[i] = "http://static.zerochan.net/.full."+tmp[-2]+"."+tmp[-1]

	def crawl(self, url):
		img = urllib.urlopen(url).read()
		f = open(self.keywords+"/"+('.'.join(url.split('.')[-2:])), 'wb')
		f.write(img)
		f.close()

	def findImg(self):
		ret = self.url_crawl()
		if ret == -1:
			return -1
		if ret == -2:
			return -2
		self.url_setting()
		self.num = len(self.img_url)
		return len(self.img_url)

	def start(self, num):
		try:
			self.keywords = self.keywords.replace(':', "")
			self.keywords = self.keywords.replace('\\', "")
			self.keywords = self.keywords.replace('/', "")
			self.keywords = self.keywords.replace('?', "")
			self.keywords = self.keywords.replace('!', "")
			self.keywords = self.keywords.replace('"', "")
			self.keywords = self.keywords.replace('<', "")
			self.keywords = self.keywords.replace('>', "")
			self.keywords = self.keywords.replace('|', "")
			os.makedirs(self.keywords)
		except:
			pass
		self.thread1 = threading.Thread(target=self.crawls, args=(1, num))
		self.thread1.start()
		self.thread2 = threading.Thread(target=self.crawls, args=(2, num))
		self.thread2.start()
		self.thread3 = threading.Thread(target=self.crawls, args=(3, num))
		self.thread3.start()
		self.thread4 = threading.Thread(target=self.crawls, args=(4, num))
		self.thread4.start()

	def crawls(self, num, maxNum):
		for i in range(0, (maxNum+4-num)/4):
			self.crawl(self.img_url[(i*4)+num-1])

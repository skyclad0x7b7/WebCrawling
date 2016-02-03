from Tkinter import *
import tkMessageBox
from crawler import *
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


class Interface:
	def __init__(self, Master):
		self.master = Master
		self.master.geometry('600x130')

		# MainFrame

		self.mainFrame = Frame(self.master)
		self.mainFrame.pack(fill=X)

		# UrlFrame

		self.urlFrame = Frame(self.mainFrame)
		self.urlFrame.pack(side=TOP, fill=X)

		self.urlLabel = Label(self.urlFrame)
		self.urlLabel.configure(text='Keywords :')
		self.urlLabel.pack(side=LEFT, padx=5, pady=10)

		self.urlEntry = Entry(self.urlFrame)
		self.urlEntry.configure(width=18)
		self.urlEntry.pack(side=LEFT, padx=5, pady=10)

		self.pageLabel = Label(self.urlFrame)
		self.pageLabel.configure(text='Page Number : ')
		self.pageLabel.pack(side=LEFT, padx=5, pady=10)

		self.pageEntry = Entry(self.urlFrame)
		self.pageEntry.configure(width=10)
		self.pageEntry.pack(side=LEFT, padx=5, pady=10)

		self.countLabel = Label(self.urlFrame)
		self.countLabel.configure(text='Image Number :')
		self.countLabel.pack(side=LEFT, padx=5, pady=10)

		self.countEntry = Entry(self.urlFrame)
		self.countEntry.configure(width=10)
		self.countEntry.pack(side=LEFT, padx=5, pady=10)

		# ButtonFrame

		self.buttonFrame = Frame(self.mainFrame)
		self.buttonFrame.pack(side=TOP, fill=X)

		self.findButton = Button(self.buttonFrame, command=self.findThreadingStart)
		self.findButton.configure(text='Find', width=25)
		self.findButton.pack(side=LEFT, padx=7, pady=5)

		self.startButton = Button(self.buttonFrame, command=self.startThreadingStart)
		self.startButton.configure(text='Start', width=25)
		self.startButton.pack(side=LEFT, padx=7, pady=5)

		self.stopButton = Button(self.buttonFrame, command=self.stopCrawling)
		self.stopButton.configure(text='Stop', width=25)
		self.stopButton.pack(side=LEFT, padx=7, pady=5)

		# Notification Frame

		self.notificationFrame = Frame(self.mainFrame)
		self.notificationFrame.pack(side=TOP, fill=X)

		self.numberLabel = Label(self.notificationFrame)
		self.numberLabel.configure(text='Images found : ')
		self.numberLabel.pack(side=LEFT, padx=10, pady=5)

		self.numberviewLabel = Label(self.notificationFrame)
		self.numberviewLabel.configure(text='N/A')
		self.numberviewLabel.pack(side=LEFT, padx=10, pady=5)

		self.notificationButton = Button(self.notificationFrame, command=self.help)
		self.notificationButton.configure(text = 'Help')
		self.notificationButton.pack(side=RIGHT, padx=10, pady=5)

		# Warning Frame

		self.warningFrame = Frame(self.mainFrame)
		self.warningFrame.pack(side=TOP, fill=X)

		self.warningLabel = Label(self.warningFrame)
		self.warningLabel.pack(side=LEFT, padx=10)

	def findThreadingStart(self):
		self.findThread = threading.Thread(target=self.findImage)
		self.findThread.start()

	def findImage(self):
		self.warningLabel.configure(text='[*] Finding Images...')

		url = self.urlEntry.get()
		if url=="":
			self.warningLabel.configure(text='[*] Please input keywords!')
			return
		page = self.pageEntry.get()
		try:
			page = int(page)
		except:
			self.warningLabel.configure(text='[*] Please input only INTEGER in page form!')
			return

		self.crawler = Crawler(url, page)
		self.number = self.crawler.findImg()

		if self.number == -1:
			self.warningLabel.configure(text='[*] No such Tag, please use other Tag')
			return
		elif self.number == -2:
			self.warningLabel.configure(text='[*] Exception occured. Please feedback to developer.')
			return

		self.numberviewLabel.configure(text=str(self.number))
		self.warningLabel.configure(text='[*] Finding Images finished')

	def startThreadingStart(self):
		self.startThread = threading.Thread(target=self.startCrawling)
		self.startThread.start()

	def startCrawling(self):
		self.warningLabel.configure(text='[*] Crawling Started')
		try:
			num = self.countEntry.get()
			if num=="MAX":
				num = self.number
			else:
				try:
					num = int(num)
				except:
					self.warningLabel.configure(text='[*] Please input only INTEGER in number form!')
					return

				if num > self.number:
					num = self.number
			self.crawler.start(num)
		except:
			self.warningLabel.configure(text="[*] Please do 'Find' before 'Start'!")
			return
	def stopCrawling(self):
		self.warningLabel.configure(text="[*] It can't be used!!")

	def help(self):
		helpString = """		[Usage]
1. Input the keywords in the box. (ex: Kousaka Kirino)
  It can be character's name, emotions(ex: crying, smile),
  objects(ex: wings, sword).
  Please use official name.

2. Input the page's number you want to crawl.
  About 5~15 images in one page.
  !! Too many pages (like above 100) can take many time.
  !! So please be careful.

3. Click the Find button, and wait for finishing.

4. After finished, input the number you want to crawl.
  If there's anything or number is greater than (3),
  It's automatically set as the maximum(3's number).
  If you want to crawl all of them, input 'MAX'.

5. Click the Start Button, and wait for finishing.

=============================================

This Program was made by 5kyc1ad(skyclad1975).
It's made up of Python 2.7.10, with Tkinter, BeautifulSoup.

Please Feedback : skyclad0x7b7@gmail.com
Blog : http://5kyc1ad.tistory.com"""
		tkMessageBox.showinfo("Zerochan_Crawler::Help",helpString)

		
root = Tk()
myApp = Interface(root)
root.mainloop()
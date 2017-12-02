from lxml import html

def padZero(num):
    if len(num) == 1:
        return "0" + num
    return num

def monthToNum(shortMonth):
    
    dates = {
        'Jan' : "01",
        'Feb' : "02",
        'March' : "03",
        'April' : "04",
        'May' : "05",
        'June' : "06",
        'July' : "07",
        'Aug' : "08",
        'Sept' : "09",
        'Oct' : "10",
        'Nov' : "11",
        'Dec' : "12"
    }

    if shortMonth not in dates:
        return ""

    return dates[shortMonth]

outputFile = "nytdata.csv"

f1=open(outputFile, 'w+')

with open ("nyt.html", "r") as myfile:
    data = myfile.read().replace('\n', '')

tree = html.fromstring(data)

titles = tree.xpath("//h2[@class='headline']/text()")
dates = tree.xpath("//time[@class='dateline']/text()")

outputList = [None] * len(titles)

for i, title in enumerate(titles):
	date = dates[i].replace(".", "").replace(",", "").split(" ")
	outputList[i] = date[2] + "" + monthToNum(date[0]) + "" + padZero(date[1]) + "," + title.strip().replace(",", "")

for item in outputList:
	print >> f1, item.encode("utf-8")

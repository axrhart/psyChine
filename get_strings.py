import urllib2
from bs4 import BeautifulSoup

# Useful functions

def rmBrackets(string):
    bracket_location = string.find('(')
    if bracket_location != -1:
        return string[0:bracket_location-1]
    else:
        return string

# Scrape ML Glossary
google_page = "https://developers.google.com/machine-learning/glossary/"
page = urllib2.urlopen(google_page)
soup = BeautifulSoup(page, 'html.parser')
entries = soup.find_all('h2', attrs={'class': 'hide-from-toc'})

first_texts = []

for entry in entries:
    first_texts.append(rmBrackets(entry.text.strip()))

# Scrapy Psych Glossary

spark_page = "https://www.sparknotes.com/psychology/psych101/glossary/terms/"
page = urllib2.urlopen(spark_page)
soup = BeautifulSoup(page, 'html.parser')
lines = soup.find_all('div', attrs={'class': 'content_txt'})
entries = soup.find_all('b')

second_texts = []

for entry in entries:
    second_texts.append(rmBrackets(entry.text.strip().encode('ascii','ignore')))

# Generate output of matches

file = open("full_list.md", "w")
file.write("# List of generated pairs\n\n")
file.close

file = open("full_list.md", "a")
for x in range(0,len(first_texts)-1):
    file.write("## " + first_texts[x] +"\n")
    file.write("| One | Two | Three |\n")
    file.write("| --- | --- | ----- |\n")
    for y in range(0,len(second_texts)-1):
        file.write("| " + first_texts[x] + " " + second_texts[y] + " ")
        if y % 3 == 0:
            file.write("|\n")
    
    file.write("\n")    
    
file.close
import urllib2
import datetime
import random
import sys
import os
import cPickle as pickle
from bs4 import BeautifulSoup

# Init variables
size = 10
append = True
parse_anew = False
random_file_name = "new_random_list.md"
fixed_file_name = "full_list.md"

# Useful functions

def rmBrackets(string):
    bracket_location = string.find('(')
    if bracket_location != -1:
        return string[0:bracket_location-1]
    else:
        return string

# Scrape ML Glossary if not already saved
try:
    if parse_anew:
        raise IOError

    with open('ml.pkl', 'rb') as input:
        first_texts = pickle.load(input)
except IOError:
    google_page = "https://developers.google.com/machine-learning/glossary/"
    page = urllib2.urlopen(google_page)
    soup = BeautifulSoup(page, 'html.parser')
    entries = soup.find_all('h2', attrs={'class': 'hide-from-toc'})

    first_texts = []

    for entry in entries:
        first_texts.append(rmBrackets(entry.text.strip()))

    with open("ml.pkl","wb") as output:
        pickle.dump(first_texts, output, -1)  

# Scrapy Psych Glossary if not already saved
try:
    if parse_anew:
        raise IOError

    with open('psy.pkl', 'rb') as input:
        second_texts = pickle.load(input)
except IOError:        
    spark_page = "https://www.sparknotes.com/psychology/psych101/glossary/terms/"
    page = urllib2.urlopen(spark_page)
    soup = BeautifulSoup(page, 'html.parser')
    lines = soup.find_all('div', attrs={'class': 'content_txt'})
    entries = soup.find_all('b')

    second_texts = []

    for entry in entries:
        second_texts.append(rmBrackets(entry.text.strip().encode('ascii','ignore')))

    with open("psy.pkl","wb") as output:
        pickle.dump(second_texts, output, -1)  

# Generate output of all matches, if file doesn't exist already
try:
    open(fixed_file_name)
except IOError:    
    file = open(fixed_file_name,"w")
    file.write("# List of generated pairs\n\n")
    file.close

    file = open(fixed_file_name, "a")
    for x in range(0,len(first_texts)-1):
        file.write("## " + first_texts[x] +"\n")
        file.write("| One | Two | Three |\n")
        file.write("| --- | --- | ----- |\n")
        for y in range(0,len(second_texts)-1):
            file.write("| " + first_texts[x].lower() + " " + second_texts[y].lower() + " ")
            if y % 3 == 0:
                file.write("|\n")
        
        file.write("\n")        
    file.close  

# Generate random output
if append:
    file = open(random_file_name,"a+")
else:
    file = open(random_file_name,"w+")

first_char = file.read(1)
if not first_char:
    file.write("# List of generated pairs\n")
else:
    file.write('\n')    

file.close    

file = open(random_file_name,"a")
file.write("## " + str(datetime.datetime.now()) + "\n\n")  
for x in range(1,11):
    a = random.randint(0,len(first_texts)-1)
    b = random.randint(0,len(second_texts)-1)

    file.write(str(x) + ". " + first_texts[a].lower() + " " + second_texts[b].lower() + "\n")

file.write("\n")
file.close    
import requests
from bs4 import BeautifulSoup
import json
import os
import sys


def getQuotes(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text)
    divs = soup.find_all("div", class_="su-note")
    para_list = []
    data_maps = []
    counter = 1
    for div in divs:
        get_paras_from_div(div, para_list)
    for para in para_list:
        dataMap = process_paras(para, counter)
        data_maps.append(dataMap)
        counter += 1
    json_dump = json.dumps(data_maps, indent=4, ensure_ascii=False)
    write_to_file(json_dump)


def write_to_file(json_dump):
    output_file_path = os.path.join(os.path.curdir, "output.json")
    with open(output_file_path, 'w') as output_file:
        output_file.write(json_dump)


def get_paras_from_div(div, para_list):
    paras = div.find_all("p")
    if(len(paras) == 0):
        print(div)
    for para in paras:
        para_list.append(para)


def process_paras(para, counter):
    quote = para.get_text(strip=True).replace("“", "").replace("”", "")
    first_space = quote.find(" ")
    quote = quote[first_space:]
    starts_with_dot = quote.find(".")
    if(starts_with_dot == 1):
        quote = quote[2:]
    quote = quote.strip()
    index_of_author = quote.find("–")
    if(index_of_author == -1):
        index_of_author = quote.find("―")
    if(index_of_author == -1):
        index_of_author = quote.find("-")
    if(index_of_author == -1):
        author = ""
        quoteWithoutAuthor = ""
    else:
        author = quote[index_of_author+1:]
        quoteWithoutAuthor = quote[:index_of_author]
    dataMap = create_data_map(counter, author, quoteWithoutAuthor, quote)
    return dataMap


def create_data_map(counter, author, quoteWithoutAuthor, quote):
    dataMap = {}
    dataMap['id'] = counter
    dataMap['author'] = author
    dataMap['quoteWithoutAuthor'] = quoteWithoutAuthor
    dataMap['quoteWithAuthor'] = quote
    return dataMap


if __name__ == "__main__":
    args = sys.argv
    if(len(args) >= 2):
        url = args[1]
        getQuotes(url)
    else:
        print("Please provide a valid url as first arg")

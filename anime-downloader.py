import requests
import re
from bs4 import BeautifulSoup
import subprocess

# Based off of http://stackoverflow.com/a/16696317/2197700
def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename

# Utility/debugging method
def write_file(file, soup):
	with open(file, 'a') as out:
		out.write(soup.prettify().encode('utf-8','replace'))

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/index').content)

anime_name = raw_input('Enter an anime: ')

for link in soup.find_all(href=re.compile('(http://www.chia-anime.com/category/)')):
	if (link.get('href')[35:] == anime_name):
		print 'Found ' + anime_name + '!'
		break;
else:
	print 'Anime not found: ' + anime_name + '.'
	quit()

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/category/' + anime_name).content)
episode = raw_input('Enter an episode: ')

for link in soup.find_all(href=re.compile('(http://www.chia-anime.com/' + anime_name + '/' + anime_name + ')')):
	if (link.get('href')[68:] == episode):
		print 'Found episode ' + episode + '!'
		break;
else:
	print 'Episode not found: ' + episode + '.'
	quit()

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/' + anime_name + '/' + anime_name + '-episode-' + episode).content)
downloadPage = soup.find_all(href=re.compile('(http://download.animepremium.tv/get/)'))[0].get('href')

soup = BeautifulSoup(requests.get(downloadPage).content)
downloadLink = soup.find_all(href=re.compile('(animepremium.tv:8880/downloadcache)'))[0].get('href')

print 'Downloading!'
download_file(downloadLink)
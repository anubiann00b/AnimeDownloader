from bs4 import BeautifulSoup
from clint.textui import progress
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import requests

# Based off of http://stackoverflow.com/a/16696317/2197700
def download_file(url):
	print 'Downloading!'
	local_filename = url.split('/')[-1]
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		cnt = 0;
		print str(cnt) + ' MB',
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()
				cnt += 1
				print '\r' + str(cnt) + ' MB',
	print 'Done!'
	return local_filename

# Utility/debugging method
def write_file(file, soup):
	with open(file, 'a') as out:
		out.write(soup.prettify().encode('utf-8','replace'))

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/index').content)

anime_name_input = raw_input('Enter an anime: ')

animes = []

for link in soup.find_all(href=re.compile('(http:\\/\\/www\\.chia-anime\\.com/category/)')):
	anime_name = link.get('href')[35:]
	animes.append(anime_name)

anime_name, anime_score = process.extractOne(anime_name_input, animes)

if (anime_score >= 75):
	print 'Found ' + anime_name + '! (Score: ' + str(anime_score) + ').'
else:
	print 'Anime not found: ' + anime_name_input + '.'
	print 'Best match: ' + anime_name + ' (' + str(anime_score) + ').'
	quit()

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/category/' + anime_name).content)
episode = raw_input('Enter an episode: ')

anime_url = anime_name
if (anime_name[-5:] == 'anime'):
	anime_url = anime_name[:-6]

for link in soup.find_all(href=re.compile('(http:\\/\\/www\\.chia-anime\\.com/' + anime_name + '\\/' + anime_url + ')')):
	href = link.get('href')
	startIndex = href.find(anime_name) + len(anime_name) + len(anime_url) + 10
	endIndex = href.find('-', startIndex)
	if endIndex == -1:
		endIndex = len(href)
	if (link.get('href')[startIndex:endIndex] == episode):
		print 'Found episode ' + episode + '!'
		break;
else:
	print 'Episode not found: ' + episode + '.'
	quit()

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/' + anime_name + '/' + anime_url + '-episode-' + episode).content)
downloadPage = soup.find_all(href=re.compile('(http:\\/\\/download\\.animepremium\\.tv\\/get)'))[0].get('href')

soup = BeautifulSoup(requests.get(downloadPage).content)
for link in soup.find_all(href=re.compile('(animepremium\\.tv:8880\\/download)')):
	download_file(link.get('href'))
	break;
else:
	for link in soup.find_all(href=re.compile('.mp4\\/')):
		print 'http://download.animepremium.tv/get/' + link.get('href')
		download_file('http://download.animepremium.tv/get/' + link.get('href'))
		break;
	else:
		print 'Error.'
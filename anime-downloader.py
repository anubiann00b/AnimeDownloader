from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
import re
import requests
import sys

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

def download_anime(anime_name_input, episode):
    soup = BeautifulSoup(requests.get('http://www.chia-anime.com/index').content)

    animes = []

    # Get anime pages from index page
    for link in soup.find_all(href=re.compile(re.escape('http://www.chia-anime.com/category/'))):
        anime_name = link.get('href')[35:]
        animes.append(anime_name)

    # Get the best matching anime from the list compared to the user supplied name
    anime_name, anime_score = process.extractOne(anime_name_input, animes)

    if anime_score >= 75:
        print 'Found ' + anime_name + '! (Score: ' + str(anime_score) + ').'
    else:
        print 'Anime not found: ' + anime_name_input + '.'
        print 'Best match: ' + anime_name + ' (' + str(anime_score) + ').'
        quit()

    # Get the anime page
    soup = BeautifulSoup(requests.get('http://www.chia-anime.com/category/' + anime_name).content)

    # Deal with some weird naming stuff
    anime_url = anime_name
    if anime_name[-5:] == 'anime':
        anime_url = anime_name[:-6]

    urlHasEpisode = True

    # Get the anime episode download link
    for link in soup.find_all(href=re.compile(re.escape('http://www.chia-anime.com/' + anime_name + '/' + anime_url))):
        href = link.get('href')
        startIndex = href.find(anime_name) + len(anime_name) + len(anime_url) + 10
        endIndex = href.find('-', startIndex)
        if endIndex == -1:
            endIndex = len(href)
        if link.get('href')[startIndex:endIndex] == episode:
            print 'Found episode ' + episode + '!'
            break;
        else:
            startIndex -= 8 # No 'episode' in download URL
            if (link.get('href')[startIndex:endIndex] == episode):
                print 'Found episode ' + episode + '!'
                urlHasEpisode = False
                break;
    else:
        print 'Episode not found: ' + episode + '.'
        quit()

    # Get the episode page
    if urlHasEpisode:
        soup = BeautifulSoup(requests.get('http://www.chia-anime.com/' + anime_name + '/' + anime_url + '-episode-' + episode).content)
    else:
        soup = BeautifulSoup(requests.get('http://www.chia-anime.com/' + anime_name + '/' + anime_url + '-' + episode).content)

    # Find the download page link
    downloadPage = soup.find_all(href=re.compile(re.escape('http://download.animepremium.tv/get')))[0].get('href')

    # Get the direct link to the file, either in the form 'animepremium.tv:8880/download' or '.mp4'.
    soup = BeautifulSoup(requests.get(downloadPage).content)
    for link in soup.find_all(href=re.compile(re.escape('animepremium.tv:8880/download'))):
        download_file(link.get('href'))
        break;
    else:
        for link in soup.find_all(href=re.compile(re.escape('.mp4/'))):
            print 'http://download.animepremium.tv/get/' + link.get('href')
            download_file('http://download.animepremium.tv/get/' + link.get('href'))
            break;
        else:
            print 'Error.'

def show_help():
    print 'Usage: anime-downloader.py [anime] [episode]'

if len(sys.argv) != 3:
    show_help()
else:
    download_anime(sys.argv[1], sys.argv[2])
import requests
import re
from bs4 import BeautifulSoup
import subprocess

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

def write_file(file, soup):
	with open(file, 'a') as out:
		out.write(soup.prettify().encode('utf-8','replace'))

# download_file('http://cache2.animepremium.tv:8880/downloadcache/32t0CFNAjlzSRp2TCO_-dQ/1416971125/nxqvstt7mlkv-650x370.html.mp4/Sword-Art-Online-Episode-2-chia-anime.com.mp4');

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

#http://www.chia-anime.com/sword-art-online/sword-art-online-episode-5
for link in soup.find_all(href=re.compile('(http://www.chia-anime.com/' + anime_name + '/' + anime_name + ')')):
	if (link.get('href')[68:] == episode):
		print 'Found episode ' + episode + '!'
		break;
else:
	print 'Episode not found: ' + episode + '.'
	quit()

soup = BeautifulSoup(requests.get('http://www.chia-anime.com/' + anime_name + '/' + anime_name + '-episode-' + episode).content)
write_file("f2.txt", soup)
downloadPage = soup.find_all(href=re.compile('(http://download.animepremium.tv/get/)'))[0].get('href')

soup = BeautifulSoup(requests.get(downloadPage).content)
downloadLink = soup.find_all(href=re.compile('(animepremium.tv:8880/downloadcache)'))[0].get('href')

print 'Downloading!'
download_file(downloadLink)


'''
results = soup.find_all(href=re.compile('(http).*(pdf)'))
requests.adapters.HTTPAdapter(max_retries=3)
for link in results:
    url = (link.get('href'))
    url = url.strip()
    try:
        r = requests.get(url)
        fileForUrl = url.split('/')[-1]
        with open(fileForUrl, 'wb') as pdf:
            try:
                pdf.write(r.content)
            finally:
                pdf.close
    except:
        print 'oops'
        bashCommand = 'rm ' + fileForUrl
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    finally:
        print url
'''
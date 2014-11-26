import requests
import re
from bs4 import BeautifulSoup
import subprocess

# http://cache2.animepremium.tv:8880/downloadcache/32t0CFNAjlzSRp2TCO_-dQ/1416971125/nxqvstt7mlkv-650x370.html.mp4/Sword-Art-Online-Episode-2-chia-anime.com.mp4
# http://a.pomf.se/pgsiqq.exe

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

download_file("http://cache2.animepremium.tv:8880/downloadcache/32t0CFNAjlzSRp2TCO_-dQ/1416971125/nxqvstt7mlkv-650x370.html.mp4/Sword-Art-Online-Episode-2-chia-anime.com.mp4");

'''
results = soup.find_all(href=re.compile("(http).*(pdf)"))
requests.adapters.HTTPAdapter(max_retries=3)
for link in results:
    url = (link.get('href'))
    url = url.strip()
    try:
        r = requests.get(url)
        fileForUrl = url.split('/')[-1]
        with open(fileForUrl, "wb") as pdf:
            try:
                pdf.write(r.content)
            finally:
                pdf.close
    except:
        print "oops"
        bashCommand = "rm " + fileForUrl
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    finally:
        print url
'''
import requests
import re
import json
import sys

global artist
global url
def get_source():
    global url 
    url = "https://soundcloud.com/" + artist
    print url
    request = requests.get(url)
    if request.status_code == 200:
        print "Successfully downloaded source html"
        return request.text

def get_music_list(source):
    regex = 'url" href="/' + artist + '/' + '([^"]+)">([^<]+)<'
    match = re.findall(regex, source)
    music_list = {}
    for music_info in match:
        title = music_info[1]
        title = title.encode('ascii', 'ignore')
        link = music_info[0]
        link = link.encode('ascii', 'ignore')
        music_list[title] = link

    print "music list is " + str(music_list)
    #print match[0]
    #match[0]= [s.encode('ascii', 'ignore') for s in match[0]]
    
    return music_list

def download_music(subdomain,title):
    download_url = url + '/' + subdomain
    print download_url
    request = requests.get(download_url)
    if request.status_code != 200:
        print "Error, either song not found or internet connection failed"
        return

    regex = "https://w1.sndcdn.com/([^_]+)"
    match = re.findall(regex, request.text)
    match[0] = match[0].encode('ascii', 'ignore')
    download_url = "http://media.soundcloud.com/stream/" + str(match[0])
    print "Downloading from " + str(download_url)
    request = requests.get(download_url)
    
    with open(str(title)+".mp3", 'wb') as f:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    print "File downloaded successfully!"

    
def print_titles(music_list):
    print "Titles from artist are : "
    for titles in music_list:
        print titles


def main():
    print "Now in main"
    global artist
    artist = sys.argv[1]
    print "artist is " + artist
    source = get_source()
    music_list = get_music_list(source)
    print_titles(music_list)
    
    print "Choose music to download"
    title_to_grab = raw_input()
    download_music(music_list[title_to_grab], title_to_grab)  
    

main()

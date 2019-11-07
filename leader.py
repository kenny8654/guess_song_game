# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
import os,io

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

leaderBoard = []
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
for year in range(2010,2011):
    url = 'https://tw-pop-chart.blogspot.com/2014/02/kkbox-'+ str(year) +'.html?m=1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    song = soup.find_all('div')
    song = song[110]
    song = str(song).split('<tr>')
    del(song[len(song)-1])
    del(song[0])
    for s in song:
        s = re.split('<td>|</td>',s)
        # print(s[3],s[5])
        leaderBoard.append(s[3]+' '+s[5])
# print(leaderBoard)


api_service_name = "youtube"
api_version = "v3"
api_token = 'YOUR_KEY'
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_token
)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './music/'+'%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

for leader in leaderBoard:
    print(leader)
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=leader 

    )
    response = request.execute()
    videoID = response["items"][0]['id']['videoId']
    f = open('songList2.txt','a+') 
    data = '\n' + str(videoID) + ',' + leader
    f.write(str(data))
    if not os.path.isfile(videoID+'.mp3'):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=' + videoID])

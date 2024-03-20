import os
import shutil
import re

from googleapiclient.discovery import build

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time

# type in your own api key
api_key = ""

def playlistVideosToUrl(playlistId):
    youtube = build("youtube", "v3", developerKey=api_key)
    
    video_ids = []
    video_titles = []
    pageToken = None
    
    bad_chars = ['<', '>', ':', "\"", "/", "\\", "\|", "\?", "*"]
    
    while (True):
        video_request = youtube.playlistItems().list(part="contentDetails, snippet", playlistId=playlistId, pageToken=pageToken, maxResults=50)
        video_response = video_request.execute()
        
        for item in video_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
            video_title = item["snippet"]["title"]
            
            for c in bad_chars:
                video_title = video_title.replace(c, '_')
            
            video_titles.append(video_title)
        
        if (video_response.get("nextPageToken") == None):
            break
        
        pageToken = video_response["nextPageToken"]
    
    youtube_prefix = "https://youtu.be/"
    
    video_urls = []
    
    for ids in video_ids:
        video_urls.append(youtube_prefix + ids)

    return (video_urls, video_titles)

def urlToMp3(youtube_urls, youtube_titles):    
    path = os.getcwd()
    
    if os.path.exists("download_folder"):
        shutil.rmtree("download_folder")
    os.mkdir("download_folder")
    
    if os.path.exists("mp3_folder"):
        shutil.rmtree("mp3_folder")
    os.mkdir("mp3_folder")

    download_path = os.path.join(path, "download_folder")
    mp3_path = os.path.join(path, "mp3_folder")
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    
    
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://cobalt.tools/")
    driver.implicitly_wait(10)
    
    audio_mode = driver.find_element(By.ID, "audioMode-true")
    audio_mode.click()
    
    input = driver.find_element(By.ID, "url-input-area")
    
    download_regex = re.compile('.*crdownload$')
    mp3_prefix = ".mp3"
    
    
    files_downloaded = 0
    for url, title in zip(youtube_urls, youtube_titles):
        input.clear()
        input.send_keys(url)
        
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, "download-button")))
        download_button = driver.find_element(By.ID, "download-button")
        download_button.click()
        
        if (len(driver.find_elements(By.XPATH, "//*[contains(@class, 'close-error switch') and text()='got it']")) > 0):
            try:
                driver.find_element(By.XPATH, "//*[contains(@class, 'close-error switch') and text()='got it']").click()
            except:
                pass
        
        time.sleep(5)
        
        while (True):
            download = os.listdir(download_path)[0]
            match = download_regex.match(download)

            if (not(match)):
                break
        
        files_downloaded += 1
        print(f"Finished downloading {files_downloaded}/{len(youtube_urls)} file")
        
        old_title = os.listdir(download_path)[0]
        
        old_file = os.path.join(download_path, old_title)
        new_file = os.path.join(mp3_path, title) + mp3_prefix
        os.rename(old_file, new_file)
        
        shutil.rmtree("download_folder")
        os.mkdir("download_folder")

    print("--------------DONE!--------------")
    print("Mp3s can be found in \"mp3_folder\"")
    
    return

if __name__ == "__main__":
    playlistUrl = input("Enter your playlist url: ")
    playlistId_regex = re.compile('.*=(.*)')
    playlistId = playlistId_regex.search(playlistUrl).group(1)
    print(playlistId)
    video_urls, video_titles = playlistVideosToUrl(playlistId)
    urlToMp3(video_urls, video_titles)
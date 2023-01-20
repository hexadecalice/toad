from pytube import YouTube
from flask import session 
import os
import moviepy.editor as mp 

forbidden_chars = '"*\\/\'.|?:<>'

def sanitizeName(forbidden_chars, name):
    for char in forbidden_chars:
        name = name.replace(char, "")
    return name 
        
        

def slurp(savepath, vid, filetype):
    try:
        title = "\\" + session.get('title', None) + ".mp4"
        os.remove(vidpath + title)
    except: 
        print("no file found")
    
    
    yt = YouTube(vid)
    
    #Filter out mp4s by 360p and sanitizes the video title for windows 
    mp4_files = yt.streams.filter(file_extension="mp4")
    filteredmp4 = mp4_files.get_by_resolution("360p")
    cleanName = sanitizeName(forbidden_chars, filteredmp4.title)
    
    
    filteredmp4.download(savepath, cleanName + ".mp4")
    
    #Use moviepy to convert downloaded mp4 to audio and save under the same name
    #Clean up the unneeded mp4 file
    if filetype == ".mp3":
        clip = mp.VideoFileClip(savepath + "\\" + cleanName + ".mp4")
        clip.audio.write_audiofile(savepath + "\\" + cleanName + ".mp3")
        os.remove(savepath + "\\" + cleanName + ".mp4")
    
    #Passing the cleaned name to the download endpoint
    session['title'] = cleanName + filetype
    session['filetype'] = filetype
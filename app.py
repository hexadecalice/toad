from flask import Flask, render_template, url_for, request, redirect, send_from_directory, session, send_file
import os
import io
import tongue
import moviepy.editor as mp 

vidpath = "C:\\Users\\alice\\Desktop\\toad\\videos"
mp3 = False
app = Flask(__name__)
app.secret_key = "hello losererererererere"
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        vid = request.form["vidlink"]
        file_format = request.form["filetype"]
        tongue.slurp(vidpath, vid, file_format)
        return redirect(url_for('download'))
        
    return render_template('index.html')

@app.route('/download')
def download():
    filename = session.get('title', None)
    
    #Saves the video to local memory, then sends the video/audio held in memory 
    #Deletes mp4 file and sends video from the local memory 
    videoMemory = io.BytesIO()
    vidLocation = vidpath + "\\" + filename
    with open(vidLocation,'rb') as f: 
        videoMemory.write(f.read())
    videoMemory.seek(0)
    
    
    
    os.remove(vidLocation)
    if session.get('filetype', None) == ".mp3":
        return send_file(videoMemory, mimetype="audio/mpeg", as_attachment=True, download_name=filename)
    elif session.get('filetype', None) == ".mp4":
        return send_file(videoMemory, mimetype="video/mp4", as_attachment=True, download_name=filename)
    
    
    

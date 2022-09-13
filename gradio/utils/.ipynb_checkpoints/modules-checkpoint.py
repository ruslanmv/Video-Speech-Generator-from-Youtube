# Modules for the Video Messsage Generator From Youtube

from IPython.display import HTML, Audio
from base64 import b64decode
import numpy as np
from scipy.io.wavfile import read as wav_read
import io
import ffmpeg
from pytube import YouTube
import random
from subprocess import call
import os
from datetime import datetime


def time_between(t1, t2):
    FMT = '%H:%M:%S'
    t1 = datetime.strptime(t1, FMT)
    t2 = datetime.strptime(t2, FMT)
    delta = t2 - t1
    return str(delta)

def download_video(url):

    print("Downloading...")
    local_file = (
        YouTube(url)
        .streams.filter(progressive=True, file_extension="mp4")
        .first()
        .download(filename="youtube{}.mp4".format(random.randint(0, 10000)))
    )
    print("Downloaded")
    return local_file
  # download(output_path=destination, filename="name.mp4")
    
    
def download_youtube(url):
    #Select a Youtube Video
    #find youtube video id
    from urllib import parse as urlparse
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    YOUTUBE_ID = query["v"][0]
    url_download ="https://www.youtube.com/watch?v={}".format(YOUTUBE_ID)
    # download the youtube with the given ID
    os.system("{} youtube-dl -f  mp4 --output youtube.mp4 '{}'".format(env,url_download))
    return "youtube.mp4"

       
    
def cleanup():
    import pathlib
    import glob
    types = ('*.mp4','*.mp3', '*.wav') # the tuple of file types
    #Finding mp4 and wave files
    junks = []
    for files in types:
        junks.extend(glob.glob(files))
    try:    
        # Deleting those files
        for junk in junks:
            print("Deleting",junk)
            # Setting the path for the file to delete
            file = pathlib.Path(junk)
            # Calling the unlink method on the path
            file.unlink()               
    except Exception:
        print("I cannot delete the file because it is being used by another process")
        
        
def clean_data():
    # importing all necessary libraries
    import sys, os
    # initial directory
    home_dir = os.getcwd()
    # some non existing directory
    fd = 'sample_data/'
    # Join various path components
    path_to_clean=os.path.join(home_dir,fd)
    print("Path to clean:",path_to_clean)
    # trying to insert to false directory
    try:
        os.chdir(path_to_clean)
        print("Inside to clean", os.getcwd())
        cleanup()
    # Caching the exception
    except:
        print("Something wrong with specified\
        directory. Exception- ", sys.exc_info())
    # handling with finally
    finally:
        print("Restoring the path")
        os.chdir(home_dir)
        print("Current directory is-", os.getcwd())
        
def youtube_trim(url,start,end):
    #cancel previous youtube
    cleanup()
    #download youtube
    #download_youtube(url) # with youtube-dl (slow)
    input_videos=download_video(url)
    # Get the current working directory
    parent_dir = os.getcwd()
    # Trim the video (start, end) seconds
    start =  start
    end =  end
    #Note: the trimmed video must have face on all frames
    #interval = end - start
    interval = time_between(start, end)
    #trimmed_video= parent_dir+'/sample_data/input_vid{}.mp4'.format(random.randint(0, 10000))
    #trimmed_audio= parent_dir+'/sample_data/input_audio{}.mp3'.format(random.randint(0, 10000))
    trimmed_video= parent_dir+'/sample_data/input_video.mp4'
    trimmed_audio= parent_dir+'/sample_data/input_audio.mp3'
    #delete trimmed if already exits
    clean_data()
    #call(["rm","-f",trimmed_audio])
    #call(["rm","-f",trimmed_video])
    
    #!rm -f {trimmed_video}
    # cut the video  
    call(["ffmpeg","-y","-i",input_videos,"-ss", start,"-t",interval,"-async","1",trimmed_video])
    #!ffmpeg -y -i youtube.mp4 -ss {start} -t {interval} -async 1 {trimmed_video}
    # cut the audio
    call(["ffmpeg","-i",trimmed_video, "-q:a", "0", "-map","a",trimmed_audio])
    #Preview trimmed video
    #clear_output()
    print("Trimmed Video+Audio")
    return trimmed_video, trimmed_audio

def create_video(Text,Voicetoclone):
    out_audio=greet(Text,Voicetoclone)
    current_dir=os.getcwd()
    clonned_audio = os.path.join(current_dir, out_audio)
    
    #Start Crunching and Preview Output
    #Note: Only change these, if you have to
    pad_top =  0#@param {type:"integer"}
    pad_bottom =  10#@param {type:"integer"}
    pad_left =  0#@param {type:"integer"}
    pad_right =  0#@param {type:"integer"}
    rescaleFactor =  1#@param {type:"integer"}
    nosmooth = False #@param {type:"boolean"}
    
    out_name ="result_voice_{}.mp4".format(random.randint(0, 10000))
    out_file="../"+out_name
    
    if nosmooth == False:
        os.system('{} cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "../sample_data/input_video.mp4" --audio "../out/clonned_audio.wav" --outfile {} --pads {} {} {} {} --resize_factor {}'.format(env,out_file,pad_top ,pad_bottom ,pad_left ,pad_right ,rescaleFactor))
    else:
        os.system('{} cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "../sample_data/input_video.mp4" --audio "../out/clonned_audio.wav" --outfile {} --pads {} {} {} {} --resize_factor {} --nosmooth'.format(env,out_file,pad_top ,pad_bottom ,pad_left ,pad_right ,rescaleFactor))

    #clear_output()
    print("Creation of Video done")
    return out_name


def time_format_check(input1):
    timeformat = "%H:%M:%S"
    #input1 = input("At what time did sensor 1 actuate? ")
    try:
        validtime = datetime.strptime(input1, timeformat)
        print("The time format is valid", input1)
        #Do your logic with validtime, which is a valid format
        return False
    except ValueError:
        print("The time {}  has not valid format hh:mm:ss".format(input1))
        return True
    
    
def to_seconds(datetime_obj):
    from datetime import datetime
    time =datetime_obj
    date_time = datetime.strptime(time, "%H:%M:%S")
    a_timedelta = date_time - datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()
    return seconds
    
    
def validate_youtube(url):
    #This creates a youtube objet
    try:
        yt = YouTube(url)  
    except Exception:
        print("Hi there URL seems invalid")
        return True, 0
    #This will return the length of the video in sec as an int
    video_length = yt.length
    if    video_length > 600:
        print("Your video is larger than 10 minutes")
        return True, video_length
    else:
        print("Your video is less than 10 minutes")
        return False, video_length
    
    
def video_generator(text_to_say,url,initial_time,final_time):
    print('Checking the url',url)
    check1, video_length = validate_youtube(url)
    if check1 is True: return "./demo/tryagain2.mp4"
    check2 = validate_time(initial_time,final_time, video_length)
    if check2 is True: return "./demo/tryagain0.mp4"
    trimmed_video, trimmed_audio=youtube_trim(url,initial_time,final_time)
    voicetoclone=trimmed_audio
    print(voicetoclone)
    outvideo=create_video(text_to_say,voicetoclone)
    #Preview output video
    print("Final Video Preview")
    final_video= parent_dir+'/'+outvideo
    print("DONE")
    #showVideo(final_video)
    return final_video


def validate_time(initial_time,final_time,video_length):
    is_wrong1=time_format_check(initial_time)
    is_wrong2=time_format_check(final_time) 
    #print(is_wrong1,is_wrong2)
    if is_wrong1 is False and is_wrong2 is False:
        delta=time_between(initial_time,final_time)
        if len(str(delta)) > 8:
            print("Final Time is Smaller than Initial Time: t1>t2")
            is_wrong = True
            return is_wrong
        else:
            print("OK")
            is_wrong=False
            if int(to_seconds(delta)) > 300 :
                print("The trim is larger than 5 minutes")
                is_wrong = True
                return is_wrong
            
            elif int(to_seconds(delta)) > video_length :
                print("The trim is larger than video lenght")
                is_wrong = True
                return is_wrong             
            else:
                return  is_wrong
            
    else:
        print("Your time format is invalid")
        is_wrong = True
        return is_wrong
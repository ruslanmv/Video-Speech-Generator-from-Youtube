import gradio as gr
import os
import sys
#Installation of libraries
EC2_INSTANCE = True
if EC2_INSTANCE : os.system('cd scripts && sh install.sh')
os.system('python installation.py')

TTS_PATH = "TTS/"
# add libraries into environment
sys.path.append(TTS_PATH) # set this if TTS is not installed globally
VOICE_PATH = "utils/"
# add libraries into environment
sys.path.append(VOICE_PATH) # set this if modules and voice are not installed globally
from utils.modules import *
from utils.voice import *

#Definition Web App in Gradio

text_to_say=gr.inputs.Textbox(label='What would you like the voice to say? (max. 2000 characters per request)')
url =gr.inputs.Textbox(label = "Enter the YouTube URL below:")
initial_time = gr.inputs.Textbox(label='Initial time of trim? (format: hh:mm:ss)')
final_time= gr.inputs.Textbox(label='Final time to trim? (format: hh:mm:ss)')
demo = gr.Interface(fn = video_generator,
            inputs = [text_to_say,url,initial_time,final_time],
            outputs = 'video', 
            verbose = True,
            title = 'Video Speech Generator from Youtube Videos',
            description = 'A simple application that replaces the original speech of the video by your text. Wait one minute to process.',
            article = 
                        '''<div>
                            <p style="text-align: center"> 
                            All you need to do is to paste the Youtube link and 
                            set the initial time and final time of the real speach.
                            (The limit of the trim is 5 minutes and not larger than video length)
                            hit submit, then wait for compiling.
                            After that click on Play/Pause for listing to the video. 
                            The video is saved in an mp4 format.
                             For more information visit <a href="https://ruslanmv.com/">ruslanmv.com</a>
                            </p>
                        </div>''',

           examples = [['I am clonning your voice, Charles!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=xw5dvItD5zY", 
                        "00:00:01","00:00:10"],
                        ['I am clonning your voice, Jim Carrey!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=uIaY0l5qV0c",
                        "00:00:29",  "00:01:05"],
                        ['I am clonning your voice, Mark Zuckerberg!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=AYjDIFrY9rc",
                        "00:00:11", "00:00:44"],
                        ['I am clonning your voice, Ronald Reagan!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=iuoRDY9c5SQ",
                        "00:01:03",  "00:01:22"], 
                        ['I am clonning your voice, Elon Musk!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=IZ8JQ_1gytg",
                        "00:00:10",  "00:00:43"],
                        ['I am clonning your voice, Hitler!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=F08wrLyH5cs",
                        "00:00:15",  "00:00:40"],
                         ['I am clonning your voice, Alexandria!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=Eht6oIkzkew",
                        "00:00:02",  "00:00:30"], 
                         ['I am clonning your voice, Deborah!. Machine intelligence is the last invention that humanity will ever need to make.',
                        "https://www.youtube.com/watch?v=qbq4_Swj0Gg",
                        "00:00:03",  "00:0:44"],
                        ]           
            )
demo.launch()
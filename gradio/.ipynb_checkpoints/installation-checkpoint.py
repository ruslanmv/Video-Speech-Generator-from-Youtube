# Import the os module
import os
from utils.default_models import ensure_default_models
from pathlib import Path
Sagemaker = True
if Sagemaker :
    env='source activate python3 && conda activate VideoMessage &&'
else:
    env='' 
## Step 1. Setup of the dependencies
is_first_time = True

#Install dependency
# Download pretrained model

# Get the current working directory
parent_dir = os.getcwd()
print(parent_dir)
if is_first_time:
    # Directory 
    directory = "sample_data"
    # Path 
    path = os.path.join(parent_dir, directory) 
    print(path)
    try:
        os.mkdir(path)
        print("Directory '% s' created" % directory) 
    except Exception:
         print("Directory '% s'was already created" % directory)
if is_first_time:
    os.system('git clone https://github.com/Rudrabha/Wav2Lip')
    os.system('cd Wav2Lip &&{} pip install  -r requirements.txt'.format(env))
    ## Load the models one by one.
    print("Preparing the models of Wav2Lip")
    ensure_default_models(Path("Wav2Lip"))    
    os.system('git clone https://github.com/Edresson/Coqui-TTS -b multilingual-torchaudio-SE TTS')
    os.system('{} pip install -q -e TTS/'.format(env))
    os.system('{} pip install -q torchaudio==0.9.0'.format(env))
    os.system('{} pip install -q youtube-dl'.format(env))
    os.system('{} pip install ffmpeg-python'.format(env))
    os.system('{} pip install gradio==3.0.4'.format(env))
    os.system('{} pip install pytube==12.1.0'.format(env))
    os.system('git clone https://github.com/Cloud-Data-Science/Voice-Cloning VOICE')
    os.system('cd VOICE &&{} pip install  -r requirements.txt'.format(env))
    os.system('mv ./VOICE/* .')
    os.system('rm -r VOICE -f')
    os.system('{} pip install opencv-contrib-python-headless==4.1.2.30'.format(env))
print("Installation repositories DONE!!")
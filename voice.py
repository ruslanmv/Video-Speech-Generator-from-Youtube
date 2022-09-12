import gradio as gr
import os
import sys
TTS_PATH = "TTS/"
# add libraries into environment
sys.path.append(TTS_PATH) # set this if TTS is not installed globally
import os
import string
import time
import argparse
import json
import numpy as np
import IPython
from IPython.display import Audio
import torch
from TTS.tts.utils.synthesis import synthesis
from TTS.tts.utils.text.symbols import make_symbols, phonemes, symbols
try:
  from TTS.utils.audio import AudioProcessor
except:
  from TTS.utils.audio import AudioProcessor
from TTS.tts.models import setup_model
from TTS.config import load_config
from TTS.tts.models.vits import *  
OUT_PATH = 'out/'
# create output path
os.makedirs(OUT_PATH, exist_ok=True)
import os
# Get the current working directory
parent_dir = os.getcwd()
print(parent_dir)
# model vars 
MODEL_PATH = parent_dir+'/best_model.pth.tar'
CONFIG_PATH = parent_dir+'/config.json'
TTS_LANGUAGES = parent_dir+"/language_ids.json"
TTS_SPEAKERS = parent_dir+"/speakers.json"
USE_CUDA = torch.cuda.is_available()  
# load the config
C = load_config(CONFIG_PATH)
# load the audio processor
ap = AudioProcessor(**C.audio)
speaker_embedding = None
C.model_args['d_vector_file'] = TTS_SPEAKERS
C.model_args['use_speaker_encoder_as_loss'] = False
model = setup_model(C)
model.language_manager.set_language_ids_from_file(TTS_LANGUAGES)
# print(model.language_manager.num_languages, model.embedded_language_dim)
# print(model.emb_l)
cp = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
# remove speaker encoder
model_weights = cp['model'].copy()
for key in list(model_weights.keys()):
  if "speaker_encoder" in key:
    del model_weights[key]
model.load_state_dict(model_weights)
model.eval()
if USE_CUDA:
    model = model.cuda()
# synthesize voice
use_griffin_lim = False
os.system('pip install -q pydub ffmpeg-normalize')
CONFIG_SE_PATH = "config_se.json"
CHECKPOINT_SE_PATH = "SE_checkpoint.pth.tar"
from TTS.tts.utils.speakers import SpeakerManager
from pydub import AudioSegment
import librosa
SE_speaker_manager = SpeakerManager(encoder_model_path=CHECKPOINT_SE_PATH, encoder_config_path=CONFIG_SE_PATH, use_cuda=USE_CUDA)
def compute_spec(ref_file):
  y, sr = librosa.load(ref_file, sr=ap.sample_rate)
  spec = ap.spectrogram(y)
  spec = torch.FloatTensor(spec).unsqueeze(0)
  return spec
  
def greet(Text,Voicetoclone):
    text= "%s" % (Text)
    reference_files= "%s" % (Voicetoclone)
    print("path url")
    print(Voicetoclone)
    sample= str(Voicetoclone)
    size= len(reference_files)*sys.getsizeof(reference_files)
    size2= size / 1000000
    if (size2 > 0.012) or len(text)>2000:
      message="File is greater than 30mb or Text inserted is longer than 2000 characters. Please re-try with smaller sizes."
      print(message)
      raise SystemExit("File is greater than 30mb. Please re-try or Text inserted is longer than 2000 characters. Please re-try with smaller sizes.")
    else:
      os.system('ffmpeg-normalize $sample -nt rms -t=-27 -o $sample -ar 16000 -f')
      reference_emb = SE_speaker_manager.compute_d_vector_from_clip(reference_files)
      model.length_scale = 1  # scaler for the duration predictor. The larger it is, the slower the speech.
      model.inference_noise_scale = 0.3 # defines the noise variance applied to the random z vector at inference.
      model.inference_noise_scale_dp = 0.3 # defines the noise variance applied to the duration predictor z vector at inference.
      text = text
      model.language_manager.language_id_mapping
      language_id = 0
    
      print(" > text: {}".format(text))
      wav, alignment, _, _ = synthesis(
                        model,
                        text,
                        C,
                        "cuda" in str(next(model.parameters()).device),
                        ap,
                        speaker_id=None,
                        d_vector=reference_emb,
                        style_wav=None,
                        language_id=language_id,
                        enable_eos_bos_chars=C.enable_eos_bos_chars,
                        use_griffin_lim=True,
                        do_trim_silence=False,
                    ).values()
      print("Generated Audio")
      IPython.display.display(Audio(wav, rate=ap.sample_rate))
      #file_name = text.replace(" ", "_")
      #file_name = file_name.translate(str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
      file_name='clonned_audio.wav'
      out_path = os.path.join(OUT_PATH, file_name)
      print(" > Saving output to {}".format(out_path))
      ap.save_wav(wav, out_path)
      return out_path

#demo = gr.Interface(
#    fn=greet, 
#    inputs=[gr.inputs.Textbox(label='What would you like the voice to say? (max. 2000 characters per request)'),gr.Audio(type="filepath",         source="upload",label='Please upload a voice to clone (max. 30mb)')],
#    outputs="audio",
#    )
#demo.launch()
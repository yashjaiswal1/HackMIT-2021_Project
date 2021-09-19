from flask import *
import sys
import os
from werkzeug.utils import secure_filename

# input and output .wav audio files will go here
UPLOAD_FOLDER = 'static/'

app = Flask(__name__,template_folder="template/",static_folder="static/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    # ensures no embeddings are duplicated or mixed up due to browser caching!
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def htmloader(text,inputaudio,outputaudio):
    x = ""
    x+="Narration Text: <p>"+text+"</p><br>"
    x+="Narration Audio:<br>"
    x+="<audio id='outputAudio' controls>"
    x+="  <source src='"+str(outputaudio)+"' type='audio/wav'>"
    x+="</audio><br>"
    x+='<div class="form-group col-sm-3"><label for="exampleFormControlSelect1">Set audio speed</label><select class="form-control" id="speedForm" onchange="setSpeed(value)"><option>0.50</option><option>0.75</option><option selected>1.00</option><option>1.25</option><option>1.50</option></select>'
    return x

def isAllowedFile(filename):
    # checks if file extension is allowed
    # currently supporting only .wav format
    return filename[-4:].lower() == ".wav"

def uploadFile():
    # handles file upload
    
    file_logs = []      # file logs will be appended here
    if request.method == 'POST':
        f = request.files['file']
        if isAllowedFile(f.filename):
            f.save(UPLOAD_FOLDER+secure_filename(f.filename))
            file_logs.append("File uploaded successfully!")
            file_logs.append(UPLOAD_FOLDER+secure_filename(f.filename))
            return file_logs
        else:
            file_logs.append("Unexpected file")
            return file_logs

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/author',methods=['GET', 'POST'])
def author():
    print("works")
    # return render_template("author.html")
    file_log_output = uploadFile()

    # input text (default value)
    input_text = "Enter the text to be narrated here!"
    if request.method == 'POST':
        # overwrite default value
        input_text = request.form["textarea"]

    if str(file_log_output)=="None":
        return render_template("author.html",output="")
    else:
        from encoder.params_model import model_embedding_size as speaker_embedding_size
        from utils.argutils import print_args
        from synthesizer.inference import Synthesizer
        from encoder import inference as encoder
        from vocoder import inference as vocoder
        from pathlib import Path
        import numpy as np
        import soundfile as sf
        import librosa
        import argparse
        import torch
        try:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            
            # update the model with newer pretrained model .pt files
            parser.add_argument("-e", "--enc_model_output_file_path", type=Path,default="encoder/saved_models/pretrained.pt")
            parser.add_argument("-s", "--syn_model_dir", type=Path,default="synthesizer/saved_models/pretrained/pretrained.pt")
            parser.add_argument("-v", "--voc_model_output_file_path", type=Path,default="vocoder/saved_models/pretrained/pretrained.pt")
            parser.add_argument("--low_mem", action="store_true")
            
            # collect all args
            args = parser.parse_args()
            print_args(args, parser)
            
            encoder.load_model(args.enc_model_output_file_path)
            print(args)
            
            # replace tacotron model with the newer pre-trained model
            # synthesizer = Synthesizer(args.syn_model_dir.joinpath("taco_pretrained"))
            synthesizer = Synthesizer(args.syn_model_dir)
            vocoder.load_model(args.voc_model_output_file_path)

            input_file_path = file_log_output[1]
            preprocessed_wav = encoder.preprocess_wav(input_file_path)
            original_wav, sampling_rate = librosa.load(input_file_path)
            preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
            embed = encoder.embed_utterance(preprocessed_wav)
            print("Embedding created...")
            text = str(input_text)
            texts = [text]
            embeds = [embed]
            specs = synthesizer.synthesize_spectrograms(texts, embeds)
            spec = specs[0]
            print("Mel spectrogram created...")
            print("Synthesizing the waveform:")
            generated_wav = vocoder.infer_waveform(spec)
            generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

            output_file_path = "static/output.wav"
            print(generated_wav.dtype)
            print(librosa.__version__)

            # using SoundFile to gather samplerate
            sr = sf.info(output_file_path).samplerate
            # print("SR = " + str(sr))      16000
            # print("Synth SR = " + str(synthesizer.sample_rate))   16000
            
            # using SoundFile to create the output.wav file
            sf.write(output_file_path, generated_wav.astype(np.float32), sr)
            print("\nSaved output as %s\n\n" % output_file_path)
            return render_template("author.html",output=htmloader(text,file_log_output[1],output_file_path))
        except Exception as e:
            return render_template("author.html",output="Caught exception: %s" % repr(e))


@app.route('/',methods=['GET', 'POST'])
def main():
    print("called main route...")
    file_log_output = uploadFile()

    # input text (default value)
    input_text = "Hello! I will be your narrator for today. Let's get started!"
    if request.method == 'POST':
        # overwrite default value
        input_text = request.form["textarea"]

    if str(file_log_output)=="None":
        return render_template("index.html",output="")
    else:
        from encoder.params_model import model_embedding_size as speaker_embedding_size
        from utils.argutils import print_args
        from synthesizer.inference import Synthesizer
        from encoder import inference as encoder
        from vocoder import inference as vocoder
        from pathlib import Path
        import numpy as np
        import soundfile as sf
        import librosa
        import argparse
        import torch
        try:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            
            # update the model with newer pretrained model .pt files
            parser.add_argument("-e", "--enc_model_output_file_path", type=Path,default="encoder/saved_models/pretrained.pt")
            parser.add_argument("-s", "--syn_model_dir", type=Path,default="synthesizer/saved_models/pretrained/pretrained.pt")
            parser.add_argument("-v", "--voc_model_output_file_path", type=Path,default="vocoder/saved_models/pretrained/pretrained.pt")
            parser.add_argument("--low_mem", action="store_true")
            
            # collect all args
            args = parser.parse_args()
            print_args(args, parser)
            
            encoder.load_model(args.enc_model_output_file_path)
            print(args)
            
            # replace tacotron model with the newer pre-trained model
            # synthesizer = Synthesizer(args.syn_model_dir.joinpath("taco_pretrained"))
            synthesizer = Synthesizer(args.syn_model_dir)
            vocoder.load_model(args.voc_model_output_file_path)

            input_file_path = file_log_output[1]
            preprocessed_wav = encoder.preprocess_wav(input_file_path)
            original_wav, sampling_rate = librosa.load(input_file_path)
            preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
            embed = encoder.embed_utterance(preprocessed_wav)
            print("Embedding created...")
            text = str(input_text)
            texts = [text]
            embeds = [embed]
            specs = synthesizer.synthesize_spectrograms(texts, embeds)
            spec = specs[0]
            print("Mel spectrogram created...")
            print("Synthesizing the waveform:")
            generated_wav = vocoder.infer_waveform(spec)
            generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

            output_file_path = "static/output.wav"
            print(generated_wav.dtype)
            print(librosa.__version__)

            # using SoundFile to gather samplerate
            sr = sf.info(output_file_path).samplerate
            # print("SR = " + str(sr))      16000
            # print("Synth SR = " + str(synthesizer.sample_rate))   16000
            
            # using SoundFile to create the output.wav file
            sf.write(output_file_path, generated_wav.astype(np.float32), sr)
            print("\nSaved output as %s\n\n" % output_file_path)
            return render_template("index.html",output=htmloader(text,file_log_output[1],output_file_path))
        except Exception as e:
            return render_template("index.html",output="Caught exception: %s" % repr(e))


if __name__ == "__main__":
    app.run(debug=True)
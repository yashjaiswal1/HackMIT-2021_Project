## Readme

VoiceBook is a venture to bridge the gap between text-content and audio-content. It brings you books and texts to audio in voice of the person you choose.
It solves many socio-economic problems. Audiobooks are expensive and takes lot of time and setup to finish. With the modern world shifting to virtual technologies, the conventional textbooks are getting out of demand. Reading book is no more a regular task like it used to be.
People prefer speech over texts now. 

Voicebook is a AI platform that converts text to speech. It provides the customers with two options. First option is an Author logging in the platform to provide his sample audio file along with texts. The resultant speech produced is then delivered in his voice.
Later option is that any customer joins the platform along with the texts and choose voice from sample voices already provided on the platform to avoid the deepfakes. 

## Working

The Product uses SV2TTS model, a three-stage deep learning framework. 
Mel Spectrogram, is a Spectrogram with the Mel Scale as its y axis where Mel Scale is constructed such that sounds of equal distance from each other on the Mel Scale, also “sound” to humans as they are equal in distance from one another.
   
   ##### Model

Speaker Encoder takes in the audio as mel spectrogram frames to produce embedding which captures how speaker sounds. 
The synthesizer analyzes text input to create mel spectrograms.
Synthesizer’s encoder concatenates its encoding of the phoneme sequence with the speaker embedding, 
and decoder and attention parts of the synthesizer recurrently generates mel spectrogram, 
which the vocoder later converts into sound.

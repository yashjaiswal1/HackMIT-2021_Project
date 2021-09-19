## VoiceBooks

VoiceBooks aims to make audible formats easy to create and accessible to everyone. From people with ADHD, upcoming authors who don't speak English, and kids who prefer to follow along with audiobooks, Voicebook provides a voice for everyone.

To use the site, authors can submit a 5-second sample of your voice and our AI model generates an audiobook of the selected text. For casual users, Voicebook provides a selection of voice samples and the input text is converted into a narration file.

## Working

The project uses an [open-source voice-cloning (pre-trained) SV2TTS model](https://github.com/CorentinJ/Real-Time-Voice-Cloning), a three-stage deep learning framework, hosted locally in the backend over a Flask server. The front-end user interface of the application has been built using HTML, CSS, Jinja, vanilla JS, and Bootsrap. We have also made use of Figma to design [wireframes](https://www.figma.com/file/UsBYByGMe0KRe2Fg6foxy4/HackMIT-2021-Wireframe?node-id=0%3A1).

## Model

- Speaker Encoder takes in the audio as mel spectrogram frames to produce embedding which captures how the speaker sounds.
- The synthesizer analyzes text input to create mel spectrograms.
- Synthesizer’s encoder concatenates its encoding of the phoneme sequence with the speaker embedding, and decoder and attention parts of the synthesizer recurrently generates mel spectrogram, which the vocoder later converts into sound.

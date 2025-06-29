# Medical Consultation Transcription & Summarization

This is a personal project that uses AI to transcribe and summarize medical consultation audios. It provides a simple web interface built with Streamlit, aiming to help healthcare professionals document appointments more efficiently.

## 🚀 Features

- 📁 Upload audio files (.mp3)
- 🧠 Automatic transcription using OpenAI Whisper
- 📝 Summarization of the transcribed text
- 💻 Web interface with Streamlit

## 🛠️ Installation

Clone this repo and install the dependencies:

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
pip install -r requirements.txt
```

**Note:** You’ll need an OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

## ▶️ How to Use

### Web Interface (Streamlit)
```bash
streamlit run app_streamlit.py
```

### Command Line
```bash
python main.py
python main_os.py -> To use OpenAI Whisper locally
```

## 📌 Tech Stack

- Python
- Streamlit
- OpenAI Whisper API
- Hugging Face Transformers (optional, for summarization)
- ffmpeg / pydub (audio handling)

## 📄 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

## 🤝 Contributions

Feel free to open issues or submit pull requests. I'm happy to improve this with your help!
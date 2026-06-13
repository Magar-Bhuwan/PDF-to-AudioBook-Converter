# from pypdf import PdfReader
# import pyttsx3

# reader = PdfReader("Osho.pdf")

# text = ""
# for page in reader.pages:
#     text += page.extract_text() or ""

# engine = pyttsx3.init()
# engine.save_to_file(text, "audiobook.mp3")
# engine.runAndWait()

# print("Audiobook Created!")


import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
import os
import base64

# ---------------------------
# Extract text from PDF
# ---------------------------
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ---------------------------
# Convert text to MP3
# ---------------------------
def text_to_audio(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# ---------------------------
# Download helper
# ---------------------------
def get_binary_file_downloader_html(file_path, file_label="File"):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/mp3;base64,{b64}" download="{file_path}">📥 Download {file_label}</a>'
    return href

# ---------------------------
# UI
# ---------------------------
st.title("📄➡️🔊 PDF to MP3 Converter")
st.write("Upload a PDF file and convert it into an audiobook.")

pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])

if pdf_file is not None:
    st.success("PDF uploaded successfully!")

    if st.button("Convert to Audio"):
        with st.spinner("Extracting text..."):
            text = extract_text(pdf_file)

        if not text.strip():
            st.error("No text found in PDF!")
        else:
            with st.spinner("Converting to MP3..."):
                audio_file = text_to_audio(text)

            st.success("Conversion completed!")

            st.audio(audio_file)

            st.markdown(
                get_binary_file_downloader_html(audio_file, "Audiobook"),
                unsafe_allow_html=True
            )
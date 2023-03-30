from __future__ import unicode_literals
from pathlib import Path
import streamlit as st
from yt_dlp import YoutubeDL
import whisper
import pandas as pd
import ffmpeg
import os

temp = os.environ['TEMP']
home = os.environ['YTDLP_HOME']

####streamlit run main.pyでGUI操作###



def movie_webm():

    ydl_opts = {
    # 'format': 'bestvideo',
        'paths': {"temp" : temp, "home": home+"movie_webm"},
        'ignore_no_formats_error':True,
        'ifnoreerrors': 'only_download',
        'final_ext': 'mp4'
        }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)

def sound_webm():

    ydl_opts = {
        'format': 'bestaudio',
        'paths': {"temp" : temp, "home": home+"sound_webm"},
        'ignore_no_formats_error':True,
        'ifnoreerrors': 'only_download',
        }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)


def movie_mp4():

    ydl_opts = {
        'format': 'best',
        'paths': {"temp" : temp, "home": home+"movie_mp4"},
        'ignore_no_formats_error':True,
        'ifnoreerrors': 'only_download',
    #     'postprocessors': [{  # Extract audio using ffmpeg
    #         'key': 'FFmpegVideoConvertor',
    #         'preferredcodec': '.mp4',
    # }]
        }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)


def sound_mp3():

    ydl_opts = {
        'format': 'bestaudio',
        'paths': {"temp" : temp, "home": home+"sound_mp3"},
        'ignore_no_formats_error':True,
        'ifnoreerrors': 'only_download',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
    }]
        }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)




st.header('メディアダウンロード\n(再生リスト・チャンネルまとめても可能)')
with st.form("main_form",clear_on_submit=True):
    URL=st.text_input('URL')
    btn_movie_webm=st.form_submit_button('動画ダウンロード(.webm)')
    btn_movie_mp4=st.form_submit_button('動画ダウンロード(.mp4)')
    btn_sound_webm=st.form_submit_button('音声ダウンロード(.webm)')
    btn_sound_mp3=st.form_submit_button('音声ダウンロード(.mp3)')

    if btn_movie_webm:
        movie_webm()
    if btn_sound_webm:
        sound_webm()
    if btn_movie_mp4:
        movie_mp4()
    if btn_sound_mp3:
        sound_mp3()

st.header('Sound to Text')
path=st.text_input('音声ファイルのパス')
model = st.selectbox(
    'モデル',
    ('base','large'))
textbtn=st.button('テキスト出力')
if textbtn:
    model = whisper.load_model(model)
    result = model.transcribe(path)
    st.write(result["text"])
    st.write(pd.DataFrame(result["segments"])[["id", "start", "end", "text"]])


st.header('拡張子変換')
input=st.text_input('入力ファイルのパス')
output=st.text_input('出力ファイル(拡張子付き)')
changefilebtn=st.button('変換')
if changefilebtn:
    stream=ffmpeg.input(input)
    stream=ffmpeg.output(stream,output)
    ffmpeg.run(stream)
from googletrans import Translator
import googletrans
import json
import requests
import datetime
import streamlit as st
import pyttsx3
import streamlit.components.v1 as components
from gtts import gTTS
import pygame
import os

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")

translator = Translator()

def ChangeWidgetFontSize(wgt_txt, wch_font_size = '25px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

def speak(str):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    engine.say(str)
    engine.runAndWait()

def wish(newstype):
    currentTime = datetime.datetime.now()
    h = currentTime.hour
    if (h >= 12 and h <= 16):
        speak("good afternoon")
    elif (h >= 17 and h <= 23):
        speak("Good evening")
    elif (h >= 0 and h <= 5):
        speak("Hey buddy you should not use screen at this time , It's unhealthy for you")
    elif (h >= 6 and h <= 11):
        speak("Good morning")

    speak(f"Welcome to News Reader ,  I am Natasha. {newstype} news for today, let's begin")

def hindi_audio_generator(hindi_news_list, type_of_news):
    # Define the text to be converted to speech
    for index, item in enumerate(hindi_news_list):

        # Create a gTTS object and specify the language
        tts = gTTS(text=item, lang='hi')

        # Save the audio file
        tts.save(f"{type_of_news} {index + 1}.mp3")

def play_news(audio_file):
    # Initialize pygame
    pygame.init()

    # Load the audio file
    pygame.mixer.music.load(audio_file)

    # Play the audio file
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop and close the audio file
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def audio_file_deleter():

    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".mp3"):
            os.remove(filename)

def general_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)

    wish("general")
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)

    art_general = news_general_1["articles"]

    for index , item in enumerate(art_general):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)

        if index == len(art_general)-1:
            speak(f"Last News {item['title']} . That's all about today's headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def general_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)

    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")
    # st.write(news_list)
    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        # st.write(hindi_news)
        hindi_news.append(translated)

    # demostr1 = "Fetching News Please Wait..."
    hindi_audio_generator(hindi_news, "general_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के सामान्य समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"general_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")

    audio_file_deleter()

def business_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    wish("business")
    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_business = requests.get(url).text
    news_business_1 = json.loads(news_business)

    art_business = news_business_1["articles"]

    for index ,item in enumerate(art_business):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        if index == len(art_business) - 1:
            speak(f"Last News {item['title']} . That's all about today's business headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def business_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")

    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        hindi_news.append(translated)

    hindi_audio_generator(hindi_news, "business_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के व्यापार समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"business_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")
    audio_file_deleter()

def entertainment_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    wish("entertainment")
    url = "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_ent = requests.get(url).text
    news_ent_1 = json.loads(news_ent)

    art_ent = news_ent_1["articles"]

    for index, item in enumerate(art_ent):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        if index == len(art_ent) - 1:
            speak(f"Last News {item['title']} . That's all about today's Entertainment headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def entertainment_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")

    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        hindi_news.append(translated)

    hindi_audio_generator(hindi_news, "entertainment_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के मनोरंजन समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"entertainment_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")
    audio_file_deleter()

def health_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    wish("health")
    url = "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_health = requests.get(url).text
    news_health_1 = json.loads(news_health)

    art_health = news_health_1["articles"]

    for index, item in enumerate(art_health):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        if index == len(art_health) - 1:
            speak(f"Last News {item['title']} . That's all about today's Health related headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def health_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")

    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        hindi_news.append(translated)

    hindi_audio_generator(hindi_news, "health_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के स्वास्थय समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"health_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")
    audio_file_deleter()

def science_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    wish("science")
    url = "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_science = requests.get(url).text
    news_science_1 = json.loads(news_science)

    art_science = news_science_1["articles"]

    for index, item in enumerate(art_science):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        if index == len(art_science) - 1:
            speak(f"Last News {item['title']} . That's all about today's Science related headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def science_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")

    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        hindi_news.append(translated)

    hindi_audio_generator(hindi_news, "science_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के विज्ञान समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"science_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")
    audio_file_deleter()

def sports_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    wish("sports")
    url = "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_sports = requests.get(url).text
    news_sports_1 = json.loads(news_sports)

    art_sports = news_sports_1["articles"]

    for index, item in enumerate(art_sports):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html = True)    
        if index == len(art_sports) - 1:
            speak(f"Last News {item['title']} . That's all about today's sports headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def sports_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")

    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        hindi_news.append(translated)

    hindi_audio_generator(hindi_news, "sports_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के खेल समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"sports_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")
    audio_file_deleter()

def technology_news():
    demostr1 = "Fetching News Please Wait..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    wish("technology")
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_tech = requests.get(url).text
    news_tech_1 = json.loads(news_tech)

    art_tech = news_tech_1["articles"]

    for index, item in enumerate(art_tech):
        demostr = f"{index + 1}. {item['title']}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)

        if index == len(art_tech) - 1:
            speak(f"Last News {item['title']} . That's all about today's Technologies realated headlines , Thanks for Listening")
        else:
            speak(f"number {index + 1} {item['title']}")

def technology_news_hindi():
    demostr1 = "समाचार लाया जा रहा है कृपया प्रतीक्षा करें ..."
    empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr1}</p>'.format(demostr1=demostr1)
    st.markdown(empty_display, unsafe_allow_html=True)
    news_list = []
    hindi_news = []
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=1672d3caf47a4d84a30723f00e7eedbf"
    news_general = requests.get(url).text
    news_general_1 = json.loads(news_general)
    art_general = news_general_1["articles"]

    for index, item in enumerate(art_general):
        news_list.append(f"{item['title']}")

    for i in news_list:
        translated = translator.translate(text=i, src='en', dest='hi').text
        hindi_news.append(translated)

    hindi_audio_generator(hindi_news, "technology_hindi_news")
    play_news("hindi wishes/नमस्कार, मैं  प्रगति आपका एक बार फिरसे स्वागत करती हु न्यूज़ रीडर में, आज के प्रोद्योगिक समाचार कुछ इस प्रकार है.mp3")

    for index, item in enumerate(hindi_news):
        # print(f"{index + 1}. {item}")
        demostr = f"{index + 1}. {item}"
        empty_display = '<p style="font-family:sans-serif; font-weight:bold; color:#ffe600; font-size: 25px; -webkit-text-stroke-width:1.4px; -webkit-text-stroke-color:black ;">{demostr}</p>'.format(demostr=demostr)
        st.markdown(empty_display, unsafe_allow_html=True)
        play_news(f"technology_hindi_news {index + 1}.mp3")

    play_news("hindi wishes/आज के मुख्य समाचार समाप्त हुए , धन्यवाद.mp3")
    audio_file_deleter()


st.title("\U0001f4f0 News Reader \U0001f4f0")
c1, c2 = st.columns(2)
lang = c1.radio(label='Select Your Language / अपनी भाषा चुने', options=("English", "हिंदी"))
type_of_news = c2.radio(label='Select Type of News / समाचार का प्रकार चुनें', options=("General News / सामान्य समाचार", "Business News / व्यापार समाचार", "Entertianment News / मनोरंजन समाचार", "Health News / स्वास्थ्य समाचार", "Science News / विज्ञान समाचार", "Sports News / खेल समाचार", "Technology News / प्रौद्योगिकी समाचार"))

ChangeWidgetFontSize('Select Your Language / अपनी भाषा चुने', '25px')
ChangeWidgetFontSize('Select Type of News / समाचार का प्रकार चुनें', '25px')

if st.button("Get News / समाचार प्राप्त करें"):
    if lang == "English":
        if type_of_news == "General News / सामान्य समाचार":
            general_news()
        elif type_of_news == "Business News / व्यापार समाचार":
            business_news()
        elif type_of_news == "Entertianment News / मनोरंजन समाचार":
            entertainment_news()
        elif type_of_news == "Health News / स्वास्थ्य समाचार":
            health_news()
        elif type_of_news == "Science News / विज्ञान समाचार":
            science_news()
        elif type_of_news == "Sports News / खेल समाचार":
            sports_news()
        else:
            technology_news()
    else:
        if type_of_news == "General News / सामान्य समाचार":
            general_news_hindi()
        elif type_of_news == "Business News / व्यापार समाचार":
            business_news_hindi()
        elif type_of_news == "Entertianment News / मनोरंजन समाचार":
            entertainment_news_hindi()
        elif type_of_news == "Health News / स्वास्थ्य समाचार":
            health_news_hindi()
        elif type_of_news == "Science News / विज्ञान समाचार":
            science_news_hindi()
        elif type_of_news == "Sports News / खेल समाचार":
            sports_news_hindi()
        else:
            technology_news_hindi()
            pass




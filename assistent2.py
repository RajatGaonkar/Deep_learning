import pyttsx3
import pygame
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime as dt
import random 
import psutil
import os


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',165)


def speak(string):
    engine.say(string)
    print(string)
    engine.runAndWait()


os.system('cls')
now=dt.datetime.now()
time1=str(now.strftime('%H:%M'))
time2=time1.split(':')
H=int(time2[0])
M=int(time2[1])
if H==0 and M!=0:
    speak('Good Morning sir.')
if H>=1 and H<12:
    speak('Good Morning sir.')
if H>=12 and H<17:
    speak('Good afternoon sir.')
if H>=17:
    speak('Good evening sir.')


r=sr.Recognizer()
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        print('say something')
        audio = r.listen(source)
        data=''
        try:
            data=r.recognize_google(audio)
            print(data)
        except sr.UnknownValueError:
            print('sorry sir, I did not get that')
        except sr.RequestError:
            print('sorry sir, my service is down')
        return data



files=[]
directory='H:/Songs/All'
os.chdir(directory)
for file in os.listdir(directory):
    if file.endswith('.mp3'):
        files.append(file) 
ind=random.choice(range(0,len(files)))
index=ind
def playanysong():
    speak('playing sir')
    pygame.mixer.init()
    pygame.mixer.music.load(files[ind])
    pygame.mixer.music.play()
def getdate():
    today=dt.datetime.now()
    tod_str=str(today)
    to=tod_str.split(' ')
    date=dt.date.today()
    dat=str(date)
    wi=today.weekday()
    month_list=['s','January','February','March','April','May','June','July','August','September','October','November','December']
    mon=dat.split("-")
    mi=int(mon[1])
    month=month_list[mi]
    year=mon[0]
    day=mon[2]
    daylist=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd',
             '23rd','24th','25th','26th','27th','28th','29th','30th','31st']
             
    return 'today is '+daylist[int(day)-1]+' of '+month+' '+year+' sir.'

def respond(data):
    global index
    now=dt.datetime.now()
    time1=str(now.strftime('%H:%M'))
    time2=time1.split(':')
    H=int(time2[0])
    M=int(time2[1])
    if H>=12:
        m=' PM'
        h=H-12
    else:
        m=' AM'
        h=H
    time="sir it's  "+str(h)+':'+str(M)+m+'.'


    if 'open' in data:
        if 'visual code' in data or 'vs code' in data or 'visual studio' in data or 'v s code' in data:
            speak('here you go sir.')
            path="C:\\Users\\RAJAT\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        if 'control panel' in data:
            speak('here you go sir.')
            path='C:\\Users\\RAJAT\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Control Panel.lnk'
        if 'command prompt' in data or 'cmd' in data or 'terminal' in data:
            speak('here you go sir.')
            path='C:\\Users\\RAJAT\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Command Prompt.lnk'
        os.startfile(path)
    if 'search google' in data or 'open google' in data:
        search=record_audio('sir, what do you want to search for?')
        url='https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak('here is what I found for '+search)
        
    if 'search youtube' in data or 'open youtube' in data:
        search=record_audio('what do you want to search for?')
        url='https://www.youtube.com/results?search_query='+search
        webbrowser.get().open(url)
    if 'find location' in data or 'find a location' in data:
        location=record_audio('which location sir?')
        url='https://google.nl/maps/place/'+location+'&amp;'
        webbrowser.get().open(url)
        speak('here is the location of ',location)
    if 'what is' in data and 'boss' not in data and 'time' not in  data and 'date' not in data and 'day' not in data or 'who is' in data  :
        l=data.split(' ')
        while True:
            if l[0]=='is':
                l.remove(l[0])
                break
            else:
                l.remove(l[0])
        s=''
        for i in l:
            s=s+i+' '
        r=wikipedia.summary(s,sentences=2)
        speak(r)
    if 'hey jarvis' in data or 'hi jarvis' in data:
        speak('hi sir.')
    if 'play' in data and 'song' in data:
        playanysong()
    if 'dont like' in data and 'song' in data:
        pygame.mixer.init()
        pygame.mixer.music.stop()
        speak('try this one, sir.')
        if index!=905:
            index+=1
        else:
            index=1
        pygame.mixer.init()
        pygame.mixer.music.load(files[index])
        pygame.mixer.music.play()
    if "today's date" in data:
        speak(getdate())
    if 'time' in data or 'time now' in data:
        speak(time)
    if "today's" not in data and 'day' in data and 'today' in data or 'it' in data.split():
        today=dt.datetime.now()
        wi=today.weekday()
        week_list=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        week='its '+week_list[wi]+' sir.'
        speak(week)
    if 'exit' in data:
        exit()
    if 'stop song' in data or  'stop music' in data or 'stop playing' in data:
        pygame.mixer.music.stop()
    if 'next song' in data:
        if index!=905:
            index+=1
        else:
            index=1
        pygame.mixer.init()
        pygame.mixer.music.load(files[index])
        pygame.mixer.music.play()
    if 'previous song' in data:
        if index!=1:
            index-=1
        else:
            index=905
        pygame.mixer.init()
        pygame.mixer.music.load(files[index])
        pygame.mixer.music.play()
    if 'pause' in data:
        speak('ok sir')
        pygame.mixer.music.pause()
    if 'resume' in data:
        speak('ok sir')
        pygame.mixer.music.unpause()
    if 'volume' in data:
        volu=pygame.mixer.music.get_volume()
        add=1-volu
        if 'increase' in data:
            if volu+0.2<=1:
                vol=volu+0.2
            else:
                vol=volu+add
        if 'decrease' in data:
            if volu-0.2>=0:
                vol=volu-0.2
            else:
                vol=0
        if 'to hundred percent' in data:
            vol=1
        pygame.mixer.music.set_volume(vol)

    if 'shutdown' in data:
        speak('shutting down the system, Good bye sir')
        os.system("shutdown/s")
    if 'restart system' in data:
        speak('restarting the system, sir')
        os.system("shutdown/r")
    if 'lock device' in data or 'log out' in data or 'lock system' in data:
        speak('ok sir')  
        os.system('shutdown/l')
    if 'battery status' in data :
        battery=psutil.sensors_battery()
        plugged=battery.power_plugged
        percent=(battery.percent)
        if plugged==False:
            st='sir, '+str(percent)+' percent battery life is remaining.'
        else:
            st='sir, the system is charging and '+str(percent)+' percent battery life is remaining.'
        speak(st)
    if 'play' in data or 'i wanted to watch' in data or 'i like to watch':
        if 'movei' in data or 'film' in data:
            l=record_audio('which language sir?')
            loc='F:/'+str(l)
            os.chdir(loc)
            fl=os.listdir(loc)
            m=record_audio('which film sir?')



while True:
    data=input('say something: ')
    #record_audio()
    respond(data)

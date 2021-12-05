import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import tempfile
mixer.init()
pygame.display.init()


def talk(sentence, lang):
  with tempfile.NamedTemporaryFile(delete=True) as f:
    tts = gTTS(text=sentence, lang=lang)
    tts.save('{}.mp3'.format(f.name))
    mixer.music.load('{}.mp3'.format(f.name))
    mixer.music.set_endevent(pygame.USEREVENT)  # 語音播放結束事件
    mixer.music.play(loops=0)


sr_flag = True  # 允許語音輸入
while True:
  try:
    for event in pygame.event.get():  # 讀取語音播放結束的事件
      if event.type == pygame.USEREVENT:  # 語音播放結束
        sr_flag = True  # 允許語音輸入
  except:
    pass

  if sr_flag == True:
    try:
      # 打開麥克風
      with sr.Microphone() as source:
        print("說些話吧: ")
        r = sr.Recognizer()
        # 設定聲音辨識的靈敏度
        r.energy_threshold = 4000
        audio = r.listen(source)  # 等待語音輸入
        # 語音轉換為文字
        listen_text = r.recognize_google(audio, language="zh-TW")
        print(listen_text)
        if "讀報" in listen_text:
          talk("蘋果傳出將砸百億元擴大投資台灣", 'zh-tw')
          sr_flag = False  # 不允許語音輸入
    except sr.UnknownValueError:
      print("語音無法辨識")
      sr_flag = True  # 允許語音輸入

import pygame
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pygame import mixer
import tempfile


def talk(sentence, lang):
  with tempfile.NamedTemporaryFile(delete=True) as f:
    tts = gTTS(text=sentence, lang=lang)
    tts.save('{}.mp3'.format(f.name))
    mixer.music.load('{}.mp3'.format(f.name))
    mixer.music.set_endevent(pygame.USEREVENT)  # 語音播放結束事件
    mixer.music.play(loops=0)


def google_translator(texts, target_lang):
  translator = Translator()
  return translator.translate(texts, dest=target_lang).text


mixer.init()
pygame.display.init()
news = []
with open('news.txt', 'r', encoding='utf-8') as f:
  for line in f:
    news.append(line)

n = 0  # 第幾篇文章
report = news[n]
print(report)
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
        if "報" in listen_text:
          print(report)
          talk(report, 'zh-tw')
          sr_flag = False  # 不允許語音輸入
        elif "翻譯" in listen_text or "英文" in listen_text:
          res_text = google_translator(report, target_lang='en')
          print(res_text)
          talk(res_text, 'en')
          sr_flag = False  # 不允許語音輸入
        elif "下一篇" in listen_text or "下" in listen_text:
          n += 1
          if n == len(news):
            n = 0
          report = news[n]
          print(report)
        elif "上一篇" in listen_text or "上" in listen_text:
          n -= 1
          if n < 0:
            n = len(news)-1
          report = news[n]
          print(report)
        elif "結束" in listen_text or "停止" in listen_text \
            or "拜" in listen_text:
          break
        else:
          print("我不了解什麼是：" + listen_text)
          talk("請再說一次!", 'zh-tw')
          sr_flag = False  # 不允許語音輸入
    except sr.UnknownValueError:
      print("語音無法辨識")
      sr_flag = True  # 允許語音輸入
    except sr.RequestError as e:
      print("沒有語音輸入{0}" .format(e))
      sr_flag = True  # 允許語音輸入

import speech_recognition as sr

r = sr.Recognizer()
# 設定聲音辨識的靈敏度
r.energy_threshold = 4000

while True:
  try:
    # 打開麥克風
    with sr.Microphone() as source:
      #   print("請開始說話:")
      audio = r.listen(source)  # 等待語音輸入
      # 將剛才說的話轉成繁體中文
      listen_text = r.recognize_google(audio, language="zh-TW")
      print(listen_text + "\n")
      with open('script2.txt', 'a', encoding='utf-8') as f:
        f.write(listen_text + "\n")
      if listen_text == "結束":
        break
  except sr.UnknownValueError:
    # print("語音無法辨識\n")
    pass
  except sr.RequestError as e:
    # print("語音無法辨識{0}\n" .format(e))
    pass

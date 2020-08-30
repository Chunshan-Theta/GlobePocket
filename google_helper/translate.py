import googletrans

translator = googletrans.Translator()

def enzh(msg):
    return translator.translate(msg, src="en", dest="zh-tw").text

def zhen(msg):
    return translator.translate(msg, dest="en", src="zh-tw").text
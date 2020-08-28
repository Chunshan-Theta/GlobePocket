import googletrans

translator = googletrans.Translator()

def enzh(text):
    return str(translator.translate(text, src="en", dest="zh-tw"))

import googletrans

translator = googletrans.Translator()

def enzh(text):
    return translator.translate(text, src="en", dest="zh-tw")
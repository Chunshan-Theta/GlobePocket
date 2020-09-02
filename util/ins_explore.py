import requests
import requests as rq
from util import jieba


# 使用scikit-learn進行向量轉換
# 忽略在文章中佔了90%的文字(即去除高頻率字彙)
# 文字至少出現在2篇文章中才進行向量轉換
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

# import pandas as pd
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation



def demo(lst: list, n_components=5, top_w=10):
    lst = [str(item) for item in lst if len(item) > 0]
    reviews_data = pd.DataFrame(lst, columns=['c'])['c'].astype(str).dropna()
    #
    tm = TfidfTransformer()
    cv = CountVectorizer(max_df=10, min_df=5, stop_words="english")
    tv = TfidfVectorizer()
    reviews_data = tm.fit_transform(cv.fit_transform(reviews_data))

    data = reviews_data  # .dropna()
    dtm = tm.fit_transform(data)
    # 使用LDA演算法
    LDA = LatentDirichletAllocation(n_components=n_components, random_state=0)
    LDA.fit(dtm)
    # 觀看結果
    re_arr = []
    for i, topic in enumerate(LDA.components_):
        # print(f"TOP 10 WORDS PER TOPIC #{i}")
        re_arr.append([cv.get_feature_names()[index] for index in topic.argsort()[-1 * top_w:]])
    return re_arr


def catch_tag(text: str) -> str:
    tag_str = ""

    save_option = False
    for i in text:
        if i == "#" and not save_option:
            save_option = True
        elif i == "#" and save_option:
            tag_str += " "
        if save_option:

            if i in [" ", "\n", "\t", "\ufeff"]:
                save_option = False
                tag_str += " "
            else:
                tag_str += i

    return tag_str


def explore_hashtag(text: str, num=3) -> [str]:
    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={text}&rank_token=0.19167611402747253&include_reel=true"
    json_obj = rq.get(url).json()

    return [i["hashtag"]["name"] for i in json_obj['hashtags'][:num]]


def get_ins_post_text(text: str) -> (list, list):
    url = f"https://www.instagram.com/explore/tags/{text}/?__a=1"
    temp_arr = []
    json_obj = rq.get(url).json()
    edges = json_obj['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    for e in edges:
        try:
            temp_arr.append(catch_tag(str(e['node']['edge_media_to_caption']['edges'][0]['node']['text'])))
        except IndexError:
            pass
    return edges, temp_arr

def get_ins_from_google_search(text: str,NextPage = 0) -> (list, list):
    text.replace(" ","+")
    url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyA3fN27gbdKTelvniFWyrpMpEH6nka1sIg&q={text}&cx=9ff2e57a2817b1aec&start={1+NextPage*10}&sort=date"
    url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyA3fN27gbdKTelvniFWyrpMpEH6nka1sIg&q={text}&cx=9ff2e57a2817b1aec&start={1+NextPage*10}"
    temp_text_arr = []
    temp_pic_arr = []
    json_obj = rq.get(url).json()
    try:
        edges = json_obj['items']
    except KeyError as e:
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyBinwEHB0IW80b1G9KmHuEA0zVHbUH_lrg&q={text}&cx=9ff2e57a2817b1aec&start={1 + NextPage * 10}"
            edges = json_obj['items']
        except KeyError as e:
            print(json_obj)
            raise e
    for e in edges:
        try:
            url = e['link']
            snippet = e['snippet']
            title = e['title']
            shortcode = url[url.find('/p/')+3:url.find('/',url.find('/p/')+3)]
            description = e['pagemap']['metatags'][0]['og:description']
            source_content_post = description[description.find(":")+1:]
            content_post = " ".join([w for w in list(jieba.cut(source_content_post)) if len(w)>1])
            author = description[description.find("-")+1:description.find(":")]
            image_post = e['pagemap']['metatags'][0]['og:image']
            temp_text_arr.append(str(content_post))
            temp_pic_arr.append({
                "url":f"https://www.instagram.com/p/{shortcode}/",
                "shortcode":shortcode,
                "description":description,
                "media":image_post,
                "content":source_content_post,
                "author":author,
                "title":title
            })
        except IndexError:
            pass
        except KeyError:
            pass
    return temp_pic_arr, temp_text_arr

def export_spot(location="烏來"):
    list_text = []
    list_posts = []

    for i in range(3):
        posts, text = get_ins_from_google_search(location,NextPage=i)
        list_text += text
        for p in posts:
            #
            try:
                post_text = p['description']
                content = p['content']
                url = p['url']
                thumbnail_src = p['media']
                author = p['author']
                shortcode = p['shortcode']
                title = p['title']
                list_posts.append({
                    "shortcode":shortcode,
                    "post_text": post_text,
                    "thumbnail_src": thumbnail_src,
                    "accessibility_caption": author,
                    "title": f"{content} {author} ",
                    "media": thumbnail_src,
                    "url": f"{url}",
                })
            except IndexError:
                pass

    arr = demo(list_text, n_components=3, top_w=3)
    topics_dict = {".".join(topics): [] for topics in arr}

    exist_photo = []
    for p in list_posts:
        for k in topics_dict.keys():
            for tag in str(k).split("."):
                if p['post_text'].find(tag) != -1:
                    if p['shortcode'] not in exist_photo:
                        topics_dict[k].append(p)
                        exist_photo.append(p['shortcode'])

    return topics_dict


def ins_get_pic_by_short_code(code='B7WLKhlDn_p'):
    headers_mobile = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}

    content = requests.get(f"https://www.instagram.com/p/{code}/",headers=headers_mobile)
    htmlsoup = BeautifulSoup(content.text, 'html.parser')
    print(content.text)

    pics = htmlsoup.findAll("meta", {"property": "og:image"})
    #print(pics)
    return pics[0].get("content")
"""
import json

print(json.dumps(export_spot(location="龍山寺")))



print(ins_get_pic_by_short_code())
"""


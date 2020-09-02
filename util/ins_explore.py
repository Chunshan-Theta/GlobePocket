import requests as rq

# 使用scikit-learn進行向量轉換
# 忽略在文章中佔了90%的文字(即去除高頻率字彙)
# 文字至少出現在2篇文章中才進行向量轉換
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

# import pandas as pd
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation

import jieba

def demo(lst: list, n_components=5, top_w=10):
    lst = [str(item) for item in lst if len(item) > 0]
    reviews_data = pd.DataFrame(lst, columns=['c'])['c'].astype(str).dropna()
    #
    tm = TfidfTransformer()
    cv = CountVectorizer(max_df=0.15, min_df=0.05, stop_words="english")
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

def get_ins_from_google_search(text: str) -> (list, list):
    url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyA3fN27gbdKTelvniFWyrpMpEH6nka1sIg&q={text}+\"%23\"&cx=9ff2e57a2817b1aec&start=1&sort=date&type:%20image"
    temp_text_arr = []
    temp_pic_arr = []
    json_obj = rq.get(url).json()
    edges = json_obj['items']
    for e in edges:
        try:
            url = e['link']
            snippet = e['snippet']
            description = e['pagemap']['metatags'][0]['og:description']
            source_content_post = description[description.find(":")+1:]
            content_post = " ".join(jieba.cut_for_search(source_content_post))+source_content_post
            author = description[description.find("-")+1:description.find(":")]
            image_post = e['pagemap']['metatags'][0]['og:image']
            temp_text_arr.append(str(content_post))
            temp_pic_arr.append({
                "url":url,
                "description":description,
                "media":image_post,
                "content":content_post,
                "author":author,
            })
        except IndexError:
            pass
    return temp_pic_arr, temp_text_arr

def export_spot(location="烏來"):
    list_text = []
    list_posts = []
    hashtags = [location,f"{}+food",f"{}+photo"]
    for t in hashtags:
        posts, text = get_ins_from_google_search(t)
        list_text += text
        for p in posts:
            #
            try:
                post_text = p['description']
                url = p['url']
                thumbnail_src = p['media']
                author = p['author']
                list_posts.append({
                    "post_text": post_text,
                    "thumbnail_src": thumbnail_src,
                    "accessibility_caption": author,
                    "title": F"{author} {post_text}",
                    "media": thumbnail_src,
                    "url": f"{url}",
                })
            except IndexError:
                pass

    arr = demo(list_text, n_components=5, top_w=3)
    topics_dict = {".".join(topics): [] for topics in arr}

    for p in list_posts:
        for k in topics_dict.keys():
            for tag in str(k).split("."):
                if p['post_text'].find(tag) != -1:
                    topics_dict[k].append(p)

    return topics_dict

"""
import json

print(json.dumps(export_spot(location="龍山寺")))
"""
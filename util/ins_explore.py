import requests as rq

# 使用scikit-learn進行向量轉換
# 忽略在文章中佔了90%的文字(即去除高頻率字彙)
# 文字至少出現在2篇文章中才進行向量轉換
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
    cv = CountVectorizer(max_df=0.1, min_df=0.001, stop_words="english")
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


def export_spot(location="烏來"):
    list_text = []
    list_posts = []
    hashtags = explore_hashtag(location)
    for t in hashtags:
        posts, text = get_ins_post_text(t)
        list_text += text
        for p in posts:
            #
            try:
                post_text = p['node']['edge_media_to_caption']['edges'][0]['node']['text']
                shortcode = p['node']['shortcode']
                thumbnail_src = p['node']['thumbnail_src']
                accessibility_caption = p['node']['accessibility_caption'] or shortcode
                list_posts.append({
                    "post_text": post_text,
                    "shortcode": shortcode,
                    "thumbnail_src": thumbnail_src,
                    "accessibility_caption": accessibility_caption,
                    "title": accessibility_caption,
                    "media": thumbnail_src,
                    "url": f"https://www.instagram.com/p/{shortcode}/",
                })
            except IndexError:
                pass

    arr = demo(list_text, n_components=5, top_w=3)

    topics_dict = {".".join(topics): [] for topics in arr}

    for p in list_posts:
        for k in topics_dict.keys():
            for tag in str(k).split("."):
                if tag in p['post_text']:
                    topics_dict[k].append(p)

    return topics_dict

'''
import json

print(json.dumps(export_spot(location="西子灣")))
'''
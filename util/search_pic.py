import requests
import random

class pic(dict):

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            self.__setitem__(k, v)
        assert self.__getitem__("title")
        assert self.__getitem__("media")
        assert self.__getitem__("url")


class pic_set_obj:
    def __init__(self, pic:[pic]):
        self.pics=pic

    def get_a_pic(self,only_pic_url=False) -> pic:
        if only_pic_url:
            return random.choice(self.pics)["media"]
        else:
            return random.choice(self.pics)

    def get_pics(self,count) -> [pic]:
        assert count <=50, "Too many"
        if len(self.pics) < count:
            count = len(self.pics)
        return random.choices(population=self.pics, k=count)

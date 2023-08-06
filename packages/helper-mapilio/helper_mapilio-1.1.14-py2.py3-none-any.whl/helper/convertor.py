from json import JSONEncoder

import cv2
import numpy as np
import urllib.request
from operator import itemgetter
from itertools import groupby


class Convertor:

    @staticmethod
    def url_to_image(url: str) -> np.ndarray:
        """
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        :param url:
        :return:
        """

        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image

    @staticmethod
    def tensorFaster_to_np(tensor):
        return tensor[0]["boxes"].cpu().numpy(), \
               tensor[0]["scores"].cpu().numpy(), \
               tensor[0]["labels"].cpu().numpy()

    @staticmethod
    def tensorMask_to_np(tensor):
        return tensor[0]["boxes"].detach().cpu().numpy(), \
               tensor[0]["scores"].detach().cpu().numpy(), \
               tensor[0]["labels"].detach().cpu().numpy(), \
               tensor[0]["masks"].squeeze().detach().cpu().numpy()

    @staticmethod
    def list_to_dict(data: list, config: dict) -> dict:
        """

        :param data:
        :param config:
        :return:
        """
        keys = config.columnKeys

        return dict(zip(keys, data))

    @staticmethod
    def url_to_auth_id(url):
        x = url.split("/")
        return x[5]

    @staticmethod
    class Bunch(object):
        def __init__(self, adict):
            self.__dict__.update(adict)

    @staticmethod
    def groupby_dict_in_list_key(arr, match):
        """

        Parameters
        ----------
        arr
        match

        Returns
        -------

        """
        for key, value in groupby(arr, key=itemgetter(match)):
            yield value


    @staticmethod
    class numpy_array_encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)


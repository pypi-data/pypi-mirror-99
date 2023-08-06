#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : 陈坤泽
# @Email  : 877362867@qq.com
# @Date   : 2020/11/17 15:13

from pyxllib.cv._2_cvprcs import *


class PilPrcs(CvPrcs):
    @classmethod
    def read(cls, file, flags=1, **kwargs):
        if is_pil_image(file):
            img = file
        elif is_numpy_image(file):
            img = cv2pil(file)
        elif File(file):
            img = Image.open(str(file), **kwargs)
        else:
            raise TypeError(f'类型错误或文件不存在：{type(file)} {file}')
        return cls.cvt_channel(img, flags)

    @classmethod
    def cvt_channel(cls, img, flags=None):
        if flags is None: return img
        n_c = cls.n_channels(img)
        if flags == 0 and n_c > 1:
            img = img.convert('L')
        elif flags == 1 and n_c != 3:
            img = img.convert('RGB')
        return img

    @classmethod
    def write(cls, img, path, if_exists='delete', **kwargs):
        p = File(path)
        if p.exist_preprcs(if_exists):
            p.ensure_parent()
            img.save(str(p), **kwargs)

    @classmethod
    def resize(cls, img, size, **kwargs):
        """

        :param kwargs:
            resample=3，插值算法；有PIL.Image.NEAREST, ~BOX, ~BILINEAR, ~HAMMING, ~BICUBIC, ~LANCZOS等
                默认是 PIL.Image.BICUBIC；如果mode是"1"或"P"模式，则总是 PIL.Image.NEAREST

        >>> im = PilPrcs.read(np.zeros([100, 200], dtype='uint8'), 0)
        >>> im.size
        (100, 200)
        >>> im2 = im.reduce_by_area(50*50, **kwargs)
        >>> im2.size
        (35, 70)
        """
        # 注意pil图像尺寸接口都是[w,h]，跟标准的[h,w]相反
        return img.resize(size[::-1])

    @classmethod
    def size(cls, img):
        w, h = img.size
        return h, w

    @classmethod
    def n_channels(cls, img):
        """ 通道数 """
        return len(img.getbands())

    @classmethod
    def show(cls, img, title=None, command=None):
        return cls.show(img, title, command)

    @classmethod
    def random_direction(cls, img):
        """ 假设原图片是未旋转的状态0

        顺时针转90度是label=1，顺时针转180度是label2 ...
        """
        label = np.random.randint(4)
        if label == 1:
            # PIL的旋转角度，是指逆时针角度；但是我这里编号是顺时针
            img = img.transpose(PIL.Image.ROTATE_270)
        elif label == 2:
            img = img.transpose(PIL.Image.ROTATE_180)
        elif label == 3:
            img = img.transpose(PIL.Image.ROTATE_90)
        return img, label

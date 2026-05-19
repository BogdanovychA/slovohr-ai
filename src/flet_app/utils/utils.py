# -*- coding: utf-8 -*-


def set_attr(obj, key, value):
    setattr(obj, key, value)
    obj.update()

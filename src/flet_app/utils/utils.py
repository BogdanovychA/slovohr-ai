# -*- coding: utf-8 -*-


def set_attr(obj, key, value):
    """Динамічно встановлює атрибут об'єкта Flet та оновлює його відображення."""
    setattr(obj, key, value)
    obj.update()

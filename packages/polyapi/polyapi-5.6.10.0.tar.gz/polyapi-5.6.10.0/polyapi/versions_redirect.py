#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Описание класса, вызывающего те или иные реализации методов бизнес-сценариев Полиматики в зависимости от версии """

from .polymatica_57 import Polymatica57


class VersionRedirect():
    def __init__(self, base_bs):
        self.current_version = base_bs.polymatica_version
        self.polymatica_56_bs = base_bs
        self.polymatica_57_bs = Polymatica57(base_bs)

    def invoke_method(self, method, *args, **kwargs):
        """ Вызов определённой реализации заданного метода в зависимости от версии Полиматики """
        if self.current_version == '5.7':
            result = getattr(self.polymatica_57_bs, method)(*args, **kwargs)
        else:
            result = getattr(self.polymatica_56_bs, method)(*args, **kwargs)
        return result

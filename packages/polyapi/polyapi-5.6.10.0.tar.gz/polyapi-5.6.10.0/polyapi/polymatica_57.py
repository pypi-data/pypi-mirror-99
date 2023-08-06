#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Реализация методов бизнес-сценариев Полиматики версии 5.7 """


class Polymatica57():
    """ Реализация методов, заточенная под Полиматику версии 5.7 """
    def __init__(self, base_bs):
        self.base_bs = base_bs

    def create_multisphere_from_cube(self, **kwargs):
        """
        Создать мультисферу из куба.
        """
        result = self.base_bs.execute_manager_command(
            command_name="user_iface",
            state="create_module",
            layer_id=self.base_bs.active_layer_id,
            cube_id=self.base_bs.cube_id,
            module_id=kwargs.get('module_id'),
            after_module_id=kwargs.get('after_module_id'),
            module_type=kwargs.get('module_type')
        )
        return result

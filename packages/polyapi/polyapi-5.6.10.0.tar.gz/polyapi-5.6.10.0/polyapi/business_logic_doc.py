#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Базовый класс, описывающий бизнес-сценарии использования Полиматики.
Используемые переменные класса:

# Версия сервера Полиматики
self.polymatica_version

# Язык интерфейса. Задается во время авторизации. Возможно задать значения: "ru", "en", "de" или "fr".
# По-умолчанию "ru"
self.language

# URL стенда Полиматики
self.url

# Флаг работы в Jupiter Notebook
self.jupiter

# Таймаут выполнения запросов
self.timeout

# Текст ошибки присвается в случае аварийного завершения работы; может быть удобно при работе в Jupiter Notebook
self.current_exception

# Логин пользователя Полиматики
self.login

# Для измерения времени работы функций бизнес-логики
self.func_timing

# Таблица команд и состояний
self.server_codes

# Идентификатор активного OLAP-модуля (мультисферы)
self.multisphere_module_id

# Идентификатор куба, соответствующего активному OLAP-модулю
self.cube_id

# Название куба, соответствующего активному OLAP-модулю
self.cube_name

# Список идентификаторов всех слоёв
self.layers_list

# Идентификатор активного слоя
self.active_layer_id

# Данные мультисферы в формате {"dimensions": "", "facts": "", "data": ""}
self.multisphere_data

# Общее число строк текущего (активного) OLAP-модуля
self.total_row

# Идентификатор сессии
self.session_id

# Идентификатор (uuid) авторизации
self.authorization_uuid

# Класс, выполняющий HTTP-запросы
self.exec_request

# Объект выполнения команд модуля Manager
self.manager_command

# Объект выполнения команд модуля OLAP
self.olap_command

# Helper class
self.h

# Сохранённое имя функции для избежания конфликтов с декоратором
self.func_name

# Содержимое DataFrame
self.df

# Колонки DataFrame
self.df_cols

# Вспомогательный класс, перенаправляющий вызовы методы на нужные реализации (в зависимости от версии)
self.version_redirect
"""

__name__ = "BusinessLogic"

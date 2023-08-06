# coding: utf-8

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# Stdlib
from __future__ import absolute_import
import six

import collections

# 3rdparty
from m3.actions import Action

#------------------------------------------------------------------------------
# Metadata
#------------------------------------------------------------------------------

__author__ = 'Andrey Torsunov'
__contact__ = 'torsunov@bars-open.com'
__docformat__ = 'restructuredtext'


#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------

def make_action(
    url,
    run_method,
    shortname='',
    acd=None,
    classname='SimpleAction',
    bind_run=False,
    bind_acd=False,
    need_atomic=None,
    category=None,
):
    u""" Конструктор Action'ов.

    Позволяет создать экшен без непосредственного объявления его класса.
    Пример:

    .. code-block:: python

        from m3.actions import ACD

        def run_implementation(action, request, context):
            pass

        def acd_implementation():
            return (
                ACD(name="int_param", type=int, required=True),
            )

        action = make_action(
            '/action_url',
            run_implementation,
            acd=acd_implementation,
            bind_run=True)


    :param str url: URL экшена.
    :param function run_method: аналог метода run в экшене.
    :param str shortname: (не обязательно) уникальное имя экшена, по
        которому к нему можно получить быстрый доступ.
    :param function acd: (не обязательно) метод объявляющий список
        правил извлечения параметров (ActionContextDeclaration).
    :param str classname: (не обязательно) имя класса, которое примет
        созданный экшн, по-умолчанию: `SimpleAction`.
    :param bind_run: (не обязательно) флаг, указывающий на необходимость
        передачи методу в `run_method` ссылки на сам экшн (self),
        по-умолчанию: :const:`False`.
    :param bind_acd: (не обязательно) флаг, указывающий на необходимость
        передачи методу в `acd` ссылки на сам экшн (self),
        по-умолчанию: :const:`False`.
    :param need_atomic: (не обязательно) флаг, указывающий на необходимость
        установки такого флага на экшене - для внешнего оборачивания в atomic,
        по-умолчанию: :const:`None`.
    :param category: (не обязательно) строка, категория поведения экшена,
        например, можно указать 'readonly'.
        эта категория может использоваться для разделения экшенов на "читающие"
        и "пишущие", чтобы роутить запросы к разным БД.
        по-умолчанию: :const:`None`.

    :return: Дочерний класс от :class:`Action`
    :rtype: class

    """
    # Генерация класса экшена
    cls = type(classname, (Action,), dict(
        url=url,
        shortname=shortname
    ))
    action = cls()
    # Привязка функций реализующих логику экшена
    action.run = bind_run and run_method.__get__(action) or run_method
    if acd is not None:
        action.context_declaration = bind_acd and acd.__get__(action) or acd
    if need_atomic is not None:
        action.need_atomic = need_atomic
    if category is not None:
        action.category = category
    return action


def init_component(instance, **kwargs):
    u""" Инициализация атрибутов экземпляра.

    Используется для удобной инициализации атрибутов через конструктор
    по средством kwargs.
    """
    for attr, val in kwargs.items():
        instance.__setattr__(attr, val)


def sequenceable(item):
    u""" Преобразование в последовательность.

    Если элемент поддерживает интерфейс Sequence (за исключением строк),
    то он преобразуется к кортежу, в ином случае элемент обертвается в
    кортеж.

    .. note::
        Если передан None, то вернется пустой кортеж.

    :param item:

    :rtype tuple:

    """
    if isinstance(item, six.string_types):
        seq = (item,)
    elif item is None:
        seq = ()
    elif isinstance(item, collections.Iterable):
        seq = tuple(item)
    else:
        seq = (item,)
    return seq


class AttributedDict(dict):
    """Словарь, позволяющий обращаться к своим элементам
    как к атрибутам объекта.

    """
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, key, value):
        self[key] = value

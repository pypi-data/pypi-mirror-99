#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# Stdlib
import json
import operator
import six
from collections import (
    Iterable,
)
from six.moves import (
  filter,
)

# 3rdparty
from django.conf import (
    settings,
)
from django.core.exceptions import (
    FieldDoesNotExist,
)
from django.db.models import (
    ProtectedError,
)
from django.db.models.base import (
    Model,
)

from m3 import (
    ApplicationLogicException,
)
from m3.actions import (
    ACD,
    ActionPack,
)
from m3.actions.context import (
    ActionContext,
    ConversionFailed,
)
from m3.actions.interfaces import (
    IMultiSelectablePack,
)
from m3.actions.results import (
    OperationResult,
)
from m3.actions.urls import (
    get_url,
)
from m3.actions.utils import (
    extract_int,
)
from m3_ext.ui.containers.grids import (
    ExtLiveGridCheckBoxSelModel,
)
from m3_ext.ui.fields import (
    ExtComboBox,
    ExtDictSelectField,
)
from m3_ext.ui.fields.complex import (
    ExtMultiSelectField,
)
from m3_ext.ui.fields.simple import (
    ExtCheckBox,
    ExtRadio,
    ExtStringField,
    ExtTextArea,
)
from m3_ext.ui.misc.store import (
    ExtDataStore,
    ExtJsonStore,
)
from m3_ext.ui.panels.grids import (
    ExtMultiGroupinGrid,
    ExtObjectGrid,
)
from m3_ext.ui.results import (
    ExtUIScriptResult,
)

# Recordpack
from . import (
    helpers,
    signals,
    typecast,
)
from .be import (
    BE,
)
from .exceptions import (
    MultipleObjects,
    ObjectDoesNotExists,
)
from .provider import (
    FIELD_VIEW,
    QueryObject,
)
from .proxy import (
    BaseProxy,
)
from .results import (
    JsonSerializableResult,
)


#------------------------------------------------------------------------------
# Metadata
#------------------------------------------------------------------------------

__docformat__ = 'restructuredtext'

# категория для экшенов с записью в БД
WRITE_CATEGORY = 'write'
# категория для readonly экшенов
READONLY_CATEGORY = 'readonly'

#------------------------------------------------------------------------------
# Pack classes
#------------------------------------------------------------------------------

class BaseRecordPack(ActionPack):
    """
    Экшенпак для работы с провайдерами записей
    """
    #: Заголовок пака, а так же окна редактирования по-умолчанию.
    title = ''

    #: Иконка для рабочего стола, которая будет соответствовать паку.
    icon_big = 'enterprise-icon-b'

    #: Провайдер записей, наследованный от BaseRecordProvider
    provider = None

    #: Имя параметра в контексте, который идентифицирует текущую запись.
    #: При привязке пака к гриду методом bind_to_grid, его row_id в
    #: контексте принимает имя context_id.
    context_id = 'id'

    #: Тип, к которому будет приводиться значение в `context_id`.
    context_type = int

    #: Имя параметра в контексте, который будет использовать мастер-запись
    context_master_id = None

    #: Тип, к которому будет приводиться значение в `context_master_id`.
    context_master_type = int

    #: Имя поля в модели, хранящее ссылку на мастер-запись
    master_id = None

    #: Указывает на то, что поле master является ForeignKey.
    #: Из-за особенностей Django ORM к нему будет добавляться суффикс _id
    #: p.s.: Гореть вам в аду если не используете ForeignKey >:]
    master_is_foreignkey = True

    #: Класс формы (подкласс BaseExtWindow) для создания новой записи.
    new_window = None

    #: Класс формы (подкласс BaseExtWindow) для редактирования записи.
    edit_window = None

    #: Карта соответствия контекстных данных и имен атрибутов объекта
    #: (для фильтров и сортировки).
    #:
    #: Параметры:
    #:
    #: - ключ словаря, имя в контексте и имя фильтра;
    #: - `attr` (не обязателен), имя атрибута модели, по-умолчанию будет
    #:   совпадать с ключом;
    #: - `oper` (не обязателен), операция фильтрации из Django ORM,
    #:   по-умолчанию будет `icontains`;
    #: - `type` (не обязателен), тип данных к которому будет приведено
    #:   значение фильтра;
    #: - `filter` (не обязателен), функция для преобразования значения
    #:   фильтра, возрващаемое значение станет новым значение фильтра.
    #:
    #: Примеры:
    #:
    #: Отображение контекстных данных на поле из модели, тем самым
    #: позволяя производить сортировку по этому полю:
    #:
    #: .. code-block:: python
    #:
    #:     {'sum_form': 'sum_model'}
    #:
    #: Отображение контекстных данных на правило фильтрации по полю
    #: модели указанной в `provider` как `data_source`:
    #:
    #: .. code-block:: python
    #:
    #:     {'date': {'attr': 'person__birthday', 'oper': 'icontains'}}
    #:
    #: Допускается указание функции для преобразования значения фильтра:
    #:
    #: .. code-block:: python
    #:
    #:     {'node': {'attr': 'parent',
    #:               'oper': 'exact',
    #:               'filter': lambda x: 0 if x < 0 else x},
    #:
    #: Допускается указание типа к которому будут приведены данныз из
    #: контекста:
    #:
    #: .. code-block:: python
    #:
    #:     {'filter_date_start': {'attr': 'date_formatting',
    #:                            'oper': 'gt',
    #:                            'type': datetime.date },
    context_attr_map = {}

    #: Список правил фильтрации для колонок грида.
    #:
    #: .. note::
    #:     Отличие :attr:`quick_filters` от :attr:`context_attr_map` в
    #:     том, что :attr:`quick_filters` предназначен исключительно
    #:     для грида, в то время, как :attr:`context_attr_map` для
    #:     обработки контекста в целом.
    #:
    #: Если требуется добавить фильтрацию для колонки в гриде, то
    #: необходимо описать правило фильтрации в :attr:`quick_filters`,
    #: иначе "шапка" c полем (контролом) для фильтрации в колонке грида
    #: попросту не появится.
    #:
    #: Формат описания фильтров аналогичен :attr:`context_attr_map`, но
    #: еще можно указать контрол для фильтра в колонке, пример:
    #:
    #: .. code-block:: python
    #:
    #:     {'date': {'attr': 'parent',
    #:               'oper': 'exact',
    #:               'filter': lambda x: 0 if x < 0 else x,
    #:               'control': {'xtype': 'textfield'}}
    #:
    #: Где ``control`` - элемент фильтрации встраиваемый в колонку,
    #: по-умолчанию: ``textfield``, ``control`` так же может содержать
    #: экземпляр дочернего класса :class:`m3_ext.ui.fields.base.BaseExtField`.
    quick_filters = {}

    #: Настройка позволяет изменить поведение при приведении данных
    #: из контекста к требуемому типу данных, при извлечении фильтров
    #: :attr:`quick_filters` и :attr:`context_attr_map`.
    #: Ключ - тип (int, objects, bool и т.д.).
    #: Значение - :func:`callable` с одним аргументом.
    custom_typecast = {}

    #: Признак редактирования на клиенте.
    #: Если редактирование локальное, то запросы сохранения и удаления не
    #: пишут в базу, а лишь обрабатывают записи результатом сохранения в
    #: этом случае будет JSON созданной/редактированной записи.
    local_edit = False

    #: Признак обновления только тех частей дерева, в которых были изменения.
    #: В этом случае будет происходить и запись в базу, и передача
    #: созданной/редактированной записи.
    incremental_update = False

    #: Словарь соответствия имен параметров в запросе на сохрание
    #: атрибутов в модели / прокси.
    #: Необходимо задавать для правильного биндинга гридов в режиме
    #: локального редактирования.
    local_edit_map = {}

    #: Жесткие разрешения на отдельные действия с гридом. Влияет на
    #: поведение метода :meth:`bind_to_grid`. Если какое-то из
    #: действий не разрешено, то его экшен не будет присвоен гриду
    #: и соответствующая кнопка на тулбаре грида не будет отображена.
    #:
    #: .. note::
    #:    Тем не менее, сами экшены будут существовать. Злоумышленник
    #:    может вызвать их напрямую. Эта проблема должна решаться с
    #:    помощью разграничения прав доступа.
    allow_add = True
    allow_edit = True
    allow_delete = True

    #: Имя колонки, по-которой грид сортируется по-умолчанию.
    #: Если указан префикс "-", то сортировка будет по-убыванию.
    #: Если это массив строк, то будет множественная сортировка.
    sorting = None

    #: Итоговые атрибуты.
    #: Ключ - атрибут, значение - операция.
    #: Доступные значения операции: sum, count.
    totals = {}

    def __init__(self):
        super(BaseRecordPack, self).__init__()

        # Экшн редактирования записи (отображение окна редактирования)
        self.action_edit = helpers.make_action(
            '/edit', self.request_edit_window,
            acd=self._get_edit_action_context_declaration,
            classname='EditAction',
            need_atomic=False,
            category=READONLY_CATEGORY,
        )

        # Экшн удаления записи
        self.action_delete = helpers.make_action(
            '/delete',
            self.request_delete_rows,
            acd=self._get_delete_action_context_declaration,
            classname='DeleteAction',
            need_atomic=True,
            category=WRITE_CATEGORY,
        )

        # Экшн сохранения записи
        self.action_save = helpers.make_action(
            '/save',
            self.request_save,
            acd=self._get_save_action_context_declaration,
            classname='SaveAction',
            need_atomic=True,
            category=WRITE_CATEGORY,
        )

        # Экшн подгружающий доступные записи
        self.action_rows = helpers.make_action(
            '/rows',
            self.request_rows,
            acd=self._get_rows_action_context_declaration,
            classname='RowsAction',
            need_atomic=False,
            category=READONLY_CATEGORY,
        )

        self.actions.extend([
            self.action_edit,
            self.action_delete,
            self.action_rows,
            self.action_save
        ])

    #--------------------------------------------------------------------------
    # Правила извлечения параметров из контекста
    #--------------------------------------------------------------------------

    def _get_edit_action_context_declaration(self):
        """ Правила извлечения для :attr:`action_edit`. """
        result = [
            ACD(name='isGetData',
                required=True,
                type=bool,
                default=False),
            ACD(name=self.context_id,
                required=True,
                type=self.context_type,
                default=0),
        ]

        if self.context_master_id:
            result.append(
                ACD(name=self.context_master_id,
                    required=True,
                    type=self.context_master_type))

        return result

    def _get_save_action_context_declaration(self):
        """ Правила извлечения для :attr:`action_save`. """
        result = [
            ACD(name=self.context_id,
                required=True,
                type=self.context_type,
                default=0),
        ]
        if self.context_master_id:
            result.append(
                ACD(name=self.context_master_id,
                    required=True,
                    type=self.context_master_type))

        # В случае локального редактирования в запросе могут
        # передаваться объекты стора целиком.
        for context_name in self.local_edit_map.keys():
            result.append(
                ACD(name=context_name,
                    required=True,
                    type=object))

        return result

    def _get_rows_action_context_declaration(self):
        """ Правила извлечения для :attr:`action_rows`. """
        result = [
            ACD(
                name='multisort',
                required=False,
                type=object,
            ),
            ACD(
                name='start',
                required=True,
                default=0,
                type=int,
            ),
            ACD(
                name='limit',
                required=True,
                default=200,
                type=int,
            ),
            ACD(
                name='sort',
                required=True,
                default='',
                type=str,
            ),
            ACD(
                name='dir',
                type=str,
                required=True,
                default='ASC',
            ),
        ]
        if self.context_master_id:
            result.append(
                ACD(name=self.context_master_id,
                    required=True,
                    type=self.context_master_type))

        return result

    def _get_delete_action_context_declaration(self):
        """ Правила извлечения для :attr:`action_delete`. """
        return [
            ACD(name=self.context_id,
                required=True,
                type=ActionContext.ValuesList(type=self.context_type),
                default=0),
        ]

    #--------------------------------------------------------------------------
    # Извлечение дополнительного контекста для фильтрации
    #--------------------------------------------------------------------------

    def _extract_filter_from_request(self, request, context_map):
        _filter = None

        # Допускаются только те значения, которые описаны в context_map
        # и не явлюятся пустыми.
        iter_context = filter(
            lambda cn_cv: cn_cv[0] in context_map and cn_cv[1],
            six.iteritems(request.POST)
        )

        for context_name, context_value in iter_context:
            oper = BE.IC
            name = context_name
            params = context_map[context_name]
            if isinstance(params, six.string_types):
                params = {'attr': params}

            if 'type' in params:
                context_value = typecast.typecast(
                    context_value, params['type'], self.custom_typecast)
                if params['type'] == int:
                    oper = BE.EQ # для инта по дефолту EQ а не IC

            if 'expr' in params and callable(params['expr']):
                expr_filter = params['expr'](context_value)
                if expr_filter is not None:
                    _filter &= expr_filter
            elif 'expr' in params and isinstance(params['expr'], BE):
                _filter &= params['expr']
            else:
                if 'attr' in params:
                    name = params['attr']
                if 'oper' in params:
                    oper = params['oper']
                if 'filter' in params and callable(params['filter']):
                    context_value = params['filter'](context_value)
                _filter &= BE(name, oper, context_value)

        return _filter

    def extract_filter_context(self, request, context):
        """ Извлечение фильтров из контекста запроса.

        Извлечение фильтров происходит на основе правил описанных
        в ``context_attr_map``.

        :rtype: BooleanExpression or None

        """
        return self._extract_filter_from_request(request,
                                                 self.context_attr_map)

    def extract_quick_filter_context(self, request, context):
        """ Извлечение фильтров из контекста запроса.

        Извлечение фильтров происходит на основе правил описанных
        в ``quick_filters``.

        :rtype: BooleanExpression or None

        """
        return self._extract_filter_from_request(request, self.quick_filters)

    def _convert_context_name_to_attr(self, context_name):
        """ Преобразование имени из контекста в имя поля модели.

        Преобразование происходит по правилам описанным в:
        - :attr:`context_attr_map`,
        - :attr:`quick_filters`.

        :param basestring context_name: имя атрибута в контексте

        :return: если правило преобразования не найдено, то вернется
            непреобразованное имя.
        :rtype: str

        """
        context_maps = filter(
            lambda m: context_name in m,
            (self.context_attr_map, self.quick_filters))

        real_name = context_name
        for context_map in context_maps:
            params = context_map[context_name]
            if isinstance(params, dict) and 'attr' in params:
                real_name = params['attr']
                break
            elif isinstance(params, six.string_types):
                real_name = params
                break

        return real_name

    def _update_sorting_context(self, sort_name, direction, sorting=None):
        """ Обновление информации для сортировки.

        :param basestring sort_name: поле для сортировки
        :param basestring direction: направление сортировки ("DESC", "ASC")
        :param list sorting: данные для сортировки

        :rtype: list

        """
        sorting = sorting or []
        attr = self._convert_context_name_to_attr(sort_name)
        sorting.append((attr, direction))
        return sorting

    def extract_sort_context(self, request, context):
        """ Извлечение параметров сортировки из контекста.
        """
        sorting = []
        direction = request.POST.get('dir')
        user_sort = request.POST.get('sort')

        # Множественная сортировка.
        if hasattr(context, 'multisort'):
            for sort in context.multisort:
                sorting = self._update_sorting_context(
                    sort['field'], sort['direction'], sorting)

        # Сортировка по одному полю.
        elif user_sort:
            sorting = self._update_sorting_context(
                user_sort, direction, sorting)

        # Сортировка по-умолчанию, если есть.
        elif self.sorting:
            default_sorting = helpers.sequenceable(self.sorting)
            for sort_name in default_sorting:
                direction = sort_name.startswith("-") and "DESC" or "ASC"
                sort_name = sort_name.lstrip("-")
                sorting = self._update_sorting_context(
                    sort_name, direction, sorting)

        return sorting

    def _convert_value(self, raw_value, arg_type):
        """ Приведение значения к типу.

        :param raw_value: приводимое значение
        :param arg_type: приводимый тип

        """
        try:
            value = typecast.typecast(raw_value, arg_type)
        except (ValueError, TypeError):
            raise ConversionFailed(value=raw_value, type=arg_type)

        return value

    #--------------------------------------------------------------------------
    # Обработчики экшенов
    #--------------------------------------------------------------------------

    def get_row_from_request(self, request, context):
        """ Получение / поиск редактируемой записи из `request`.

        :return: (Model or BaseProxy, bool), первым элементом
            передается сама запись или ее прокси объект; если запись
            новая, то второй элемент кортежа будет :const:`True`, в
            ином случае :const:`False`.
        :rtype: tuple

        """
        qo = self.get_query_object(request, context)
        row_id = getattr(context, self.context_id)
        is_new = not row_id
        if is_new:
            row = self.new_row(request, context)
        else:
            row = self.get_row(request, context, key=row_id, query_object=qo)
        return row, is_new

    def get_query_object(self, request, context):
        """
        Возвращает начальный объект для запроса к провайдеру.
        Используется для переопределения в потомках.

        :rtype: QueryObject

        """
        qo = QueryObject()
        qo.totals = self.totals
        return qo

    def request_rows(self, request, context):
        """ Обработчик запроса на получение списка записей.

        :rtype: JsonSerializableResult

        """
        qo = self.get_query_object(request, context)

        # Если таблица подчиненная, то фильтруем по мастеру
        if self.context_master_id:
            master_id = getattr(context, self.context_master_id)
            qo.filter = BE(self.master_id, BE.EQ, master_id) & qo.filter

        # Пейджиг / срез
        qo.begin = extract_int(request, 'start')
        qo.end = qo.begin + extract_int(request, 'limit')

        # Фильтрация основанная на ``context_attr_map``.
        filter_context = self.extract_filter_context(request, context)
        if filter_context:
            qo.filter = filter_context & qo.filter

        # Фильтрация основанная на ``quick_filters``.
        quick_filter = self.extract_quick_filter_context(request, context)
        if quick_filter:
            qo.quick_filter = quick_filter & qo.quick_filter

        # Сортировка
        sort_context = self.extract_sort_context(request, context)
        qo.sorting.extend(sort_context)

        # Сигнал о готовности извлечь записи
        signals.base_record_pack_before_get_rows.send(
            sender=self.__class__,
            instance=self,
            request=request,
            context=context,
            query=qo)

        result = self.get_rows(request, context, qo)

        # Сигнал того, что данные уже извлечены.
        signals.base_record_pack_after_get_rows.send(
            sender=self.__class__,
            instance=self,
            request=request,
            context=context,
            query=qo,
            rows=result)

        return JsonSerializableResult(result)

    def _process_preview_field(self, field, data_object, complex_data):

        if isinstance(field, ExtMultiSelectField):
            # Для полей множественного выбора выделим список идентификаторов
            # записей по аттрибуту value_field
            # Выводить в поле будем либо объединённое выводимое значение
            # записей (по аттрибуту display_field), либо указанное в нём
            # кастомное текстовое сообщение
            data = (json.loads(field.value)
                    if isinstance(field.value, str) else field.value)
            ids = [x[field.value_field] for x in data]
            if field.multiple_display_value and len(data) > 1:
                value = field.multiple_display_value
            else:
                value = ', '.join([
                    str(x[field.display_field]) for x in data
                ])

            complex_data[field.name] = {
                'id': ids,
                'value': value
            }

        elif isinstance(field, ExtDictSelectField):
            complex_data[field.name] = {
                'id': field.value,
                'value': field.default_text
            }

        elif isinstance(field, ExtComboBox):
            if field.editable:
                data_object[field.name] = field.value
            elif field.store:
                # Правила нахожджения записи в сторе
                rules = (
                    # Длина элементов записи должна быть болье 1го
                    lambda r: len(r) > 1,
                    # Первый элемент должен совпадать с искомым
                    # значением
                    lambda r: six.text_type(r[0]) == six.text_type(field.value),
                )
                try:
                    # Поиск первой подходящей записи в сторе
                    record = next(filter(
                        lambda r: all(rl(r) for rl in rules),
                        field.store.data
                    ))
                except StopIteration:
                    # Если запись не удалось найти, данные
                    # подстав ляются как есть.
                    data_object[field.name] = field.value
                else:
                    if field.value_field == field.display_field:
                        default_text = record[0]
                    else:
                        default_text = record[1]

                    complex_data[field.name] = {
                        'id': field.value,
                        'value': default_text
                    }

        elif isinstance(field, ExtCheckBox):
            data_object[field.name] = field.checked

        elif isinstance(field, ExtRadio):
            if field.checked:
                data_object[field.name] = field.value

        else:
            data_object[field.name] = field.value

    def request_edit_window(self, request, context):
        """ Обработчик запроса на окно редактирования / создания записи.

        :rtype: ExtUIScriptResult or JsonSerializableResult

        """
        row, is_new = self.get_row_from_request(request, context)
        # Запрашиваются ли данные для предпросмотра?
        is_preview = context.isGetData

        # Перенос данных из записи в форму редактирования
        win = self.get_edit_window(
            request=request, context=context, record=row, is_new=is_new)

        # Если у окна редактирования записи есть метод настройки под
        # запрос, то он будет вызван.
        if hasattr(win, 'setup_by_request'):
            win.setup_by_request(request, context, self)

        # Отображение записи на окно редактирования.
        self.bind_record_to_window(request, context, row, win, is_new)

        if self.local_edit:
            # если редактирование в браузере
            self.bind_request_to_window(request, context, win)

        if is_preview:
            # Данные привязанные к форме из записи / прокси, должны быть
            # переданы отдельно в виде JSON.
            #
            # Передаваймый JSON содержит 2 словаря:
            # - data_object, переносит данные для простых полей.
            #   Например {'name': 'Alex', 'age': 30}
            # - complex_data, переносит данные для сложных компонентов,
            #   которые оперируют записями Store
            #
            # Данные берутся из каждого поля на форме и кладутся в
            # словарь, с ключом соответствующим имени поля. Штатный
            # биндинг М3 не подходит, т.к. когда он встречает точку в
            # name поля, например A.B, то пытается найти вложенный
            # объект A и его атрибут B.
            data_object = {}
            complex_data = {}
            grid_data = {}
            all_fields = win.form._get_all_fields(win)
            all_grids = self._get_all_grids(win)

            for field in all_fields:
                self._process_preview_field(field, data_object, complex_data)

            for grid in all_grids:
                if isinstance(grid.store, ExtDataStore) and grid.name:
                    grid_data[grid.name] = grid.store.data

            return JsonSerializableResult({
                'success': True,
                'data': data_object,
                'complex_data': complex_data,
                'grid_data': grid_data
            })

        else:
            win.form.url = get_url(self.action_save)
            win.data_url = get_url(self.action_edit)
            self.update_context(request, context, win)

            # Сигнал того, что создано окно редактирования.
            signals.base_record_pack_after_get_edit_window.send(
                sender=self.__class__,
                instance=self,
                request=request,
                context=context,
                record=row,
                window=win,
                is_new=is_new)

            return ExtUIScriptResult(win, context)

    def _get_all_grids(self, item, lst=None):
        """ Список всех гридов формы включая вложенные в контейнеры.

        :rtype: list

        """
        if lst is None:
            lst = []

        if isinstance(item, ExtObjectGrid):
            lst.append(item)
        elif hasattr(item, 'items'):
            for it in item.items:
                self._get_all_grids(it, lst)
        return lst

    def _request_save(self, request, context):
        row, is_new = self.get_row_from_request(request, context)

        # Создание окна
        win = self.get_edit_window(
            request=request, context=context, record=row, is_new=is_new)

        # Если у окна редактирования записи есть метод настройки под
        # запрос, то он будет вызван.
        if hasattr(win, 'setup_by_request'):
            win.setup_by_request(request, context, self)

        # Перенос данных запроса в форму редактирования.
        self.bind_request_to_window(request, context, win)

        # Перенос данных из формы в запись.
        self.bind_window_to_record(request, context, win, row, is_new)

        # Проверка перед сохранением
        result = self.validate_row(request, context, row, is_new)
        if result:
            return result

        qo = self.get_query_object(request, context)

        if self.local_edit:
            return self._local_save(request, context, row, is_new, qo)
        elif self.incremental_update:
            return self._incremental_save(request, context, row, is_new, qo)
        else:
            return self._natural_save(request, context, row, is_new, qo)

    def _local_save(self, request, context, row, is_new, qo):
        """ Редактирование на клиенте.

        :return: выдадим JSON записи
        :rtype: JsonSerializableResult

        """
        return JsonSerializableResult({'success': True, 'data': row})

    def _incremental_save(self, request, context, row, is_new, qo):
        """ Обновление частями.

        :return: JSON записи
        :rtype: JsonSerializableResult or OperationResult

        """
        self.save_row(request, context, row, is_new)
        # Для выдачи JSON надо получить объект списка, а не карточки,
        # но к сожалению провайдер устроен так, что ListProxy выдает
        # только get_rows.
        #
        # Его можно вызвать аналогично get_row, использую фильтрацию
        # только по id.
        qo.filter = BE(self.provider.key_field, BE.EQ, row.id)
        rows = self.provider.get_records(qo)

        if isinstance(rows, dict) and 'rows' in rows:
            rows = rows['rows']

        if rows:
            list_obj = rows[0]
            return JsonSerializableResult({'success': True, 'data': list_obj})

        return OperationResult()

    def _natural_save(self, request, context, row, is_new, qo):
        """ Серверное редактирование. """
        self.save_row(request, context, row, is_new)
        return OperationResult()

    def request_save(self, request, context):
        """ Обработчик запроса на сохранение записи.

        :rtype: OperationResult or JsonSerializableResult

        """
        return self._request_save(request, context)

    def request_delete_rows(self, request, context):
        """ Обработчик запроса на удаление записей.

        :rtype: OperationResult

        """
        rows_id = getattr(context, self.context_id)
        result = self.validate_delete_rows(request, context, rows_id)

        if result:
            return result

        # Удаление из БД только для серверного редактирования.
        if not self.local_edit:
            self.delete_rows(request, context, rows_id)

        return OperationResult()

    #--------------------------------------------------------------------------
    # Взаимодействие с провайдером
    #--------------------------------------------------------------------------

    def new_row_defaults(self, request, context, defaults):
        """
        Тут можно обновить/установить значения по-умолчанию для новых
        записей в зависимости от контекста
        """
        pass

    def new_row(self, request, context):
        """ Оборачивает создание новой записи от провайдера.

        Позволяет создать запись с предопределенными значениями полей.

        :rtype: Model or BaseProxy

        """
        # Создаем новую запись с заполненным мастером по умолчанию
        default_values = {}
        if self.context_master_id:
            master_value = getattr(context, self.context_master_id)
            master_field = self.master_id
            if self.master_is_foreignkey and not master_field.endswith('_id'):
                master_field += '_id'
            default_values[master_field] = master_value

        self.new_row_defaults(request, context, default_values)

        return self.provider.new_record(**default_values)

    def get_row(self, request, context, key, query_object=None):
        """ Оборачивает получение записи от провайдера.

        Метод нужнен чтобы обрабатывать возможные ошибки на
        пользовательском уровне.

        :raises: ObjectDoesNotExists, MultipleObjects

        """
        # Если key == 0, то требуется создать новую запись
        if self.local_edit and not typecast.mute_typecast(key, int):
            return self.new_row(request, context)
        else:
            try:
                return self.provider.get_record(
                    key=key, query_object=query_object)
            except ObjectDoesNotExists:
                raise ApplicationLogicException(
                    f'Запись с id={key} не существует в базе данных.')
            except MultipleObjects:
                raise ApplicationLogicException(
                    f'По id={key} найдено несколько записей. Возможно '
                    f'целостность данных нарушена.')

    def get_rows(self, request, context, query_object):
        """ Получение списка записей.

        :rtype: list

        """
        return self.provider.get_records(query_object)

    def save_row(self, request, context, record, is_new):
        """
        Сохранение записи.
        """
        return self.provider.save(record)

    def validate_row(self, request, context, record, is_new):
        """
        Проверка записи на корректность заполнения.
        """
        return self.provider.validate(record)

    def validate_delete_rows(self, request, context, ids):
        """
        Проверка возможности удаления записей.
        """
        return False

    def delete_rows(self, request, context, ids):
        """
        Удаление записей.
        """
        if isinstance(ids, six.string_types) or not isinstance(ids, Iterable):
            ids = [ids, ]

        for _id in ids:
            obj = self.get_row(request, context, key=_id)
            self.delete_row(request, context, obj)

    def delete_row(self, request, context, record):
        """
        Удаление записи.
        """
        try:
            self.provider.delete_record(record)
        except ProtectedError as e:
            err_msg = 'Нельзя удалить запись, так как она где-то используется!'

            if settings.DEBUG:
                if len(e.protected_objects) > 50:
                    err_msg += '<br>(обнаружено более 50 зависимостей)'
                err_msg = '{0}<br>{1}'.format(err_msg, '<br>'.join(
                    ['{0} ID={1}'.format(po._meta.verbose_name, po.id) for
                     po in e.protected_objects[:50]]))

            raise ApplicationLogicException(err_msg)

    #--------------------------------------------------------------------------
    # Взаимодействие с окнами
    #--------------------------------------------------------------------------

    def get_edit_window(self, request, context, record, is_new, **kwargs):
        """
        Получение окна редактирования записи.
        """
        if is_new:
            assert self.new_window, 'new_window должен быть задан'
            win = self.new_window(create_new=is_new, **kwargs)
        else:
            assert self.edit_window, 'edit_window должен быть задан'
            win = self.edit_window(create_new=is_new, **kwargs)

        if not win.title:
            win.title = self.title

        if hasattr(self, 'icon') and self.icon:
            win.icon_cls = self.icon

        win.form.url = get_url(self.action_save)

        return win

    def update_context(self, request, context, window):
        """
        Настройка контекста окна.
        """
        if not window.action_context:
            window.action_context = context
        else:
            window.action_context.__dict__.update(context.__dict__)

    def bind_record_to_window(self, request, context, record, window, is_new):
        """
        Отображение записи на форму.
        """
        window.form.from_object(record)

        def get_dbfield(obj, names):
            """
            Аналог функции get_value в ExtForm.from_object
            Ищет в объекте obj поле с именем names.
            Если соответствующего поля не оказалось, то возвращает None

            names задается в виде списка, т.о. если его длина больше единицы,
            то имеются вложенные объекты и их надо обработать
            :param obj: объект или словарь
            :type obj: object или dict
            :param names: список имен
            :type names: list
            """
            field_object = None

            # hasattr не работает для dict'a
            has_attr = (
                hasattr(obj, names[0])
                if not isinstance(obj, dict) else names[0] in obj)
            if has_attr:
                if len(names) == 1:
                    if not isinstance(obj, dict):
                        if isinstance(obj, BaseProxy):
                            obj = obj._root
                        if isinstance(obj, Model):
                            try:
                                field_object = obj._meta.get_field(names[0])
                            except FieldDoesNotExist:
                                pass
                else:
                    nested = (
                        getattr(obj, names[0])
                        if not isinstance(obj, dict) else obj[names[0]])
                    field_object = get_dbfield(nested, names[1:])

            return field_object

        # помимо отображения, сделаем настройку полей
        all_fields = window.form._get_all_fields(window.form)
        for field in all_fields:
            if not field.name:
                continue
            dbfield = get_dbfield(record, field.name.split('.'))
            # выставим макс длину поля в соответствии с длиной поля БД
            if (dbfield and isinstance(field, (ExtStringField, ExtTextArea)) and
                    dbfield.max_length and (field.max_length is None
                    or dbfield.max_length < field.max_length)):
                field.max_length = dbfield.max_length

    def bind_request_to_window(self, request, context, window):
        """
        Отображение запроса на форму.
        """
        window.form.bind_to_request(request)

    def bind_window_to_record(self, request, context, window, record, is_new):
        """
        Отображение формы в запись.
        """
        window.form.to_object(record)

        # Привязка данных при локальном редактировании
        for k, v in self.local_edit_map.items():
            value = getattr(context, k)
            setattr(record, v, value)

    def create_column_filters(self, request, context, grid_or_tree):
        """
        Построение фильтров в гриде.
        """
        columns = grid_or_tree.columns or ()
        for col_name, params in six.iteritems(self.quick_filters):
            params = params or {}
            control = params.get('control', {'xtype': 'textfield'})

            if isinstance(control, dict):
                control['filterName'] = col_name

            for column in columns:
                if column.data_index == col_name:
                    column.extra['filter'] = control

    def bind_to_grid(self, request, context, grid):
        """
        Присоединение списка к гриду.
        """
        # настройка стора
        if not grid.get_store():
            grid_store = ExtJsonStore(
                url=get_url(self.action_rows),
                auto_load=True,
                remote_sort=True)
            grid_store.total_property = 'total'
            grid_store.root = 'rows'
            grid.set_store(grid_store)
        else:
            grid.store.url = get_url(self.action_rows)
            grid.store.total_property = 'total'
            grid.store.root = 'rows'

        # Подключение экшенов
        if self.allow_add:
            grid.action_new = self.action_edit
        if self.allow_edit:
            grid.action_edit = self.action_edit
        if self.allow_delete:
            grid.action_delete = self.action_delete

        grid.action_data = self.action_rows
        grid.row_id_name = self.context_id
        grid.get_store().id_property = self.provider.key_field

        if isinstance(grid, (ExtMultiGroupinGrid, ExtObjectGrid)):
            grid.local_edit = self.local_edit or self.incremental_update

        self.create_column_filters(request, context, grid)

    #--------------------------------------------------------------------------
    # Геттеры адресов экшенов
    #--------------------------------------------------------------------------

    def get_edit_url(self):
        """
        Возвращает адрес формы редактирования элемента справочника.
        """
        return get_url(self.action_edit)

    def get_rows_url(self):
        """
        Возвращает адрес по которому запрашиваются элементы грида.
        """
        return get_url(self.action_rows)


class BaseRecordListPack(BaseRecordPack, IMultiSelectablePack):
    """ Прямой аналог линейного справочника.

    В дополнение к работе с данными из BaseRecordPack, содержит экшены
    форм списка и выбора, реализует интерфейс справочника ISelectablePack.

    """
    #: Заголовок окна списка записей по-умолчанию
    title_plural = ''

    #: Форма, которая будет вызываться при показе списка
    list_window = None

    #: Форма, которая будет вызываться при выборе из списка
    select_window = None

    #: Имя поля, по которому будет накладываться фильтр автодоплонения
    #: при выборе из ExtDictSelectField. Раньше, оно называлось так
    #: column_name_on_select = 'name'
    autocomplete_fields_name = 'name'

    #: Имя фильтра для автокомплита, см. meth:`extract_filter_context`
    autocomplete_filter_name = 'filter'

    def __init__(self):
        super(BaseRecordListPack, self).__init__()

        if not self.title_plural:
            self.title_plural = self.title

        # Экшн журнального окна.
        self.action_list = helpers.make_action(
            '/list',
            self.request_list_window,
            acd=self._get_list_action_context_declaration,
            classname='ListAction',
            need_atomic=False,
            category=READONLY_CATEGORY,
        )

        # Экшн окна выбора записей. Обычно используется для
        # :class:`ExtDictSelectField`.
        self.action_select = helpers.make_action(
            '/select',
            self.request_select_window,
            acd=self._get_select_action_context_declaration,
            classname='SelectAction',
            need_atomic=False,
            category=READONLY_CATEGORY,
        )

        # Экшн окна множественного выбора записей. Обычно используется для
        # :class:`ExtDictSelectField`.
        self.action_multi_select = helpers.make_action(
            '/multi-select',
            self.request_multi_select_window,
            acd=self._get_select_action_context_declaration,
            classname='MultiSelectAction',
            need_atomic=False,
            category=READONLY_CATEGORY,
        )

        self.actions.extend([
            self.action_list,
            self.action_select,
            self.action_multi_select
        ])

    #--------------------------------------------------------------------------
    # Правила извлечения параметров из контекста
    #--------------------------------------------------------------------------

    def _get_list_action_context_declaration(self):
        """ Правила извлечения контекста для :attr:`action_list`. """
        return []

    def _get_select_action_context_declaration(self):
        """ Правила извлечения контекста для :attr:`action_select`. """
        return [
            ACD(name='column_name_on_select',
                required=True,
                type=six.text_type,
                default=''),
        ]

    #--------------------------------------------------------------------------
    # Извлечение дополнительного контекста для фильтрации
    #--------------------------------------------------------------------------

    def extract_filter_context(self, request, context):
        _filter = super(BaseRecordListPack, self).extract_filter_context(
            request, context)

        if self.autocomplete_fields_name:
            # Введенные пользователем данные требующие автокомлита
            user_text = request.POST.get(self.autocomplete_filter_name)
            if user_text:
                _filter &= BE(self.autocomplete_fields_name, BE.IC, user_text)

        return _filter

    #--------------------------------------------------------------------------
    # Обработчики экшенов
    #--------------------------------------------------------------------------

    def request_list_window(self, request, context):
        """
        Обработчик запроса на октрытие журнального окна.
        """
        self._clear_context(request, context)
        win = self.get_list_window(request, context, False)

        # Если у журнального окна есть метод настройки под запрос, то он
        # будет вызван.
        if hasattr(win, 'setup_by_request'):
            win.setup_by_request(request, context, self)

        # Привязка пака к основному гриду журнального окна.
        self.bind_to_grid(request, context, win.grid)

        # Сигнал того, что создано журнальное окно.
        signals.base_record_list_pack_after_get_list_window.send(
            sender=self.__class__,
            instance=self,
            request=request,
            context=context,
            window=win)

        return ExtUIScriptResult(win, context)

    def request_select_window(self, request, context):
        """
        Обработчик запроса на октрытие окна выбора записи.
        """
        self._clear_context(request, context)
        win = self.get_list_window(request, context, True)

        # Если у окна выбора записи есть метод настройки под запрос,
        # то он будет вызван.
        if hasattr(win, 'setup_by_request'):
            win.setup_by_request(request, context, self)

        # Привязка пака к основному гриду окна выбора записи.
        self.bind_to_grid(request, context, win.grid)

        # Сигнал того, что создано окно выбора записи.
        signals.base_record_list_pack_after_get_select_window.send(
            sender=self.__class__,
            instance=self,
            request=request,
            context=context,
            window=win)

        return ExtUIScriptResult(win, context)

    def request_multi_select_window(self, request, context):
        """
        Обработчик запроса на октрытие окна множественного выбора записей.
        """
        self._clear_context(request, context)
        win = self.get_list_window(request, context, True)

        # Если у окна множественного выбора запией есть метод настройки
        # под запрос, то он будет вызван.
        if hasattr(win, 'setup_by_request'):
            win.setup_by_request(request, context, self)

        # Привязка пака к основному гриду окна множественного выбора записей.
        self.bind_to_grid(request, context, win.grid)

        # Модификация окна под множественный выбор.
        win.grid.sm = ExtLiveGridCheckBoxSelModel(check_only=True)
        win.set_multiselect_mode(True)

        return ExtUIScriptResult(win, context)

    def _clear_context(self, request, context):
        """ Очистка контекста от лишних параметров.

        В окно могут попасть оставшиеся в контексте значения quick-фильтров.

        """
        for context_name in self.quick_filters.keys():
            if hasattr(context, context_name):
                delattr(context, context_name)

    #--------------------------------------------------------------------------
    # Взаимодействие с окнами
    #--------------------------------------------------------------------------

    def get_list_window(self, request, context, is_select, *args, **kwargs):
        if is_select:
            if self.select_window is None:
                raise AttributeError((
                    "'select_window' must be specified in '{}' class"
                ).format(self.__class__.__name__))
            win = self.select_window(*args, **kwargs)
            win.modal = True
        else:
            if self.list_window is None:
                raise AttributeError((
                    "'list_window' must be specified in '{}' class"
                ).format(self.__class__.__name__))
            win = self.list_window(*args, **kwargs)

        if not win.title:
            win.title = self.title_plural

        if hasattr(self, 'icon') and self.icon:
            win.icon_cls = self.icon

        return win

    #--------------------------------------------------------------------------
    # Геттеры адресов экшенов
    #--------------------------------------------------------------------------

    def get_list_url(self):
        """ Возвращает адрес формы списка элементов справочника.

        Используется для присвоения адресов в прикладном приложении.

        """
        return get_url(self.action_list)

    #--------------------------------------------------------------------------
    # Реализация :class:`IMultiSelectablePack`
    #--------------------------------------------------------------------------

    def get_autocomplete_url(self):
        """ Возвращает адрес для автоподбора элементов по введеному
        пользователем тексту.
        """
        return self.get_rows_url()

    def get_edit_url(self):
        """ Возвращает адрес диалога редактирования выбранного элемента. """
        return super(BaseRecordListPack, self).get_edit_url()

    def get_multi_select_url(self):
        """ Возвращает адрес экшена окна для множественного выбора записей. """
        return get_url(self.action_multi_select)

    def get_select_url(self):
        """ Возвращает адрес экшена окна для выбора записей. """
        return get_url(self.action_select)

    def get_display_dict(self, key, value_field='id', display_field='name'):
        """ Получает список словарей для отображения в компоненте
        множественного выбора.

        Метод работает по разному в зависимости от переданного ключа key:
        - json строка - переводится с список id и передается провайдеру;
        - список или кортеж - передается провайдеру;
        - запись ORM или прокси - не передается провайдеру, данные
        извлекаются из неё напрямую.

        """
        items = []

        if isinstance(key, six.string_types):
            try:
                keys = json.loads(key)
            except ValueError:
                keys = [key]
        elif isinstance(key, Iterable):
            keys = key
        else:
            keys = [key]

        for key in filter(None, keys):
            if isinstance(key, (Model, BaseProxy)):
                row = key
            else:
                try:
                    row = self.get_display_record(key, [value_field,
                                                        display_field])
                except ObjectDoesNotExists:
                    row = None
                if not row:
                    continue

            value = getattr(row, value_field, None)
            if value:
                display = getattr(row, display_field, None)
                if callable(display):
                    display = display()
                items.append({
                    value_field: value,
                    display_field: display})

        return items

    def get_display_text(self, key, attr_name=None):
        """ Возвращает отображаемое значение записи (или :attr:`attr_name`)
        по ключу `key`.
        """
        name = attr_name or self.autocomplete_fields_name
        row = self.get_display_record(key, [name])

        if name and row:
            try:
                text = operator.attrgetter(name)(row)
            except AttributeError:
                text = None

            return callable(text) and text() or text
        elif row:
            return six.text_type(row)
        else:
            return

    def get_display_record(self, key, attrs=None):
        """
        Специальный метод, вызываемый в биндинге формы (ExtForm.from_object)
        для связки поля выбора из справочника с текущей выбранной записью.
        В отличие от get_record, должен вытащить не полную запись, а
        по возможности самый минимальный набор атрибутов.
        Это должно регулироваться либо специальным proxy-объектом (listproxy),
        либо query_object, в котором указываются нужные атрибуты
        :param key: ключ записи
        :param attrs: список атрибутов, которые требуются для отображения
        :return: запись
        """
        qo = QueryObject()
        # укажаем желаемое представление записи
        qo.view = FIELD_VIEW
        return self.get_record(key, query_object=qo)

    def get_record(self, key, query_object=None):
        if key == 0 or key == '':
            return None
        return self.provider.get_record(key=key, query_object=query_object)

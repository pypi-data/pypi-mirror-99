from typing import Dict, List
from elasticsearch import Elasticsearch

import time


########### es field ##############################
class ESTypeMapping:
    Long = 'long'
    Integer = 'integer'
    Short = 'short'
    Byte = 'byte'
    Double = 'double'
    Float = 'float'
    HalfFloat = 'half_float'
    ScaledFloat = 'scaled_float'
    UnsignedLong = 'unsigned_long'
    Keyword = 'keyword'
    ConstantKeyword = 'constant_keyword'
    Wildcard = 'wildcard'
    Text = 'text'
    Date = 'date'
    IP = 'ip'
    Boolean = 'boolean'


class ESBaseFeild:
    def __init__(self, feild_name, feild_type, **properties):
        self.feild_name = feild_name
        self.properties = {'type': feild_type}
        self.properties.update(properties)

    def add_property(self, **properties):
        """ 添加字段属性 """
        self.properties.update(properties)

    def get_feild(self):
        """ 获取属性结果 """
        return {self.feild_name: self.properties}


class LongFeild(ESBaseFeild):
    """ 64 位长整型 """

    def __init__(self, feild_name, **properties):
        super(LongFeild, self).__init__(feild_name, ESTypeMapping.Long, **properties)


class IntegerFeild(ESBaseFeild):
    """ 32位整型 """

    def __init__(self, feild_name, **properties):
        super(IntegerFeild, self).__init__(feild_name, ESTypeMapping.Integer, **properties)


class ShortFeild(ESBaseFeild):
    """ 16位短整型 """

    def __init__(self, feild_name, **properties):
        super(ShortFeild, self).__init__(feild_name, ESTypeMapping.Short, **properties)


class ByteFeild(ESBaseFeild):
    """ 字节类型 """

    def __init__(self, feild_name, **properties):
        super(ByteFeild, self).__init__(feild_name, ESTypeMapping.Byte, **properties)


class DoubleFeild(ESBaseFeild):
    """ 双精度浮点数 """

    def __init__(self, feild_name, **properties):
        super(DoubleFeild, self).__init__(feild_name, ESTypeMapping.Double, **properties)


class FloatFeild(ESBaseFeild):
    """ 单精度浮点型 """

    def __init__(self, feild_name, **properties):
        super(FloatFeild, self).__init__(feild_name, ESTypeMapping.Float, **properties)


class HalfFloatFeild(ESBaseFeild):
    """ 半浮点型 """

    def __init__(self, feild_name, **properties):
        super(HalfFloatFeild, self).__init__(feild_name, ESTypeMapping.HalfFloat, **properties)


class UnsignedLongFeild(ESBaseFeild):
    """ 64位 无符号长整形 """

    def __init__(self, feild_name, **properties):
        super(UnsignedLongFeild, self).__init__(feild_name, ESTypeMapping.UnsignedLong, **properties)


class KeywordFeild(ESBaseFeild):
    """ 关键字 """

    def __init__(self, feild_name, **properties):
        super(KeywordFeild, self).__init__(feild_name, ESTypeMapping.Keyword, **properties)


class ConstantKeywordFeild(ESBaseFeild):
    """ 关键字常量 值不变 """

    def __init__(self, feild_name, **properties):
        super(ConstantKeywordFeild, self).__init__(feild_name, ESTypeMapping.ConstantKeyword, **properties)


class WildcardFeild(ESBaseFeild):
    """ 通配符关键字 完整字段搜索慢 适用于类似日志grep等操作 """

    def __init__(self, feild_name, **properties):
        super(WildcardFeild, self).__init__(feild_name, ESTypeMapping.Wildcard, **properties)


class TextFeild(ESBaseFeild):
    """ 文本字段 """

    def __init__(self, feild_name, **properties):
        super(TextFeild, self).__init__(feild_name, ESTypeMapping.Text, **properties)


class DateFeild(ESBaseFeild):
    """ 日期 """

    def __init__(self, feild_name, **properties):
        super(DateFeild, self).__init__(feild_name, ESTypeMapping.Date, **properties)


class IPFeild(ESBaseFeild):
    """ IP """

    def __init__(self, feild_name, **properties):
        super(IPFeild, self).__init__(feild_name, ESTypeMapping.IP, **properties)


class BooleanFeild(ESBaseFeild):
    """ 布尔值 """

    def __init__(self, feild_name, **properties):
        super(BooleanFeild, self).__init__(feild_name, ESTypeMapping.Boolean, **properties)


########### es field ##############################
########### base data #############################
class BaseData(object):
    def __init__(self, **kwargs):
        self += kwargs
        # 记录实例化时间，用于排序
        self._created_at = time.time()

    def __add__(self, other: Dict):
        """ 使用加法的形式添加数据
        tmp = BaseData()
        tmp += {'a': 1}
        """
        if not isinstance(other, Dict):
            raise Exception('BaseData need dict')
        for key, val in other.items():
            self[key] = val
        return self

    def __lt__(self, other):
        """ 根据时间排序，默认升序排列 """
        return self._created_at < other._created_at

    def __getattribute__(self, item):
        """ 当访问的属性不存在时，返回 None """
        try:
            return super().__getattribute__(item)
        except Exception:
            return None

    def __getitem__(self, item):
        """ 该函数使实例可以像字典一样获取属性值 """
        return getattr(self, item)

    def __setitem__(self, key, value):
        """ 该函数使实例可以像字典一样获取属性值 """
        setattr(self, key, BaseData(**value) \
            if isinstance(value, Dict) else value)

    def __delitem__(self, key):
        """ 该函数使实例可以像字典一样删除属性 """
        delattr(self, key)

    def __call__(self):
        """ 使实例可执行，返回一个属性字典 """
        ret = dict()
        for item in dir(self):
            if item.startswith('_'): continue
            value = getattr(self, item)
            ret[item] = value() \
                if isinstance(value, BaseData) else value
        return ret


########### base data #############################


class Base(object):
    _name_ = None

    def __call__(self, *args, **kwargs):
        pass


class BaseField(Base):
    def __init__(self, **kwargs):
        self += kwargs

    def __add__(self, other: Dict):
        for key, val in other.items():
            setattr(self, key, val)
        return self

    def __call__(self):
        ret = dict()
        for name in dir(self):
            if name.startswith('_'): continue
            value = getattr(self, name)
            ret[name] = value() if isinstance(value, BaseField) else value
        return ret


class Fields(object):
    def __init__(self, **kwargs):
        self.fields = list()
        self += kwargs

    def __iter__(self):
        for item in self.fields:
            yield item

    def __add__(self, other: Dict):
        for key, val in other.items():
            self.fields.append(BaseField(**{key: val}))
        return self


class BaseItem(Base):
    def __init__(self, fields: Fields):
        self.fields = fields

    def __iter__(self):
        for item in self.fields:
            yield {self._name_: item()}

    def __call__(self):
        return [item for item in self]

    def add(self, **kwargs):
        self.fields += kwargs


class Term(BaseItem):
    _name_ = 'term'


class Match(BaseItem):
    _name_ = 'match'


class Range(BaseItem):
    _name_ = 'range'


class Wildcard(BaseItem):
    _name_ = 'wildcard'


class BaseQuery(Base):
    def __init__(self, *items):
        self.items = list(items)

    def add(self, item: BaseItem):
        self.items.append(item)

    def __call__(self):
        ret = list()
        for item in self.items:
            tmp = item()
            if isinstance(tmp, List):
                ret.extend(tmp)
            elif isinstance(tmp, Dict):
                ret.append(tmp)
        return {self._name_: ret}


class Must(BaseQuery):
    _name_ = 'must'


class MustNot(BaseQuery):
    _name_ = 'must_not'


class Filter(BaseQuery):
    _name_ = 'filter'


class Should(BaseQuery):
    _name_ = 'should'


class Bool(Base):
    def __init__(self, *queries):
        self._name_ = 'bool'
        self.queries = list(queries)

    def add(self, query: Base):
        self.queries.append(query)

    def deal_queries(self, item, ret: Dict):
        for key, val in item().items():
            if ret.get(key):
                ret[key].extend(val)
            else:
                ret[key] = val
        return ret

    def __call__(self):
        ret = dict()
        for item in self.queries:
            ret = self.deal_queries(item, ret)
        if 'should' in ret:
            ret['minimum_should_match'] = 1
        return {self._name_: ret}


class Sort(Base):
    def __init__(self, **kwargs):
        self._name_ = 'sort'
        self.sorts = list()
        for key, val in kwargs.items():
            self.sorts.append(BaseField(**{key: val}))

    def __call__(self, *args, **kwargs):
        return {self._name_: [item() for item in self.sorts]}


class Collapse(Base):
    """ 有去重的效果，但是返回的数据总量是去重前的
        通过某个字段折叠数据"""

    def __init__(self, field: str):
        """ field 去重的字段 """
        self._name_ = 'collapse'
        self.field = field

    def __call__(self):
        return {self._name_: {'field': self.field}}


class Update(Base):
    def __init__(self, **params):
        self._name_ = 'update'
        self.params = params
        self.lang = 'painless'

    def __call__(self):
        source = str()
        for key in self.params:
            source += f'{";" if source else ""}ctx._source.{key}=params.{key}'
        return {'script': {'source': source, 'params': self.params, 'lang': self.lang}}


class ESPagination(Base):
    def __init__(self, page=1, page_size=20, limit=10000):
        self.page = page
        self.limit = limit
        self.page_size = page_size

    def __call__(self):
        from_ = (self.page - 1) * self.page_size
        if from_ >= self.limit:
            return {'size': 0, 'from': self.limit}

        if self.page * self.page_size > self.limit:
            self.page_size = self.limit - from_

        return {'size': self.page_size, 'from': from_}


class Q(Base):
    _name_ = 'query'
    Q_ITEM_TYPE = {'term': Term, 'match': Match, 'range': Range}
    Q_QUERY_TYPE = {'must': Must, 'filter': Filter, 'should': Should}

    def __init__(self, *queries):
        self.queries = list(queries)

    def __add__(self, other):
        return self.__and__(other)

    def __and__(self, other):
        if isinstance(other, self.__class__):
            self.queries.extend(other.queries)
        elif isinstance(other, BaseQuery):
            self.queries.append(other)
        return self

    def __or__(self, other):
        if isinstance(other, BaseQuery):
            self.queries = [Should(Bool(*self.queries), Bool(other))]
        elif isinstance(other, self.__class__):
            self.queries = [Should(Bool(*self.queries), Bool(*other.queries))]
        return self

    def __call__(self,
                 sort: Sort = None,
                 pagination: ESPagination = None,
                 collapse: Collapse = None,
                 updater: Update = None):
        ret = {self._name_: Bool(*self.queries)()}
        if sort:
            ret.update(sort())
        if pagination:
            ret.update(pagination())
        if collapse:
            # 去重
            ret.update(collapse())
        if updater:
            # 更新数据
            ret.update(updater())
        return ret

    @classmethod
    def common(cls, item_typ, query_typ, **kwargs) -> "Q":
        tmp = cls.Q_ITEM_TYPE[item_typ](Fields(**kwargs))
        return cls(cls.Q_QUERY_TYPE[query_typ](tmp))

    @classmethod
    def must(cls, item_typ, **kwargs) -> "Q":
        return cls.common(item_typ, 'must', **kwargs)

    @classmethod
    def filter(cls, item_typ, **kwargs) -> "Q":
        return cls.common(item_typ, 'filter', **kwargs)

    @classmethod
    def should(cls, item_typ, **kwargs) -> "Q":
        return cls.common(item_typ, 'should', **kwargs)


class SearchSyntax:
    """ 搜索语法 """

    def __init__(self, **commands):
        self.commands = commands

    def deal(self, key: str, sep: str = ':'):
        tmp_key, conditions = key.replace(f'{sep}', f'{sep} '), list()
        if 'AND' in tmp_key:
            conditions.append('AND')
            for item in [i.strip() for i in tmp_key.split('AND') if i]:
                if 'OR' in item:
                    sub_conditions = ['OR']
                    for item in [i.strip() for i in item.split('OR') if i]:
                        tmp = [i.strip() for i in item.split(f'{sep} ') if i]
                        sub_conditions.append({self.commands[tmp[0]]: tmp[1]})
                    conditions.append(sub_conditions)
                else:
                    tmp = [i.strip() for i in item.split(f'{sep} ') if i]
                    conditions.append({self.commands[tmp[0]]: tmp[1]})
        elif 'OR' in tmp_key:
            conditions.append('OR')
            for item in [i.strip() for i in tmp_key.split('OR') if i]:
                tmp = [i.strip() for i in item.split(f'{sep} ') if i]
                conditions.append({self.commands[tmp[0]]: tmp[1]})
        else:
            tmp = [i.strip() for i in tmp_key.split(f'{sep} ') if i]
            if len(tmp) > 1:
                conditions = {self.commands[tmp[0]]: tmp[1]}
            else:
                conditions = ['OR', {'content': key}, {'group_name': key}, {'sender': key}]
        return conditions

    def _analyze_item(self, item: Dict):
        for key, val in item.items():
            if val.startswith('-'):
                return Bool(MustNot(Match(Fields(**{key: val[1:]}))))
            else:
                return Match(Fields(**item))

    def analyze(self, conditions, sub=False):
        if isinstance(conditions, Dict):
            return Filter(self._analyze_item(conditions))

        ctrl, items = conditions[0], list()
        while conditions:
            item = conditions.pop()
            if isinstance(item, List):
                items.append(self.analyze(item, sub=True))
            elif isinstance(item, Dict):
                items.append(self._analyze_item(item))
            else:
                break
        if ctrl == 'AND':
            return Filter(*items)
        elif ctrl == 'OR':
            if sub:
                return Bool(Should(*items))
            else:
                return Should(*items)


class Result(object):
    def __init__(self, result):
        self.result = result

    def total(self):
        return int(self.result.get('hits', {}).get('total', {}).get('value', 0))

    def hits(self):
        """ 获取查询数据列表 """
        return self.result.get('hits', {}).get('hits', [])

    def __iter__(self):
        """ 遍历结果 """
        for item in self.hits():
            yield BaseData(**item['_source'])


class ESHelper(object):
    def __init__(self, es: Elasticsearch, index: str = None, index_prefix: str = None):
        self.es = es
        if index:
            self.index = index
        elif index_prefix:
            self.index_prefix = index_prefix
            self.index = self.get_index_name(index_prefix)
        else:
            self.index = None

    def flush_index(self):
        self.index = self.get_index_name(self.index_prefix)

    def get_index_name(self, prefix: str = None):
        ret = self.es.indices.get_alias().keys()
        if prefix:
            ret = [item for item in ret if item.startswith(prefix)]
        if len(ret) > 0:
            return sorted(ret, reverse=True)[0]

    def search(self, body: Dict):
        if self.index:
            return Result(self.es.search(index=self.index, body=body, request_timeout=9999))

    def insert(self, body: Dict):
        self.es.index(index=self.index, body=body, refresh=True)

    def update(self, body: Dict):
        self.es.update_by_query(index=self.index, body=body, refresh=True, request_timeout=9999)

    def exists(self, body: Dict):
        body['size'] = 0
        return self.search(body).total() > 0

    @classmethod
    def del_mapping(cls, es: Elasticsearch, index: str):
        if es.indices.exists(index):
            es.indices.delete(index)

    @classmethod
    def create_mapping(cls, es: Elasticsearch, properties: List, index: str):
        mappings = {'mappings': {'properties': dict()}}
        properties_ = mappings['mappings']['properties']
        for item in properties:
            properties_.update(item.get_feild())
        es.indices.create(index=index, body=mappings)

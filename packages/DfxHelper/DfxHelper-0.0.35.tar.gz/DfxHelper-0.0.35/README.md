# 辅助工具库

* 其他辅助工具： helper
* 时间辅助工具： time_helper

## 安装

pip install dfxhelper

## 使用
``` python
from dfx_utils.helper import random_str
tmp_str = random_str(32)
```

## Elasticsearch Orm

对 ES 常用操作做了一些封装，简便了查询与结果的处理

```python
from es_helper import ESHelper, Q as ES7_Q, Sort, ESPagination, Collapse, Result, Update
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts='http://127.0.0.1:9200', http_auth=['aaaa', 'bbbbb'], timeout=30,
                       max_retries=10, retry_on_timeout=True)
es_helper = ESHelper(es, index='xxxxx')

q = ES7_Q.must('term', sender='L')
# and 逻辑
q &= ES7_Q.filter('term', group_name='HC998')  # 或者 q += Q.must('term', group_name='HC998')
# or 逻辑
q |= ES7_Q.should('match', sender='天道酬勤', group_name='anlei1')
# 排序
sort = Sort(group_name='desc')
# 分页
pagination = ESPagination(1, 100, 1000)
# 折叠聚合，类似去重
collapse = Collapse('sender')
# 条件更新
update = Update(sender=1)
# es_helper.update(q(updater=update))
print(q(sort=sort, pagination=pagination, collapse=collapse, updater=update))
# {'query': {'bool': {'should': [{'bool': {'must': [{'term': {'sender': 'L'}}], 'filter': [{'term': {'group_name': 'HC998'}}]}}, {'bool': {'should': [{'match': {'sender': '天道酬勤'}}, {'match': {'group_name': 'anlei1'}}], 'minimum_should_match': 1}}], 'minimum_should_match': 1}}, 'sort': [{'group_name': 'desc'}], 'size': 100, 'from': 0, 'collapse': {'field': 'sender'}}
result: Result = es_helper.search(q(sort=sort, pagination=pagination, collapse=collapse))

##### 搜索语法
from es_helper import SearchSyntax

tmp = SearchSyntax(sender='sender', group_name='group_name', content_hash='content_hash')
conditions = tmp.deal('group_name: HC998 OR group_name: anlei1')
query = tmp.analyze(conditions)
q = ES7_Q(query)
# q => {"query": {"bool": {"should": [{"term": {"group_name": "anlei1"}}, {"term": {"group_name": "HC998"}}], "minimum_should_match": 1}}}
conditions = tmp.deal('group_name: HC998 AND group_name: anlei1')
query = tmp.analyze(conditions)
q = ES7_Q(query)
# q => {"query": {"bool": {"filter": [{"term": {"group_name": "anlei1"}}, {"term": {"group_name": "HC998"}}]}}}
conditions = tmp.deal('group_name: HC998 OR group_name: anlei1 AND sender: 天道酬勤')
query = tmp.analyze(conditions)
q = ES7_Q(query)
# q => {"query": {"bool": {"filter": [{"term": {"sender": "\u5929\u9053\u916c\u52e4"}}, {"bool": {"should": [{"term": {"group_name": "anlei1"}}, {"term": {"group_name": "HC998"}}], "minimum_should_match": 1}}]}}}
conditions = tmp.deal('group_name: HC998 OR group_name: anlei1 AND sender: 天道酬勤 OR sender: L')
query = tmp.analyze(conditions)
q = ES7_Q(query)
# q => {"query": {"bool": {"filter": [{"bool": {"should": [{"term": {"sender": "L"}}, {"term": {"sender": "\u5929\u9053\u916c\u52e4"}}], "minimum_should_match": 1}}, {"bool": {"should": [{"term": {"group_name": "anlei1"}}, {"term": {"group_name": "HC998"}}], "minimum_should_match": 1}}]}}}
conditions = tmp.deal('TG128')
query = tmp.analyze(conditions)
q = ES7_Q(query)
# => {"query": {"bool": {"should": [{"match": {"sender": "TG128"}}, {"match": {"group_name": "TG128"}}, {"match": {"content": "TG128"}}], "minimum_should_match": 1}}}
```

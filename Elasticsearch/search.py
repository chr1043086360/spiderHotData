from elasticsearch import Elasticsearch

es = Elasticsearch()
#######################################################################################################
# 诗词作品收录排行榜
# res = es.search(index="poetry")
# ret = es.search(index='poetry', body={'size': 0, 'aggs': {
#                 'authors': {"terms": {"field": "author"}}}})
# for item in ret['aggregations']['authors']['buckets']:
#     print(item['key'], item['doc_count'])

#######################################################################################################
# 最热门词牌排行榜
# ret = es.search(index='poetry', body={'size': 0, 'aggs': {
#                 'epigraphs': {"terms": {"field": "epigraph", 'size': 11}}}})

# for item in ret['aggregations']['epigraphs']['buckets']:
#     print(item['key'], item['doc_count'])

#######################################################################################################
# ElasticSearch使用了Fielddata缓存技术，要对这样的字段进行聚合，首先要开启字段的Fielddata
es.index(index='poetry', doc_type='_mapping', body={
         "properties": {"content": {"type": "text", "fielddata": True}}})

#######################################################################################################
# 文字频率排行榜
# ret = es.search(index='poetry', body={'size': 0, 'aggs': {
#                 'content': {"terms": {"field": "content", 'size': 20}}}})

# for item in ret['aggregations']['content']['buckets']:
#     print(item['key'], item['doc_count'])

#######################################################################################################
# 字高亮显示
# ret = es.search(index='poetry', body={"query": {
#                 "match": {"content": "江"}}, "highlight": {"fields": {"content": {}}}})
# print(ret['hits']['total']['value'])
# for item in ret['hits']['hits']:
#     print(item['_source']['title'], item['_source']['author'])
#     print(item['highlight']['content'])

#######################################################################################################
# 两个字的高亮
condition = {
    "query": {
        "match": {
            "content": {
                "query": "江 水",
                "operator": "and"
            }
        }
    },
    "highlight": {
        "fields": {
            "content": {}
        }
    }
}

ret = es.search(index='poetry', body=condition)
print(ret['hits']['total']['value'])
for item in ret['hits']['hits']:
    print(item['_source']['title'], item['_source']['author'])
    print(item['highlight']['content'])

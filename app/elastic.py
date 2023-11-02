import elasticsearch
from app import es

def delete_by_id(index, id):
    try:
        es.delete(index=index, id=id)
        return True
    except elasticsearch.NotFoundError:
       return False

def query_index_by_text(index, text):
    search = es.search(
        index=index,
        size=20,
        query = {'multi_match': {'query': text, 'fields': ['*']}})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids

def query_index_by_id(index, id):
    result = es.search(index=index, size=1, query={
            "match": {
                'id': id
            }
        })["hits"]["hits"]
    return result

def add_to_index(index, model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index=index, id=model.id, body=payload)

# Импортировали данные в Индекс Эластика используя add_to_index через cmd.
# Обязательно проверьте запущен ли Elasticsearch через cmd или как сервис!
# Полный код импорта через интепретатор Python:
# from app.models import Docs
# from app.elastic import add_to_index
# for post in Docs.query.all():\ 
#     add_to_index('docs', post)
#
# Удалить индекс из эластика:
# from app import es
# es.indices.delete(index='docs')
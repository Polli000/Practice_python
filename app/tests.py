import unittest, time

import app
from elastic import query_index_by_text

class Test1(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_true_delete(self):
        response = self.app.delete("/delete/?id=52").data.decode()
        assert response == 'True'
    
    def test_delete_invalid_id(self):
        response = self.app.delete("/delete/?id=12345").data.decode()
        assert response == 'Not found post with such id'

class Test2(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_false_delete(self):
        response = self.app.delete("/delete/?id=52").data.decode()
        assert response == 'Not found post with such id'
    
    def test_get_ids(self):
        response = query_index_by_text('docs', 'святой')
        assert response == [547, 871, 872]

class Test3(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_search_by_text(self):
        response = self.app.get("/search/?text=админам")
        assert response.status_code == 200

# Все работает, но тест не проходит, потому что delete выполняется параллельно и
# к возвращению response, данные все еще в базе данных. Решили с помощью задержки.
class Test4(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_ids_after_delete(self):
        self.app.delete("/delete/?id=547")
        time.sleep(2)
        response = query_index_by_text('docs', 'святой')
        assert response == [871, 872]

if __name__ == '__main__':
    unittest.main()
        
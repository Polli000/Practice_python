from app import db
from datetime import datetime

DATETIME_PATTERN = r"%Y-%m-%d %H:%M:%S"

class Docs(db.Model):
    __searchable__ = ['text']
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime)
    rubrics = db.Column(db.String())

    def __init__(self, id: int, text: str, raw_created_date: str, rubrics: str):
        self.id = id
        self.text = text
        self.created_date = datetime.strptime(raw_created_date, DATETIME_PATTERN)
        self.rubrics = rubrics

    def as_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_date": self.created_date.strftime(DATETIME_PATTERN),
            "rubrics": self.rubrics,
        }

# Создали базу данных через flask db init
# Добавили столбцы через миграции flask db migrate и flask db upgrade.
# После используя программу "DB Browser for SQLite" удалили индекс и импортировали
# csv файл. После возвращали id в этой же программе.

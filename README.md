# mydjango

## やること
Djangoを使用して、pythonでWebサービスを実装する。
（→URLは[こちら](http://okmethod.pythonanywhere.com/ "http://okmethod.pythonanywhere.com/")）

## 目的
- Webサービス実装の練習をする。
- MVC(Model/View/Controller)と対比させつつ、MTV(Model, Template, View)に基づいた設計の練習をする。

## ディレクトリ構成
    .
    ├── README.md
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    │
    ├── config
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── <apps>
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── forms.py
    │   ├── apps.py
    │   └── tests.py
    │
    ├── staticfiles
    │   ├── css
    │   │   └── *.css
    │   └── image
    │       └── *
    │      
    └── templates
        └── <apps>
            └── *.html

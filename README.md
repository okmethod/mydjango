# mydjango

---
## やること
Djangoを使用して、pythonでWebサービスを実装する。


---
## 目的
- AWSインフラ構築の練習をする。
- Webサービス構築に必要なMWに触れる。
- Webサービス実装の練習をする。
- MVC(Model/View/Controller)と対比させつつ、MTV(Model, Template, View)に基づいた設計の練習をする。


---
## アーキテクチャ

![代替テキスト](https://github.com/okmethod/mydjango/blob/master/staticfiles/image/architecture.drawio.png "画像タイトル")

~~[URL](http://dev-mydjango-web-alb-915478302.ap-northeast-1.elb.amazonaws.com) （標準サービス提供時間：9:00-17:00）~~

ALBの料金が高いので一時削除中

---
## ディレクトリ構成
    .
    ├── README.md
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    │
    ├── etc
    │   └── *
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
    │   ├── js
    │   │   └── *.js
    │   └── image
    │       └── *
    │      
    └── templates
        └── <apps>
            └── *.html

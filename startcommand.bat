rem 仮想環境の起動
myvenv\Scripts\activate

rem Webサービスの起動
python manage.py runserver

rem superユーザの作成
python manage.py createsuperuser

rem DBマイグレーション
python manage.py makemigrations
python manage.py migrate

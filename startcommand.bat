rem 仮想環境の作成
python -m venv myvenv

rem 仮想環境の起動
myvenv\Scripts\activate

rem pipによるパッケージインストール
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rem Webサービスの起動
python manage.py runserver

rem superユーザの作成
python manage.py createsuperuser

rem DBマイグレーション
python manage.py makemigrations
python manage.py migrate

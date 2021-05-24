# 仮想環境の有効化
workon okmethod.pythonanywhere.com

# PythonAnywhereヘルパーツールのインストール
pip3.6 install --user pythonanywhere

# GitHubのソースからWebサービスを起動
pa_autoconfigure_django.py --python=3.6 https://github.com/okmethod/mydjango.git
# GitHubからコードをダウンロード
# PythonAnywhere上に仮想環境を作成
# 一部のデプロイメント設定で設定ファイルを更新
# manage.py migrateコマンドを使ってPythonAnywhere上のデータベースをセットアップ
# 静的ファイルの設定
# APIを通じてPythonAnywhereがWebサービスを提供するように設定

# GitHubのソースをpull
cd ~/okmethod.pythonanywhere.com
git reset --hard HEAD~1
git pull

# DEBUGモードをOFFに切り替え
python switch_debug_mode.py off

# staticファイルを再読み込み
python manage.py collectstatic

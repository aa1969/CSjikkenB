#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import io
import re
import textwrap
import csv

# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

localhost=False

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
app_dir = os.path.dirname(os.path.abspath(__file__))
dbname = os.path.join(app_dir, 'database.db')

# テーブルの作成
def createTable():
    # データベース接続とカーソル生成
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    # テーブルの作成
    create_table = 'create table if not exists users (date varchar(64), temperature float, weather varchar(64))'
    cur.execute(create_table)
    # コミット（変更を確定）
    con.commit()
    # カーソルと接続を閉じる
    cur.close()
    con.close()

createTable()
                   
# データベースへの登録
def registerWeather(std_date, std_temperature, std_weather):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    con.text_factory = str

    # SQL文（insert）の作成と実行
    sql = 'insert into users (date, temperature, weather) values (?,?,?)'
    cur.execute(sql, (std_date, std_temperature, std_weather))
    con.commit()

    cur.close()
    con.close()

# データの削除
def deleteWeather(std_date):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    sql = 'delete from users where date = ?'
    cur.execute(sql, (std_date,))
    con.commit()
    cur.close()
    con.close()

# 指定された条件に一致するレコードを取得
def searchWeather(search_date=None, search_temperature=None, search_weather=None):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    con.text_factory = str

    # SQL文の構築
    sql = 'SELECT * FROM users WHERE 1=1'
    params = []

    if search_date:
        sql += ' AND date = ?'
        params.append(search_date)
    if search_temperature:
        sql += ' AND temperature = ?'
        params.append(float(search_temperature))
    if search_weather:
        sql += ' AND weather = ?'
        params.append(search_weather)

    cur.execute(sql, params)
    results = cur.fetchall()
    cur.close()
    con.close()
    return results

# 登録情報一覧の取得
def getAllWeathers():
    # データベース接続とカーソル生成
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    con.text_factory = str

    # SQL文（select）の作成と実行
    sql = 'select * from users'
    cur.execute(sql)
    lists = cur.fetchall()

    cur.close()
    con.close()

    return lists

# CSSファイルなどを送信（リファレンスWEBサーバ実行時のみ使用）
def serveFile(environ,start_response):
    # 拡張子とコンテンツタイプ（必要に応じて追加すること）
    types = {'.css': 'text/css', '.jpg': 'image/jpg', '.png': 'image/png'}
    
    # static ディレクトリ以下の指定ファイルを開いてその内容を返す．
    # ファイルが無ければエラーを返す．
    #
    assert(re.match('/static/', environ['PATH_INFO']))
    filepath = '{dir}/{path}'.format(dir=app_dir, path=environ['PATH_INFO'])
    ext  = os.path.splitext(filepath)[1]
    
    if os.path.isfile(filepath) and ext in types:
        try:
            with open(filepath, "rb") as f:
                r = f.read()
            binary_stream = io.BytesIO(r)
        except:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b"Internal server error"]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not found."]

    start_response('200 OK', [('Content-Type', types[ext])])
    return binary_stream

# CSVファイルを読み取って特定の列を選び、データベースに登録する関数
def importCsvToDatabase(csv_path):
    with open(csv_path, newline='', encoding='shift_jis') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ
        for i, row in enumerate(reader):
            if i < 4:  # 最初の6行をスキップ
                continue
            if not any(row):  # 空行や空白行をスキップ
                continue
            # 特定の列（例：0列目と2列目）を選択して登録
            if len(row) >= 5:  # インデックスエラーを防ぐため、列数をチェック
                try:
                    std_date = row[0]  # 1列目のデータ
                    std_temperature = row[1]
                    std_weather = row[4]      # 3列目のデータ
                    registerWeather(std_date, float(std_temperature), std_weather)
                except ValueError:
                    print(f"無効なデータ: {row}")
                except sqlite3.IntegrityError:
                    print(f"重複エラー: {row[0]} は既に登録されています。")

importCsvToDatabase("data/data.csv") 


# アプリケーション本体
def application(environ,start_response):
    msg = ''  # msg を初期化

    if localhost and re.match('/static/', environ['PATH_INFO']):
        ''' リファレンスWEBサーバ実行時のみ
             このwsgiスクリプトを実行しているカレントディレクトリ以下に
             static というディレクトリを作って，default.cssというファイルを置いておくと，
             http://localhost:8080/static/default.css でファイルがダウンロードできる．
        '''
        return serveFile(environ,start_response)

    # HTML（共通テンプレート）
    tmpl = textwrap.dedent('''
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <title>WSGI テスト</title>
    <link rel="stylesheet" href="/static/default.css"> 
    </head>
    {body}
    </html>
    ''')

    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)

    if 'register' in form:
        # 入力フォームで登録ボタンがクリックされた場合

        # フォームデータから各フィールド値を取得
        v1 = form.getvalue("v1")
        v2 = form.getvalue("v2")
        v3 = form.getvalue("v3")

        if v1 != '' and v2 != '' and v3 != '':
            try:
                # 気温を浮動小数点数に変換
                temperature = float(v2)
                # データベースへ学生の登録
                registerWeather(v1, temperature, v3)
                msg = '登録しました。'
            except ValueError:
                msg = '登録失敗：気温には数値を入力してください。'
        else:
            msg = '登録失敗：空になっている入力項目があります。'

        # データベースの登録情報一覧の取得
        weathers_list = getAllWeathers()

        # 一覧のHTML形式への変換
        list = ''
        for row in weathers_list:
            list += f'<li>{row[0]}, {str(row[1])}, {row[2]}</li>\n'

        bcontent = textwrap.dedent('''
        <body style="text-align: center;">
        <p style>{message}</p>
        <hr>
        <div class="ol1" style="display: inline-block; text-align: left;">
        <h2 style="text-align: center;">一覧表示</h2>
        <ul style="list-style-type: none; padding: 0;">
        {slist}
        </ul>
        </div>
        <br>
        <a href="./102210017.wsgi" style="display: inline-block; margin-top: 20px; font-size: 1.2em;">前のページに戻る</a>
        </body>
        ''').format(message=msg, slist=list)

    elif 'delete' in form:
        # 削除ボタンがクリックされた場合

        # フォームデータから各フィールド値を取得
        std_date = form.getvalue("v1")
        search_results = searchWeather(std_date, '', '')
        if std_date:
            search_results = searchWeather(std_date, '', '')
            if len(search_results) == 0:
                msg = '削除失敗：日時が' + str(std_date) + 'のデータは見つかりませんでした。'
            else:    
                deleteWeather(std_date)
                msg = '日時が' + str(std_date) +'のデータを削除しました。'
        else:
            msg = '削除失敗：日時が指定されていません。'

        # データベースの登録情報一覧の取得
        weathers_list = getAllWeathers()

        # 一覧のHTML形式への変換
        list = ''
        for row in weathers_list:
            list += f'<li>{row[0]}, {str(row[1])}, {row[2]}</li>\n'

        bcontent = textwrap.dedent('''
        <body style="text-align: center;">
        <p style>{message}</p>
        <hr>
        <div class="ol1" style="display: inline-block; text-align: left;">
        <h2 style="text-align: center;">一覧表示</h2>
        <ul style="list-style-type: none; padding: 0;">
        {slist}
        </ul>
        </div>
        <br>
        <a href="./102210017.wsgi" style="display: inline-block; margin-top: 20px; font-size: 1.2em;">前のページに戻る</a>
        </body>
        ''').format(message=msg, slist=list)

    elif 'search' in form:
        search_results = []
        # 検索ボタンがクリックされた場合
        search_date = form.getvalue("v1")
        search_temperature = form.getvalue("v2")
        search_weather = form.getvalue("v3")
        try:
            if search_temperature != '':
                # 気温を浮動小数点数に変換
                search_temperature = float(search_temperature)
            # 検索結果の取得
            search_results = searchWeather(search_date, search_temperature, search_weather)
            msg = str(len(search_results))+'件のデータが見つかりました。'
        except ValueError:
            msg = '検索失敗：気温には数値を入力してください。'

        # 一覧のHTML形式への変換
        list = ''
        for row in search_results:
            list += f'<li>{row[0]}, {str(row[1])}, {row[2]}</li>\n'

        bcontent = textwrap.dedent('''
        <body style="text-align: center;">
        <p style>{message}</p>
        <hr>
        <div class="ol1" style="display: inline-block; text-align: left;">
        <h2 style="text-align: center;">一覧表示</h2>
        <ul style="list-style-type: none; padding: 0;">
        {slist}
        </ul>
        </div>
        <br>
        <a href="./102210017.wsgi" style="display: inline-block; margin-top: 20px; font-size: 1.2em;">前のページに戻る</a>
        </body>
        ''').format(message=msg, slist=list)        

    else:
        # デフォルトページ（入力フォーム表示）

        # HTML（入力フォーム部分）
        bcontent = textwrap.dedent('''
        <body>
        <div class="header" style="text-align: center;">名古屋市の気象情報 102210017 安藤駿</div>
        <div class="form1" style="text-align: center;">
        <form>
        日時 <input type="text" name="v1"><br>
        気温 <input type="text" name="v2"><br>
        天気 <input type="text" name="v3"><br>
        <div style="text-align: left; color: gray; margin: 0 auto; width: 500px; padding-left: 200px;">
            <span>気温の欄には数値を入力してください</span><br>
            <span>登録をするときはすべての項目に入力してください</span><br>
            <span>削除をするときは日時の項目に入力してください</span><br>
        </div>
        <span style="color: gray; font-size: 12px;"></span><br>
        <button type="submit" name="search">検索</button>
        <button type="submit" name="register">登録</button>
        <button type="submit" name="delete">削除</button>                           
        </form>
        </div>
        </body>
        ''')


    html = tmpl.format(body=bcontent)
    html = html.encode('utf-8')

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 sample.wsgi）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 sample.wsgi ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 50017
    localhost = True
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()

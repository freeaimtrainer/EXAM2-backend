from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from datetime import datetime
import sqlite3
import logging
import re 
import os


app = Flask(__name__)
app.secret_key = 'super_secret_key'

# 路徑修改
def get_db_connection():
    conn = sqlite3.connect('shopping_data.db')
    if not os.path.exists('shopping_data.db'):
        logging.error(f"Database file not found at {'shopping_data.db'}")
        return None
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

def check_user_credentials(username, password):
    return username == "testuser" and password == "testpass"

@app.route()
def index():
    return
    
@app.route('/page_register', methods=['GET', 'POST'])
def page_register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # 帳號重複檢查
        if check_user_exists(username):
            insert_or_update_user(username, password, email)
            return jsonify({"status": "success_update", "message": "帳號已存在，成功修改密碼或信箱"})

        # 密碼檢查：長度
        if len(password) < 8:
            return jsonify({"status": "error", "message": "密碼必須超過8個字元"})
            
        # 密碼檢查：包含大小寫英文
        if not (re.search(r'[a-z]', password) and re.search(r'[A-Z]', password)):
            return jsonify({"status": "error", "message": "密碼必須包含英文大寫和小寫"})
            
        # 信箱檢查：格式
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"status": "error", "message": "Email 格式不符重新輸入"})
            
        # 全部符合後，寫入資料庫
        if insert_or_update_user(username, password, email):
            return jsonify({"status": "success", "message": "註冊成功"})
        else:
            # 處理其他可能的資料庫寫入失敗
            return jsonify({"status": "error", "message": "資料庫寫入失敗，請稍後再試"})
       
    return render_template('page_register.html')


def login_user(username, password):
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                return {"status": "success", "message": "Login successful"}
            else:
                return {"status": "error", "message": "Invalid username or password"}
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return {"status": "error", "message": "An error occurred"}
        finally:
            conn.close()
    else:
        return {"status": "error", "message": "Database connection error"}

@app.route('/page_login' , methods=['GET', 'POST'])
def page_login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            result = login_user(username, password)
            if result["status"] == "success":
                session['username'] = username
            return jsonify(result)
        return render_template('page_login.html')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 補齊剩餘副程式


# 補齊空缺程式碼
if __name__ == '__main__':
    app.run(debug=True)



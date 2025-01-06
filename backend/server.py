import csv
from flask import Flask, jsonify, render_template, request
import os

# Flask 앱 생성 (static_folder 및 template_folder 설정)
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')

# 사용자 포트폴리오 데이터
user_portfolio = {"balance": 10000, "stocks": {}}

@app.route('/')
def home():
    stocks = []
    try:
        # stocks.csv 파일 경로 설정
        file_path = os.path.join(os.path.dirname(__file__), 'stocks.csv')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stocks.append(row)
    except FileNotFoundError:
        return "stocks.csv file not found", 404
    except Exception as e:
        return str(e), 500

    # index.html 렌더링하며 stocks 데이터 전달
    return render_template('index.html', stocks=stocks)

@app.route('/stocks')
def get_stocks():
    stocks = []
    try:
        # stocks.csv 파일 경로 설정
        file_path = os.path.join(os.path.dirname(__file__), 'stocks.csv')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stocks.append(row)
        return jsonify({"stocks": stocks})
    except FileNotFoundError:
        return jsonify({"error": "stocks.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/buy', methods=['POST'])
def buy_stock():
    data = request.json
    symbol = data['symbol']
    quantity = int(data['quantity'])
    price = float(data['price'])
    total_cost = price * quantity

    if user_portfolio['balance'] >= total_cost:
        user_portfolio['balance'] -= total_cost
        if symbol in user_portfolio['stocks']:
            user_portfolio['stocks'][symbol] += quantity
        else:
            user_portfolio['stocks'][symbol] = quantity
        return jsonify({"message": "Stock purchased!", "portfolio": user_portfolio})
    else:
        return jsonify({"message": "Insufficient balance!"}), 400

if __name__ == '__main__':
    app.run(debug=True)



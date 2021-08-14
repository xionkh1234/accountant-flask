from flask import Flask, render_template, jsonify, request
from accountant import manager
from manager import NotEnoughMoneyException, NotEnoughStockException

app = Flask(__name__)
manager.process()

@app.route("/")
def index():
  manager.process_action("magazyn", [])
  return render_template('index.html', stock=manager.stock)

@app.route("/buy")
def buy():
  return render_template('buy.html')

@app.route("/api/buy_product", methods=['POST']) # {'name': 'asd', 'price_one': '1', 'count': '22'}
def api_buy_product():
  request_json = request.get_json()
  try:
    manager.process_action("zakup", [request_json['name'], request_json['price_one'], request_json['count']])
    manager.save()

  except NotEnoughMoneyException:
    return jsonify({'status': 'NotEnoughMoney'})

  else:
    return jsonify({'status': 'ok', 'newBalance': manager.account})

@app.route("/sell")
def sell():
  return render_template('sell.html')

@app.route("/api/sell_product", methods=['POST']) # {'name': 'asd', 'price_one': '1', 'count': '22'}
def api_sell_product(): #NotEnoughStockException
  request_json = request.get_json()
  try:
    manager.process_action("sprzedaz", [request_json['name'], request_json['price_one'], request_json['count']])
    manager.save()
    
  except NotEnoughStockException:
    return jsonify({'status': 'NotEnoughStock'})

  else:
    return jsonify({'status': 'ok', 'newBalance': manager.account})

@app.route("/history")
def history():
  return render_template('history.html', history=manager.review('', ''))

@app.route("/history/<line_from>/<line_to>")
def history_bounds(line_from, line_to):
  return render_template('history.html', history=manager.review(line_from, line_to))

@app.route("/change_balance")
def change_balance():
  return render_template('change_balance.html')

@app.route("/api/change_balance", methods=['POST']) # {'name': 'asd', 'price_one': '1', 'count': '22'}
def api_change_balance(): #NotEnoughStockException
  request_json = request.get_json()
  try:
    manager.process_action("saldo", [request_json['value'], request_json['comment']])
    manager.save()
    
  except NotEnoughMoneyException:
    return jsonify({'status': 'NotEnoughMoney'})

  else:
    return jsonify({'status': 'ok', 'newBalance': manager.account})

@app.route("/api/get_bal", methods=['GET'])
def get_bal():
  return jsonify({'newBalance': manager.account})
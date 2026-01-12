from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB connection from .env
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/')
def index():
    products = list(mongo.db.products.find())
    return render_template('index.html', products=products, username=session.get('username'))

@app.route('/category/<category_name>')
def category_page(category_name):
    category_name = category_name.lower()
    products = list(mongo.db.products.find({'category': category_name}))
    return render_template('category.html', products=products, category=category_name.capitalize(), username=session.get('username'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return "Product not found", 404

    similar_products = list(
        mongo.db.products.find({
            'category': product['category'],
            '_id': {'$ne': ObjectId(product_id)}
        }).limit(4)
    )

    return render_template('product.html', product=product, similar_products=similar_products, username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        action = request.form.get('action')

        if not username or not password:
            flash("Username and password are required.")
            return render_template('login.html')

        user = mongo.db.users.find_one({'username': username})

        if action == 'login':
            if user and user['password'] == password:
                session['username'] = username
                return redirect(url_for('index'))
            flash("Invalid login credentials")

        elif action == 'register':
            if user:
                flash("Username already exists")
            else:
                mongo.db.users.insert_one({
                    'username': username,
                    'password': password,
                    'cart': []
                })
                session['username'] = username
                return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add-to-cart/<product_id>')
def add_to_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = mongo.db.users.find_one({'username': session['username']})
    cart = user.get('cart', [])
    cart.append(ObjectId(product_id))

    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'cart': cart}})
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = mongo.db.users.find_one({'username': session['username']})
    cart_ids = user.get('cart', [])

    cart_items = {}
    for pid in cart_ids:
        pid_str = str(pid)
        cart_items[pid_str] = cart_items.get(pid_str, 0) + 1

    products = mongo.db.products.find({'_id': {'$in': cart_ids}})
    item_details = {str(p['_id']): p for p in products}

    display_items = {}
    total = 0
    for pid, qty in cart_items.items():
        if pid in item_details:
            display_items[pid] = {'product': item_details[pid], 'quantity': qty}
            total += item_details[pid]['price'] * qty

    return render_template('cart.html', cart_items=display_items, total=total, username=session['username'])

@app.route('/remove-one/<product_id>')
def remove_one(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = mongo.db.users.find_one({'username': session['username']})
    cart = user.get('cart', [])

    try:
        cart.remove(ObjectId(product_id))
    except ValueError:
        pass

    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'cart': cart}})
    return redirect(url_for('view_cart'))

@app.route('/remove-all/<product_id>')
def remove_all(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = mongo.db.users.find_one({'username': session['username']})
    new_cart = [pid for pid in user.get('cart', []) if str(pid) != product_id]

    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'cart': new_cart}})
    return redirect(url_for('view_cart'))

@app.route('/add-n/<product_id>', methods=['POST'])
def add_n(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    count = int(request.form.get('count', 1))
    user = mongo.db.users.find_one({'username': session['username']})
    cart = user.get('cart', [])

    cart.extend([ObjectId(product_id)] * count)
    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'cart': cart}})
    return redirect(url_for('view_cart'))

@app.route('/place-order')
def place_order():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = mongo.db.users.find_one({'username': session['username']})
    cart = user.get('cart', [])

    if not cart:
        return "Cart is empty"

    mongo.db.orders.insert_one({
        'username': session['username'],
        'products': cart,
        'timestamp': datetime.utcnow()
    })

    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'cart': []}})
    return render_template('place_order.html', username=session['username'])

if __name__ == "__main__":
    app.run()


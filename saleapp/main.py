from flask import render_template, request, redirect
from saleapp import app, utils, login
from flask_login import login_user
from saleapp.admin import *
import os


@app.route('/')
def index():
    categories = utils.read_data()
    return render_template('index.html',
                           categories=categories)


@app.route('/products')
def product_list():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    products = utils.read_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('product-list.html',
                           products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id=product_id)
    return render_template('product-detail.html',
                           product=product)


@app.route('/login', methods=['post'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password == confirm:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            avatar = request.files["avatar"]

            avatar_path = 'images/upload/%s' % avatar.filename
            avatar.save(os.path.join(app.root_path,
                                     'static/',
                                     avatar_path))
            if utils.add_user(name=name, email=email, username=username,
                              password=password, avatar_path=avatar_path):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def get_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)

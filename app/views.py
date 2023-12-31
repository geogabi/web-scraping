from .models import Products, Items, Requests
from .initialize import db
from .scraper import save_link, save_request
from .charts import product_statistic, items_statistics, create_graphic
from .db_function import delete_db, save_db, paginate_db
from .email import send_mail

from flask import Blueprint, render_template, flash, request, redirect, url_for
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

views = Blueprint('views', __name__)
matplotlib.use('agg')
plt.style.use('fivethirtyeight')


@views.route('/', methods=['GET', 'POST'])
def home():
    products = paginate_db(Products)
    items = paginate_db(Items)
    requests = paginate_db(Requests)

# read the link from webpage and save in db
    if request.method == 'POST':
        product_link = request.form['link']
        product_found = Products.query.filter_by(link=product_link).first()
        if product_found:
            flash('Product already exist')
        else:
            product = Products(link=product_link, data=datetime.now())
            save_db(product)
            save_link(product)
            return redirect(url_for('.home'))

# send email
    for item in items:
        if item.price_increase[0] == '-':
            print('Sending')
            send_mail(item.title)
            print("Sent")

    return render_template('home.html', products=products, items=items, requests=requests)


@views.route('/view/<int:id>', methods=['POST', 'GET'])
def view_element(id):
    products = Products.query.filter_by(id=id)
    product = products.first()

    price = Items.query.filter_by(link_id=product.id).first()

    requests = Requests.query.filter_by(product_id=product.id).order_by(Requests.request_data.desc())
    last_request = requests.first()
    last_second_request = requests.offset(1).first()

    # create statistics
    try:
        # get general prices
        first_st = product_statistic(last_request.request_price, price.price)
        price.price_increase = first_st
        db.session.commit()
        try:
            # get prices from requests
            second_st = items_statistics(last_request.request_price, last_second_request.request_price)
            last_request.statistic = second_st
            db.session.commit()
        except:
            second_st = items_statistics(last_request.request_price, price.price)
            last_request.statistic = second_st
            db.session.commit()
    except Exception as e:
        print(e)
        return None

    if request.method == 'POST':
        save_request(product)

    return render_template('view.html', products=products, requests=requests, id=id, price=price)


# display charts
@views.route('/plot.png/<int:id>')
def plot(id):
    product = Products.query.filter_by(id=id)
    link = product.first()
    weeks = db.paginate(db.select(Requests).filter_by(product_id=link.id).order_by(Requests.request_data))

    # create charts
    y = [week.request_price for week in weeks]
    x = [week.request_data.strftime('%d-%m-%Y') for week in weeks]

    return create_graphic(x, y)


# delete a product
@views.route('/delete/<int:id>')
def delete(_id):
    delete_element = Products.query.filter_by(id=_id).first()
    delete_db(delete_element)

    return redirect(url_for('.home'))
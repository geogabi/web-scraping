from .initialize import db


# table for links
class Products(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    link = db.Column(db.String(400), unique=True, nullable=False)
    data = db.Column(db.DateTime)
    item = db.relationship('Items', backref='detail', lazy=True)
    requests = db.relationship('Requests', backref='requests', lazy=True)


# table for every data about product -- price, title
class Items(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    price = db.Column(db.Float)
    price_increase = db.Column(db.String, default='+0%')
    link_id = db.Column(db.Integer, db.ForeignKey('products.id'))


# table with all requests
class Requests(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    request_data = db.Column(db.DateTime)
    request_price = db.Column(db.Float)
    statistic = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

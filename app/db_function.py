from .initialize import db


def save_db(data):
    db.session.add(data)
    db.session.commit()


def delete_db(id: int):
    db.session.delete(id)
    db.session.commit()


paginate_db = lambda data: db.paginate(db.select(data).order_by(data.id))

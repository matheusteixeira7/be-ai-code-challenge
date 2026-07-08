from .. import db
from ..models import Account


def create_account(name, password, settings):
    acc = Account(name=name, password=password, settings=settings)
    db.session.add(acc)
    db.session.commit()
    return acc


def get_all_accounts():
    return Account.query.all()


def account_exists(acc_id):
    return bool(Account.query.filter_by(id=acc_id).count())


def delete_account(acc_id):
    Account.query.filter_by(id=acc_id).delete()
    db.session.commit()

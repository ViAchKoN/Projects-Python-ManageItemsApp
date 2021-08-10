from application import db


class Item(db.Model):
    __tablename__ = 'item'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE',
        ),
    )
    name = db.Column(db.String(32))
    user = db.relationship('User')

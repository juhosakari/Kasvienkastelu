from app import db
from app.models import User

u = User(name='kayttaja1')
f = User(name='kayttaja2')
h = User(name='kayttaja3')
g = User(name='kayttaja4')

db.session.add(u)
db.session.add(f)
db.session.add(h)
db.session.add(g)

db.session.commit()
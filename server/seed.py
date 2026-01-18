from app import app, db
from models import Message

with app.app_context():
    db.drop_all()
    db.create_all()

    messages = [
        Message(body="Hello, world!", username="Ian"),
        Message(body="How's it going?", username="Jess"),
        Message(body="Testing 123", username="Alex"),
    ]

    db.session.add_all(messages)
    db.session.commit()
    print("Database seeded!")

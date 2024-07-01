# server/app.py

from flask import Flask
from flask_migrate import Migrate

from models import db

# create a Flask application instance 
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)


if __name__ == '__main__':
    app.run(port=5556, debug=True)


# Add a new Pet 
@app.route('/add_pet')
def add_pet():
    # new Pet instance
    pet1 = Pet(name='Fido', species='Dog')

    db.session.add(pet1)

    # Commit 
    db.session.commit()

    return 'Added a new pet!'

@app.route('/pets')
def get_pets():
    pets = Pet.query.all()
    return {'pets': [pet.__repr__() for pet in pets]}

# Update 
@app.route('/update_pet/<int:id>')
def update_pet(id):
    # Retrieve pet
    pet = Pet.query.get(id)
    if pet:
        # Update
        pet.name = 'Fido the Mighty'
        db.session.commit()
        return f'Updated pet with id {id}'
    return f'Pet with id {id} not found'

# Delete
@app.route('/delete_pet/<int:id>')
def delete_pet(id):
    # Retrieve pet
    pet = Pet.query.get(id)
    if pet:
        # Delete the Pet 
        db.session.delete(pet)
        db.session.commit()
        return f'Deleted pet with id {id}'
    return f'Pet with id {id} not found'
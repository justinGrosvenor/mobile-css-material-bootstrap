import os
import tempfile
import pytest
from app import app, database, user_datastore, bcrypt, db_session, User

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['TESTING'] = True

    client = app.test_client()
    
    with app.app_context():
        database.init_db()

    yield client

    os.close
    os.unlink(app.config['DATABASE'])

def test_site(client):
    site = client.get('/')
    assert site.data != None

def test_create_user(client):
    hashed_pw = bcrypt.generate_password_hash('password').decode('utf-8')
    user_datastore.create_user(username='test', email='test@test.com', password=hashed_pw)
    db_session.commit()
    this_user = user_datastore.find_user(email='test@test.com')
    assert this_user != None

def test_delete_user(client):
    this_user = user_datastore.find_user(email='test@test.com')
    user_datastore.delete_user(this_user)
    db_session.commit()
    assert user_datastore.find_user(email='test@test.com') == None


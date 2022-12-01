import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import *

from App.main import create_app
from App.database import create_db
from App.models import  Author, Publication
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class AuthorUnitTests(unittest.TestCase):

    def test_new_author(self):
        author = Author("John","Doe","JohnDoe@mail.com","bobpass")
        assert author.first_name == "John" and author.last == "Doe" and author.email == "JohnDoe@mail.com"
    
    def test_author_toJSON(self):
        author = Author("John","Doe","JohnDoe@mail.com","bobpass")
        author_json = author.toJSON()
        self.assertDictEqual(author_json, {
            'id': None,
            'first_name': "John",
            'last_name': "Doe",
            'email': "JohnDoe@mail.com"
        })
    
    def test_password(self):
        author = Author("John","Doe","JohnDoe@mail.com","bobpass")
        self.assertFalse("bobpass",author.password)



class PublicationUnitTests(unittest.TestCase):
    def test_new_publication(self):
        authors = []
        publication = Publication("test", "comp", "10/10/10")
        author = Author("John","Doe","JohnDoe@mail.com","bobpass")
        self.assertTrue("test" == publication.title and publication.field == "comp" and publication.publication_date == "10/10/10")

    def test_publication_toDict(self):
        publication = Publication("Intro to Computer Science", "comp", "10/10/10")
        publication_json = publication.toDict()
        self.assertDictEqual(publication_json, {
            "id": None,
            "title": "Intro to Computer Science",
            "field": "comp",
            "publication_date": "10/10/10"
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate():
    user = create_user("Bob Moog", "bobpass")
    assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_author(self):
        author = create_user("Bob Moog", "05/08/2001", "BSc. Computer Science")
        assert author.name == "Bob Moog"

    def test_create_publication(self):
        publication=create_publication([{"title":"Intro to Computer Science"},{"authors":[author.toJSON() for author in authors]},{"coauthors":[coauthor.toJSON() for coauthor in coauthors]}])
        assert publication.title=="Intro to Computer Science"

    def test_get_author_json(self):
        author_json=get_author_json()
        self.assertListEqual([{"name": "Bob Moog"},{"dob":"05/08/2001"},{"qualifications":"BSc. Computer Engineering"}], author_json)


    def test_get_publication_json(self):
        publication_json= get_publication_json()
        self.assertListEqual([{"title":"Intro to Computer Science"},{"authors":[author.toJSON() for author in authors]},{"coauthors":[coauthor.toJSON() for coauthor in coauthors]}])

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

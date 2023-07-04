"""
Test cases for Customer Model

"""
import os
import logging
import unittest
from service.models import Customer, db
from service import app
from tests.factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
######################################################################
#  Customer   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomer(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
       

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """ It should always be true """
        self.assertTrue(True)


    def test_create_a_customer(self):
        """It should Create a product and assert that it exists"""
        customer = Customer(name="c1", id = 1, address = "address1", phone_number = "123456", email="c1@gmail.com", password = "c1")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.name, "c1")
        self.assertEqual(customer.address, "address1")
        self.assertEqual(customer.phone_number, "123456")
        self.assertEqual(customer.email, "c1@gmail.com")
        self.assertEqual(customer.password, "c1")


    def test_read_a_customer(self):
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        self.assertIsNotNone(customer.id)
        # Fetch it back
        found_customer = Customer.find(customer.id)
        self.assertEqual(found_customer.id, customer.id)
        self.assertEqual(found_customer.name, customer.name)
        self.assertEqual(found_customer.address, customer.address)
        self.assertEqual(found_customer.phone_number, customer.phone_number)
        self.assertEqual(found_customer.password, customer.password)
        self.assertEqual(found_customer.email, customer.email)
    



"""
Test cases for Customer Model

"""
import os
import logging
import unittest
from service.models import Customer, db
from service import app

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
    
    def test_find_customer(self):
        """It should Find a customer by ID"""
        customers = PetFactory.create_batch(5)
        for customers in customers:
            customers.create()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(customer.all()), 5)
        # find the 2nd customers in the list
        customers = customer.find(customers[1].id)
        self.assertIsNot(customers, None)
        self.assertEqual(customers.id, customers[1].id)
        self.assertEqual(customers.name, customers[1].name)
        self.assertEqual(customers.email, customers[1].email)
        self.assertEqual(customers.address, customers[1].address)
        self.assertEqual(customers.phone_number, customers[1].phone_number)

    def test_find_by_address(self):
        """It should Find Customers by Category"""
        customers = PetFactory.create_batch(10)
        for customers in customers:
            customers.create()
        address = customers[0].address
        count = len([customers for customers in customers if customers.address == address])
        found = customer.find_by_category(address)
        self.assertEqual(found.count(), count)
        for customers in found:
            self.assertEqual(customers.address, address)

    def test_find_by_name(self):
        """It should Find a customer by Name"""
        customers = PetFactory.create_batch(10)
        for customers in customers:
            customers.create()
        name = customers[0].name
        count = len([customers for customers in customers if customers.name == name])
        found = customer.find_by_name(name)
        self.assertEqual(found.count(), count)
        for customers in found:
            self.assertEqual(customers.name, name)

    def test_find_by_email(self):
        """It should Find Customers by email"""
        customers = PetFactory.create_batch(10)
        for customers in customers:
            customers.create()
        email = customers[0].email
        count = len([customers for customers in customers if customers.email == email])
        found = customer.find_by_availability(email)
        self.assertEqual(found.count(), count)
        for customers in found:
            self.assertEqual(customers.email, email)
    
    def test_find_by_phone_number(self):
        """It should Find Customers by phone_number"""
        customers = PetFactory.create_batch(10)
        for customers in customers:
            customers.create()
        phone_number = customers[0].phone_number
        count = len([customers for customers in customers if customers.phone_number == phone_number])
        found = customer.find_by_availability(phone_number)
        self.assertEqual(found.count(), count)
        for customers in found:
            self.assertEqual(customers.phone_number, phone_number)
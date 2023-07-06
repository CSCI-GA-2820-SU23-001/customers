"""
Test cases for Customer Model

"""
import os
import logging
import unittest
from service.models import Customer, db, DataValidationError
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

    def test_repr(self):
        """It should provide a string representation of a Customer"""
        customer = Customer(name="c1", id = 1, address = "address1", phone_number = "123456", email="c1@gmail.com", password = "c1")
        self.assertEqual(repr(customer), f"<Customer c1 id=[1]>")
        
        
        
    def test_deserialize_key_error(self):
        """It should raise a DataValidationError when a key is missing during deserialization"""
        data = {"name": "c1", "address": "address1", "phone_number": "123456", "email":"c1@gmail.com", "password": "c1"}
        customer = Customer()
        del data['name']  # remove a key to trigger KeyError
        try:
            customer.deserialize(data)
        except DataValidationError as e:
            self.assertEqual(str(e), "Invalid Customer: missing name")
        else:
            self.fail("KeyError not raised")

    def test_deserialize_type_error(self):
        """It should raise a DataValidationError when a bad type is provided during deserialization"""
        data = ["Not a dictionary"]  # not a dictionary
        customer = Customer()
        try:
            customer.deserialize(data)
        except DataValidationError as e:
            self.assertTrue("Invalid Customer: body of request contained bad or no data" in str(e))
        else:
            self.fail("TypeError not raised")




    def test_find_by_name(self):
        """It should find Customers by their name"""
        customers = [CustomerFactory(name="test name") for _ in range(3)]
        for customer in customers:
            customer.create()

        # make sure they got saved
        self.assertEqual(len(Customer.all()), 3)

        # find them by name
        same_name_customers = Customer.find_by_name("test name")
        
        self.assertEqual(len(same_name_customers), 3)
        for customer in same_name_customers:
            self.assertEqual(customer.name, "test name")






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
        """It should Create a Customer"""
        customer = Customer(name="c1", id = 1, address = "address1", phone_number = "123456", email="c1@gmail.com", password = "c1")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.name, "c1")
        self.assertEqual(customer.address, "address1")
        self.assertEqual(customer.phone_number, "123456")
        self.assertEqual(customer.email, "c1@gmail.com")
        self.assertEqual(customer.password, "c1")
    

    def test_read_a_customer(self):
        """It should Read a Customer"""
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

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.id)
        # Change it an save it
        customer.name = "customer2"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.name, "customer2")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].name, "customer2")


    def test_serialize_a_customer(self):
        """It should serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], customer.name)
        self.assertIn("phone_number", data)
        self.assertEqual(data["phone_number"], customer.phone_number)
        self.assertIn("password", data)
        self.assertEqual(data["password"], customer.password)
        self.assertIn("address", data)
        self.assertEqual(data["address"], customer.address)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)


    def test_deserialize_a_customer(self):
        """It should de-serialize a Customer"""
        data = CustomerFactory().serialize()
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, data["name"])
        self.assertEqual(customer.password, data["password"])
        self.assertEqual(customer.address, data["address"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.phone_number, data["phone_number"])

    
    
    def test_delete_customer(self):
        """It should delete a customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertIsNotNone(customer.id)
        customer = customer.find(customer.id)
        self.assertTrue(customer)
        customer.delete()
        customer = Customer.all()
        self.assertEqual(len(customer),0)




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
# Customer Model Test Cases
######################################################################
class TestCustomer(unittest.TestCase):
    """Test Cases for Customer Model"""

    def test_repr(self):
        """It should provide a string representation of a Customer"""
        customer = Customer(
            name="c1",
            id=1,
            address="address1",
            phone_number="123456",
            email="c1@gmail.com",
            password="c1",
            available=True,
        )
        self.assertEqual(repr(customer), "<Customer c1 id=[1]>")

    def test_deserialize_key_error(self):
        """It should raise a DataValidationError when a key is missing during deserialization"""
        data = {
            "name": "c1",
            "address": "address1",
            "phone_number": "123456",
            "email": "c1@gmail.com",
            "password": "c1",
            "available": "True",
        }
        customer = Customer()
        del data["name"]  # remove a key to trigger KeyError
        try:
            customer.deserialize(data)
        except DataValidationError as error:
            self.assertEqual(str(error), "Invalid Customer: missing name")
        else:
            self.fail("KeyError not raised")

    def test_deserialize_type_error(self):
        """It should raise a DataValidationError when a bad type is provided during deserialization"""
        data = ["Not a dictionary"]  # not a dictionary
        customer = Customer()
        try:
            customer.deserialize(data)
        except DataValidationError as error:
            self.assertTrue(
                "Invalid Customer: body of request contained bad or no data"
                in str(error)
            )
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

    def test_find_customer(self):
        """It should Find a Customer by ID"""
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(Customer.all()), 5)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.phone_number, customers[1].phone_number)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.email, customers[1].email)

    def test_find_by_phone_number(self):
        """It should Find Customer by Phone number"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        phone_number = customers[0].phone_number
        count = len([customer for customer in customers if customer.phone_number == phone_number])
        found = Customer.find_by_phone_number(phone_number)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.phone_number, phone_number)

    def test_find_by_address(self):
        """It should Find Customer by Address"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        address = customers[0].address
        count = len(
            [customer for customer in customers if customer.address == address])
        found = Customer.find_by_address(address)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.address, address)

    def test_find_by_email(self):
        """It should Find Customer by Email"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        email = customers[0].email
        count = len(
            [customer for customer in customers if customer.email == email])
        found = Customer.find_by_email(email)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.email, email)

    def test_find_or_404_found(self):
        """It should Find or return 404 not found for Customer"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()

        customer = Customer.find_or_404(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.phone_number, customers[1].phone_number)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.email, customers[1].email)
    
    def test_find_by_availability_false(self):
        """ Find Customers by availability -- False """
        available_customer = CustomerFactory(available=True)
        unavailable_customer = CustomerFactory(available=False)
        db.session.add(available_customer)
        db.session.add(unavailable_customer)
        db.session.commit()
        query = Customer.find_by_availability(False)
        customers = query.all()  # 将查询转换为列表
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, unavailable_customer.id)
        self.assertFalse(customers[0].available)

    # def test_find_by_availability_empty(self):
    #     """ Find Customers by availability - No Customers """
    #     customers = Customer.find_by_availability(True)
    #     self.assertEqual(len(customers), 0)

    def test_find_by_phone_existing(self):
        """ Find Customers with an existing phone number """
        customer_with_phone = CustomerFactory(phone_number="1234567890")
        customer_without_phone = CustomerFactory(phone_number="0987654321")
        db.session.add(customer_with_phone)
        db.session.add(customer_without_phone)
        db.session.commit()
        customers = Customer.find_by_phone("1234567890")
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, customer_with_phone.id)
        self.assertEqual(customers[0].phone_number, "1234567890")

    def test_find_by_phone_non_existing(self):
        """ Find Customers with a non-existing phone number """
        customer = CustomerFactory(phone_number="1234567890")
        db.session.add(customer)
        db.session.commit()
        customers = Customer.find_by_phone("0987654321")
        self.assertEqual(len(customers), 0)

    def test_find_by_phone_empty(self):
        """ Find Customers with phone number when no Customers in DB """
        customers = Customer.find_by_phone("1234567890")
        self.assertEqual(len(customers), 0)

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    # T E S T C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """It should Create a Customer"""
        customer = Customer(
            name="c1",
            id=1,
            address="address1",
            phone_number="123456",
            email="c1@gmail.com",
            password="c1",
            available=True,
        )
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.name, "c1")
        self.assertEqual(customer.address, "address1")
        self.assertEqual(customer.phone_number, "123456")
        self.assertEqual(customer.email, "c1@gmail.com")
        self.assertEqual(customer.password, "c1")
        self.assertEqual(customer.available, True)

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
        # Change it and save it
        customer.name = "customer2"
        original_customer_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_customer_id)
        self.assertEqual(customer.name, "customer2")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_customer_id)
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
        self.assertIn("available", data)
        self.assertEqual(data["available"], customer.available)

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
        self.assertEqual(customer.available, data["available"])

    def test_delete_customer(self):
        """It should delete a customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertIsNotNone(customer.id)
        customer = customer.find(customer.id)
        self.assertTrue(customer)
        customer.delete()
        customer = Customer.all()
        self.assertEqual(len(customer), 0)

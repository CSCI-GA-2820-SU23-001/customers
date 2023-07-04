"""
TestCustomer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Customer
from service.common import status  # HTTP Status Codes
from tests.factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/customers"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.client.post(BASE_URL, json=test_customer.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = response.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers


    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer(self):
        """It should Get a single customer"""
        # get the name of a customer
        test_customer = self._create_customers(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_customer.name)

    def test_get_customer_not_found(self):
        """It should not Get a customer thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_customers(self):
        """ Factory method to create customers in bulk """
        test_customer = self._create_customers(1)[0]
        response = self.client.post(f"{BASE_URL}",json=test_customer.serialize(),content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        customer_id = data["id"]

        test_customer.name = "new"
        response = self.client.put(f"{BASE_URL}/{customer_id}",json=test_customer.serialize(),content_type = "application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"],customer_id)
        self.assertEqual(data["name"],"new")
        self.assertEqual(data["address"],test_customer.address)
        self.assertEqual(data["email"],test_customer.email)
        self.assertEqual(data["phone_number"],test_customer.phone_number)
        self.assertEqual(data["password"],test_customer.password)

    def test_delete_customer(self):
        """It should delete a customer"""
        customer = self._create_customers(1)[0]
        resp = self.client.get(f'{BASE_URL}/{customer.id}')
        self.assertEqual(status.HTTP_200_OK,resp.status_code)

        data = resp.get_json()
        self.assertTrue(data)

        customer_id = data['id']
        resp = self.client.delete(f"{BASE_URL}/{customer_id}")
        self.assertEqual(status.HTTP_204_NO_CONTENT,resp.status_code)

        resp = self.client.get(f"{BASE_URL}/{customer_id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_found(self):
        """It should not delete a customer thats not found"""
        resp = self.client.delete(f"{BASE_URL}/-1")
        self.assertEqual(resp.status_code,status.HTTP_404_NOT_FOUND)

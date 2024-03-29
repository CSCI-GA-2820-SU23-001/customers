"""
TestCustomer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
# pylint: disable=cyclic-import
# pylint: disable=too-many-lines
import os
import logging
import json
from unittest import TestCase
from unittest.mock import patch
from service import app
from service.models import db, init_db, Customer
from service.common import status  # HTTP Status Codes
from tests.factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/api/customers"
FLAG = False

######################################################################
#  T E S T   C A S E S
######################################################################


class TestYourResourceServer(TestCase):
    # pylint: disable=too-many-public-methods
    """REST API SERVER Tests"""
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(Customer).delete()
        db.session.commit()
        self.app = app.test_client()
        self.app.testing = True
        self.phone_number = "123-456-7890"

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_customers(self, count):
        """Factory method to create customers in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.client.post(BASE_URL, json=test_customer.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test customer",
            )
            new_customer = response.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################
    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer_no_data(self):
        """It should not Create a Customer with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_get_customer(self):
    #     """It should Get a single customer"""
    #     # get the name of a customer
    #     test_customer = self._create_customers(1)[0]
    #     response = self.client.get(f"{BASE_URL}/{test_customer.id}")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     data = response.get_json()
    #     self.assertEqual(data["name"], test_customer.name)

    def test_get_customer_list(self):
        """It should Get a list of Customers"""

        customers = CustomerFactory.create_batch(5)

        for customer in customers:
            customer.create()

        cust_get_req = self.client.get(BASE_URL)

        # Assert that the customer list is populated
        self.assertEqual(
            cust_get_req.status_code,
            status.HTTP_200_OK,
            "Customer list is populated successfully",
        )
        data = cust_get_req.get_json()
        self.assertEqual(len(data), 5)

    # def test_get_customer_not_found(self):
    #     """It should not Get a customer thats not found"""
    #     response = self.client.get(f"{BASE_URL}/0")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     data = response.get_json()
    #     logging.debug("Response data = %s", data)
    #     self.assertIn("was not found", data["message"])

    def test_update_customers(self):
        """Factory method to create customers in bulk"""
        test_customer = self._create_customers(1)[0]
        response = self.client.post(
            f"{BASE_URL}",
            json=test_customer.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        customer_id = data["id"]

        test_customer.name = "new"
        response = self.client.put(
            f"{BASE_URL}/{customer_id}",
            json=test_customer.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"], customer_id)
        self.assertEqual(data["name"], "new")
        self.assertEqual(data["address"], test_customer.address)
        self.assertEqual(data["email"], test_customer.email)
        self.assertEqual(data["phone_number"], test_customer.phone_number)
        self.assertEqual(data["password"], test_customer.password)
        self.assertEqual(data["available"], test_customer.available)

    def test_delete_customer(self):
        """It should delete a customer"""
        customer = self._create_customers(1)[0]
        resp = self.client.get(f"{BASE_URL}/{customer.id}")
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        data = resp.get_json()
        self.assertTrue(data)

        customer_id = data["id"]
        resp = self.client.delete(f"{BASE_URL}/{customer_id}")
        self.assertEqual(status.HTTP_204_NO_CONTENT, resp.status_code)

        resp = self.client.get(f"{BASE_URL}/{customer_id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_delete_not_found(self):
    #     """It should not delete a customer thats not found"""
    #     resp = self.client.delete(f"{BASE_URL}/-1")
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_not_found(self):
        """It should not Update a customer that's not found"""
        test_customer = CustomerFactory()
        response = self.client.put(
            f"{BASE_URL}/0",
            json=test_customer.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_create_customer_no_content_type(self):
        """
        It should return 415 if 'Content-Type' is not specified
        in headers when creating customers
        """
        new_customer = CustomerFactory()
        response = self.client.post(BASE_URL, data=new_customer.serialize())
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data = response.get_json()
        self.assertIn("Content-Type must be application/json", data["message"])

    def test_update_customer_no_content_type(self):
        """It should return 415 if 'Content-Type' is not
        specified in headers when updating customers
        """
        # First create a new customer
        new_customer = self._create_customers(1)[0]
        # Update customer data
        new_customer.name = "Updated name"
        # Make a PUT request without setting 'Content-Type' in headers
        headers = {"Content-Type": None}  # Explicitly set to None
        response = self.client.put(
            f"{BASE_URL}/{new_customer.id}",
            data=new_customer.serialize(),
            headers=headers,
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data = response.get_json()
        self.assertIn("Content-Type must be application/json", data["message"])

    def test_method_not_supported(self):
        """It should assert a method that not allowed error"""
        customer = CustomerFactory.create()
        customer.name = "Valentina"
        response = self.client.patch(
            f"{BASE_URL}/{customer.id}", json=customer.serialize()
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_suspend_customer(self):
        """It should Suspend a Customer"""

        # create a customer
        test_customer = self._create_customers(1)[0]

        # suspend the customer
        response = self.client.put(f"{BASE_URL}/{test_customer.id}/suspend")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the customer
        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the customer is suspended
        customer = response.get_json()
        self.assertEqual(customer["available"], False)

    def test_activate_customer(self):
        """It should Activate a Customer"""

        # create a customer
        test_customer = self._create_customers(1)[0]

        # suspend the customer
        response = self.client.put(f"{BASE_URL}/{test_customer.id}/suspend")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the customer
        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the customer is suspended
        customer = response.get_json()
        self.assertEqual(customer["available"], False)

        # activate the customer
        response = self.client.put(f"{BASE_URL}/{test_customer.id}/activate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the customer
        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the customer is active
        customer = response.get_json()
        self.assertEqual(customer["available"], True)

    def test_suspend_customer_not_found(self):
        """It should not Suspend a Customer that does not exist"""

        # suspend the customer
        response = self.client.put(f"{BASE_URL}/0/suspend")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_activate_customer_not_found(self):
        """It should not Activate a Customer that does not exist"""

        # activate the customer
        response = self.client.put(f"{BASE_URL}/0/activate")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_customers_by_name(self):
        """ Get a list of Customers by name """
        customers = self._create_customers(5)
        target_name = customers[0].name
        resp = self.app.get("/api/customers", query_string={"name": target_name})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], target_name)

    def test_list_customers_by_availability(self):
        """ Get a list of Customers by availability """
        self._create_customers(5)
        resp = self.app.get("/api/customers", query_string={"available": "true"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertTrue(all(cust['available'] for cust in data))

    @patch.object(Customer, 'find_by_phone')
    def test_find_by_phone(self, mock_find_by_phone):
        """
        to test whether we can list customers by searching phone number.
        """
        mock_customers = [Customer(phone_number=self.phone_number)]
        mock_find_by_phone.return_value = mock_customers

        response = self.app.get(f'/api/customers?phone_number={self.phone_number}')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['phone_number'], self.phone_number)

    @patch.object(Customer, 'find')
    def test_get_customer_by_id(self, mock_find):
        """Get a Customer by its ID"""
        # Assume we have a customer with ID 123 in the database
        test_customer = Customer(id=123, name="Test Customer")
        mock_find.return_value = test_customer

        # Now use the test client to make the request
        resp = self.app.get("/api/customers", query_string={"id": 123})

        # Check the status code and the returned data
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 123)
        self.assertEqual(data[0]["name"], "Test Customer")
        mock_find.assert_called_once_with(123)

    def test_missing_content_type(self):
        """Test missing Content-Type in headers"""
        response = self.app.post('/api/customers', data=json.dumps({
            "name": "John",
            "address": "123 Main St",
            "email": "john@example.com",
            "password": "password",
            "phone_number": "123-456-7890",
            "available": True
        }))  # intentionally not setting the content-type header
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Content-Type must be application/json")

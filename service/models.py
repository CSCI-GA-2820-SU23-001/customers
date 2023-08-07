"""
Models for Customer
All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Customer.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Customer(db.Model):
    """
    Class that represents a Customer
    """
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(63), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(63))
    available = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"<Customer {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Customer to the database"""
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Customer to the database"""
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Customer from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Customer into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "email": self.email,
            "phone_number": self.phone_number,
            "password": self.password,
            "available": self.available,
        }

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.address = data["address"]
            self.email = data["email"]
            self.password = data["password"]
            self.phone_number = data.get("phone_number")
            self.available = data["available"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data - "
                "Error message: " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the Customers in the database"""
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Customer by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Customers with the given name

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def find_by_phone_number(cls, phone_number):
        """Returns all Customers with the given phone_number

        :param name: the phone_number of the Customers you want to match
        :type phone_number: str

        :return: a collection of Customers with that phone_number
        :rtype: list

        """
        logger.info("Processing phone_number query for %s ...", phone_number)
        return cls.query.filter(cls.phone_number == phone_number)

    @classmethod
    def find_by_address(cls, address):
        """Returns all Customers with the given address

        :param name: the address of the Customers you want to match
        :type address: str

        :return: a collection of Customers with that address
        :rtype: list

        """
        logger.info("Processing address query for %s ...", address)
        return cls.query.filter(cls.address == address)

    @classmethod
    def find_by_email(cls, email):
        """Returns the Customer with the given email

        Args:
            email (string): the email of the Customer you want to match
        """
        logger.info("Processing email query for %s ...", email)
        return cls.query.filter(cls.email == email)

    @classmethod
    def find_or_404(cls, customer_id: int):
        """Find a Customer by its id

        :param customer_id: the id of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id, or 404_NOT_FOUND if not found
        :rtype: Customer

        """
        logger.info("Processing lookup or 404 for id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)

    @classmethod
    def find_by_availability(cls, available: bool = True) -> list:
        """Return all Customers by their availability

        :param available: True for Customers that are available
        :type available: str

        :return: a collection of Customers that are available
        :rtype: list

        """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

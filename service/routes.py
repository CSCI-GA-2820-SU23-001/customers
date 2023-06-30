"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Customer

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...



# Create customers
# -----------------------------------------------------------
@app.route("/customers/<name>", methods=["POST"])
def create_customers(name):
    """Creates a new counter and stores it in the database

    Args:
        name (str): the name of the customers to create

    Returns:
        dict: the customers and it's value
    """
    app.logger.info(f"Request to Create customer {name}...")

    # See if the customer already exists and send an error if it does
    Customer = Customer.find(name)
    if Customer is not None:
        abort(status.HTTP_409_CONFLICT, f"Counter {name} already exists")

    # Create the new customer
    Customer = Customer(name)
    Customer.create()

    # Set the location header and return the new Customer
    location_url = url_for("read_customers", name=name, _external=True)
    return (
        jsonify(counter.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )
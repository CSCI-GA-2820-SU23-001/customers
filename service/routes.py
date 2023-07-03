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


@app.route("/customers", methods=["GET"])
def list_pets():
    """Returns all of the Customers"""
    app.logger.info("Request for Customer list")
    customers = []
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        customers = Customer.find_by_category(category)
    elif name:
        customers = Customer.find_by_name(name)
    else:
        customers = Customer.all()

    results = [Customer.serialize() for Customer in customers]
    app.logger.info("Returning %d customers", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE A Customer
######################################################################
@app.route("/pets/<int:customer_id>", methods=["GET"])
def get_pets(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for Customer with id: %s", customer_id)
    Customer = Customer.find(customer_id)
    if not Customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

    app.logger.info("Returning Customer: %s", Customer.name)
    return jsonify(Customer.serialize()), status.HTTP_200_OK
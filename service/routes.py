"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Customer

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )

    app.logger.info("Returning customer: %s", customer.name)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a customer
    This endpoint will create a customer based the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("create_customers", customer_id=customer.id, _external=True)

    app.logger.info("Customer with ID [%s] created.", customer.id)

    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# MODIFY A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")

    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )
    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.update()
    message = customer.serialize()
    app.logger.info("Customer with ID [%s] updated.", customer.id)
    return jsonify(message), status.HTTP_200_OK


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a customer
    This endpoint will delete a customer based the id in the path
    """
    customer = Customer()
    app.logger.info("Request to delete a customer with id: %s", customer_id)
    customer = customer.find(customer_id)
    if customer:
        customer.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# list a customer #
######################################################################


@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the Customers"""
    app.logger.info("Request for customer list")
    customers = []
    customer_id = request.args.get("customer_id")
    phone = request.args.get("phone_number")
    name = request.args.get("name")
    available = request.args.get("available")

    if customer_id:
        customers = Customer.find_by_id(customer_id)
    elif phone:
        customers = Customer.find_by_phone(phone)
    elif name:
        customers = Customer.find_by_name(name)
    elif available:
        customers = Customer.find_by_availability(available)
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    app.logger.info("Returning %d customers", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# SUSPEND A CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>/suspend", methods=["PUT"])
def suspend_customer(customer_id):
    """
    Suspend a Customer
    This endpoint will suspend a Customer based on the id specified in the path
    """
    app.logger.info("Request to suspend Customer with id: %s", customer_id)

    customer = Customer.find(customer_id)
    if not customer:
        # if no customer is found, return a 404
        app.logger.error("Customer with id %s does not exist", customer_id)
        abort(
            status.HTTP_404_NOT_FOUND, f"Customer with id {customer_id} does not exist"
        )

    customer.available = False
    customer.update()
    app.logger.error("Customer with id %s suspend complete.", customer_id)
    return (jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# ACTIVATE A CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>/activate", methods=["PUT"])
def activate_customer(customer_id):
    """
    Activate a Customer
    This endpoint will activate a Customer, setting suspended to false,
    based on the id specified in the path
    """
    app.logger.info("Request to activate Customer with id: %s", customer_id)

    customer = Customer.find(customer_id)
    if not customer:
        # if no customer is found, return a 404
        app.logger.error("Customer with id %s does not exist", customer_id)
        abort(
            status.HTTP_404_NOT_FOUND, f"Customer with id {customer_id} does not exist"
        )

    customer.available = True
    customer.update()
    app.logger.error("Customer with id %s activated complete.", customer_id)
    return (jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """
    Checks that the media type is correct
    """
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )

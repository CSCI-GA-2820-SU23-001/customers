"""
My Service

Describe what your service does here
"""

from flask import request, make_response, abort
from flask_restx import Resource, fields, reqparse, inputs
from service.common import status  # HTTP Status Codes
from service.models import Customer
from . import app, api

######################################################################
# Configure the Root route before OpenAPI
######################################################################


@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Customer",
    {
        "name": fields.String(
            required=True,
            description="The name of the Customer"
        ),
        "address": fields.String(
            required=True,
            description="The address of the Customer",
        ),
        "email": fields.String(
            required=True,
            description="The email of the Customer"
        ),
        "password": fields.String(
            required=True,
            description="The password of the Customer"
        ),
        "phone_number": fields.String(
            required=True,
            description="The phone_number of the Customer"
        ),
        "available": fields.Boolean(
            required=True,
            description="Active or not"
        ),
    },
)

customer_model = api.inherit(
    "CustomerModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True,
            description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument(
    "id",
    type=int,
    location="args",
    required=False,
    help="List Pets by id",
)
customer_args.add_argument(
    "phone_number",
    type=str,
    location="args",
    required=False,
    help="List Pets by phone_number"
)
customer_args.add_argument(
    "name",
    type=str,
    location="args",
    required=False,
    help="List Pets by name"
)
customer_args.add_argument(
    "available",
    type=inputs.boolean,
    location="args",
    required=False,
    help="List Pets by available",
)


######################################################################
#  PATH: /customers/{id}
######################################################################
@api.route("/customers/<int:customer_id>")
@api.param("customer_id", "The customer identifier")
class CustomerResource(Resource):
    """
    CustomerResource class

    Allows the manipulation of a single customer
    GET /customers{id} - Returns a customer with the id
    PUT /customers{id} - Modifies a customer with the id
    DELETE /customers{id} -  Deletes a customer with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("get_customers")
    @api.response(404, "Customer not found")
    @api.marshal_with(customer_model)
    def get(self, customer_id):
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
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # MODIFY A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("update_customers")
    @api.response(404, "Customer not found")
    @api.response(400, "The posted customer data was not valid")
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a customer
        This endpoint will update a customer based on it's id
        """
        app.logger.info("Request to update customer with id: %s", customer_id)
        check_content_type("application/json")

        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.update()
        app.logger.info("Customer with ID [%s] updated.", customer.id)
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("delete_customers")
    @api.response(204, "Customer deleted")
    def delete(self, customer_id):
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
#  PATH: /customers
######################################################################
@api.route("/customers", strict_slashes=False)
class CustomerCollection(Resource):
    """Handles all interactions with collections of Customers"""

    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------
    @api.doc("list_customers")
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """Returns all of the Customers"""
        app.logger.info("Request for customer list")
        customers = []
        args = customer_args.parse_args()
        if args["id"]:
            customer = Customer.find(args["id"])
            customers = [customer] if customer else []
        elif args["phone_number"]:
            customers = Customer.find_by_phone(args["phone_number"])
        elif args["name"]:
            customers = Customer.find_by_name(args["name"])
        elif args["available"]:
            customers = Customer.find_by_availability(args["available"])
        else:
            customers = Customer.all()

        results = [customer.serialize() for customer in customers]
        app.logger.info("Returning %d customers", len(results))
        return results, status.HTTP_200_OK
    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    # ------------------------------------------------------------------

    @api.doc("create_customers")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a customer
        This endpoint will create a customer based the data in the body that is posted
        """
        app.logger.info("Request to create a customer")
        check_content_type("application/json")
        customer = Customer()
        customer.deserialize(api.payload)
        customer.create()
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)
        app.logger.info("Customer with ID [%s] created.", customer.id)
        print("Customer with ID ", customer.id, " created.")
        return customer.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /customers/{id}/suspend
######################################################################
@api.route("/customers/<int:customer_id>/suspend")
@api.param("customer_id", "Suspend customer")
class SuspendResource(Resource):
    """Suspend actions on a customer"""

    @api.doc("suspend_customer")
    @api.response(404, "Customer not found")
    @api.response(409, "The customer is not available for suspend")
    def put(self, customer_id):
        """
        Suspend a customer
        This endpoint will suspend a customer based on the id specified in the path
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
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /customers/{id}/activate
######################################################################
@api.route("/customers/<int:customer_id>/activate")
@api.param("customer_id", "Activate customer")
class ActivateResource(Resource):
    """Activate actions on a customer"""

    @api.doc("activate_customer")
    @api.response(404, "Customer not found")
    @api.response(409, "The customer is not available for activate")
    def put(self, customer_id):
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
        return customer.serialize(), status.HTTP_200_OK


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

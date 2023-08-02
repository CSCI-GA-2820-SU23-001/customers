$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_name").val(res.name);
        $("#customer_address").val(res.address);
        $("#customer_email").val(res.email);
        $("#customer_password").val(res.password);
        $("#customer_phone_number").val(res.phone_number);
        if (res.available == true) {
            $("#customer_available").val("true");
        } else {
            $("#customer_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#customer_name").val("");
        $("#customer_address").val("");
        $("#customer_email").val("");
        $("#customer_password").val("");
        $("#customer_phone_number").val("");
        $("#customer_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#customer_name").val();
        let address = $("#customer_address").val();
        let email = $("#customer_email").val();
        let password = $("#customer_password").val();
        let phone_number = $("#customer_phone_number").val();
        let available = $("#customer_available").val() == "true";

        let data = {
            "name": name,
            "address":address,
            "email":email,
            "password":password,
            "phone_number":phone_number,
            "available":available
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let name = $("#customer_name").val();
        let address = $("#customer_address").val();
        let phone_number = $("#customer_phone_number").val();
        let available = $("#customer_available").val() == "true";
        let email = $("#customer_email").val();
        let password = $("#customer_password").val();
       

        let data = {
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "available":available,
            "email": email,
            "password": password
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#customer_name").val();
        let address = $("#customer_address").val();
        let password = $("#customer_password").val();
        let available = $("#available").val() == "true";

        $("#flash_message").empty();
        if (name || address || password || available) {
            flash_message("Only support id, email, phone_number query");
            return;
        }

        let customer_id = $("#customer_id").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let queryString = ""


        if (customer_id) {
            queryString += 'id=' + customer_id
        }
        if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email
            } else {
                queryString += 'email=' + email
            }
        }
        if (phone_number) {
            if (queryString.length > 0) {
                queryString += '&phone_number=' + phone_number
            } else {
                queryString += 'phone_number=' + phone_number
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Address</th>'
            table += '<th class="col-md-2">Password</th>'
            table += '<th class="col-md-2">Phone_Number</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let pet = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.id}</td><td>${customer.name}</td><td>${customer.email}</td><td>${customer.address}</td><td>${customer.password}</td><td>${customer.phone_number}</td><td>${customer.available}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})

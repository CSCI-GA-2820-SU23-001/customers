$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#id").val(res.id);
        $("#name").val(res.name);
        $("#address").val(res.address);
        $("#email").val(res.email);
        $("#password").val(res.password);
        $("#phone_number").val(res.phone_number);
        if (res.available == true) {
            $("#available").val("true");
        } else {
            $("#available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#id").val("");
        $("#name").val("");
        $("#address").val("");
        $("#email").val("");
        $("#password").val("");
        $("#phone_number").val("");
        $("#available").val("");
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

        let name = $("#name").val();
        let address = $("#address").val();
        let email = $("#email").val();
        let password = $("#password").val();
        let phone_number = $("#phone_number").val();
        let available = $("#available").val()=="true";

        let data = {
            "name": name,
            "address": address,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "available": available
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            clear_form_data()
            // update_form_data(res)
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

        let id = $("#id").val();
        let name = $("#name").val();
        let address = $("#address").val();
        let email = $("#email").val();
        let password = $("#password").val();
        let phone_number = $("#phone_number").val();
        let available = $("#available").val()=="true";
        
        let data = {
            "name": name,
            "address": address,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "available": available
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/customers/${id}`,
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

        let id = $("#id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/customers/${id}`,
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

        let id = $("#id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/customers/${id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {
        // let id = $("#id").val();
        let name = $("#name").val();
        let address = $("#address").val();
        let email = $("#email").val();
        let phone_number = $("#phone_number").val();
        let available = $("#available").val();

        let queryString = ""
        // if (id) {
        //     queryString += 'id=' + id
        // }
        if (name) {
            if (queryString.length > 0) {
                queryString += '&name=' + name
            } else {
                queryString += 'name=' + name
            }
        }
        if (address) {
            if (queryString.length > 0) {
                queryString += '&address=' + address
            } else {
                queryString += 'address=' + address
            }
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
            url: `/api/customers?${queryString}`,
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
            table += '<th class="col-md-2">address</th>'
            table += '<th class="col-md-2">email</th>'
            table += '<th class="col-md-2">password</th>'
            table += '<th class="col-md-2">phone</th>'
            table += '<th class="col-md-2">available</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.id}</td><td>${customer.name}</td><td>${customer.address}</td><td>${customer.email}</td><td>${customer.password}</td><td>${customer.phone_number}</td><td>${customer.available}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                // update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})

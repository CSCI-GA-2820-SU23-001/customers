Feature: The customer service back-end
    As an app manager
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | name       | address   | email             | password  | phone      | available |
        | fido       | address1  | abc@gmail.com     | 123456    | 1112223456 | True |
        | kitty      | address2  | bcd@gmail.com     | abcdef    | 1234567890 | False |
        | leo        | address3  | cde@gmail.com     | qwerty    | 0987654321 | False |
        | sammy      | address4  | def@gmail.com     | asdfgh    | 111111111  | True |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Address" to "one 5th ave."
    And I set the "Email" to "aa1111@nyu.edu"
    And I set the "Password" to "NYU"
    And I set the "Phone Number" to "9998887777"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Address" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Phone Number" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Happy" in the "Name" field
    And I should see "one 5th ave." in the "Address" field
    And I should see "NYU" in the "Password" field
    And I should see "9998887777" in the "Phone Number" field
    And I should see "aa1111@nyu.edu" in the "Email" field

Scenario: List all pets
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the results
    And I should not see "kitty" in the results
    And I should not see "leo" in the results
    And I should see "sammy" in the results

Scenario: Search by phone numbers
    When I visit the "Home Page"
    And I set the "Phone Number" to "111111111"
    And I press the "Search" button
    Then I should see the message "Success"
    # And I should not see "kitty" in the results
    # And I should not see "leo" in the results
    # And I should not see "fido" in the results
    And I should see "sammy" in the results

Scenario: Search for available
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the results
    And I should not see "kitty" in the results
    And I should see "sammy" in the results
    And I should not see "leo" in the results

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "Name" to "fido"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the "Name" field
    And I should see "address1" in the "Address" field
    When I change "Name" to "Loki"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Loki" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Loki" in the results
    And I should not see "fido" in the results

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "Name" to "fido"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the "Name" field
    And I should see "address1" in the "Address" field
    When I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "kitty" in the results
    And I should not see "fido" in the results
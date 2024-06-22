import { fetchCurrentDonorName, logout } from './app_utils.js';

$(document).ready(function() {
    const table = $('#contacts_table').DataTable({
        columnDefs: [
            {
                targets: 4, // Assuming the date_donated column is at index 4 (zero-based index)
                render: function(data, type, row) {
                    if (type === 'display' && data) {
                        const date = new Date(data);
                        const year = date.getFullYear();
                        const month = String(date.getMonth() + 1).padStart(2, '0');
                        const day = String(date.getDate()).padStart(2, '0');
                        return `${year}/${month}/${day}`;
                    }
                    return data;
                }
            }
        ]
    });


    // Fetch data from API and update table
    fetchDataAndUpdateTable(table);

    fetchCurrentDonorName();

    // Handle add row button click
    $('#addRowBtn').click(function() {
        $('#addRowModal').modal('show');
    });

    // Handle form submission for adding row
    $('#addContactForm').submit(function(event) {
        event.preventDefault();
        addContact(table);
    });

    // Handle edit button click
    $('#contacts_table tbody').on('click', 'button.edit-btn', function() {
        const rowData = table.row($(this).parents('tr')).data();
        const contactId = rowData[0]; // Assuming ID is in the first column
        openEditModal(rowData);
        // Handle form submission for editing row
        $('#editContactForm').off().submit(function(event) {
            event.preventDefault();
            updateContact(table, contactId);
        });
    });

    // Handle delete button click
    $('#contacts_table tbody').on('click', 'button.delete-btn', function() {
        const rowData = table.row($(this).parents('tr')).data();
        const contactId = rowData[0]; // Assuming ID is in the first column
        openDeleteConfirmationModal(contactId, table);
    });

    $('#logoutBtn').click(function() {
        logout();
      });

});

// Fetch data from API and update DataTable
function fetchDataAndUpdateTable(table) {

    const token = localStorage.getItem('accessToken');

    $.ajax({
        url: 'http://127.0.0.1:8000/contacts/user',
        method: 'GET',
        dataType: 'json',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        success: function(response) {
            if (Array.isArray(response)) {
                response.forEach(function(item) {
                    table.row.add([
                        item.id,
                        item.contact_name,
                        item.email,
                        item.phone_num,
                        item.date_created,
                        '<button class="btn btn-primary edit-btn" style="font-size: 14px; padding: 3px 5px; margin: 1px;">Edit</button> ' +
                        '<button class="btn btn-danger delete-btn" style="font-size: 14px; padding: 3px 5px; margin: 1px;">Delete</button>'
                    ]).draw(false);
                });
            } else {
                console.error('Invalid data format in API response');
            }
        },
        error: function(xhr, status, error) {
            if(xhr.status === 401){
                console.error('Token has expired');
                redirectToLoginPage();
            }else{
                console.error('Error fetching data:', error);
            }
            
        }
    });
}


function redirectToLoginPage() {
    // Remove the access token from localStorage
    localStorage.removeItem('accessToken');
  
    // Redirect to the login page
    window.location.href = 'http://localhost:63342/foodshareAPI/frontend/webapp/login_register_form.html';
}


// Add a new row to the DataTable
async function addContact(table) {
    const contact_name = $('#name').val();
    const email = $('#email').val();
    const phone_num = $('#phone_number').val();
    // const donor_id = $('#donorID').val();

    // Retrieve the JWT token from localStorage
    const token = localStorage.getItem('accessToken');

    const response = await fetch('http://127.0.0.1:8000/contacts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        },
        body: JSON.stringify({
            contact_name,
            email,
            phone_num,
            // donor_id
        })
    });

    if (!response.ok) {
        throw new Error(`Error adding donation: ${await response.text()}`);
    }

    const data = await response.json();

    // Reset form and hide modal
    $('#addContactForm').trigger('reset');
    $('#addRowModal').modal('hide');

    // Display success message
    alert('Contact added successfully!');

    return data;
}

// Open the edit modal and populate with current row data
function openEditModal(rowData) {
    $('#editName').val(rowData[1]);
    $('#editEmail').val(rowData[2]);
    $('#editPhoneNumber').val(rowData[3]);
    $('#editDonorID').val(rowData[4]);
    $('#editRowModal').modal('show');
}

// Update the row in the DataTable
function updateContact(table, contactId) {
    const newName = $('#editName').val();
    const newEmail = $('#editEmail').val();
    const newPhonenum = $('#editPhoneNumber').val();
    // const newDonorID = $('#editDonorID').val();

    // Retrieve the JWT token from localStorage
    const token = localStorage.getItem('accessToken');

    $.ajax({
         url: 'http://127.0.0.1:8000/contacts/' + contactId + '/',
        method: 'PUT',
        contentType: 'application/json',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        data: JSON.stringify({
            contact_name: newName,
            email: newEmail,
            phone_num: newPhonenum,
            // donor_id: newDonorID
        }),
        success: function(response) {
            $('#editRowModal').modal('hide');
            alert('Row updated successfully!');
            $('#editRowForm').trigger('reset');
            table.ajax.reload(); // Reload the table data
        },
        error: function(xhr, status, error) {
            if(xhr.status === 401){
                // Handle unauthorized access
                alert('Your session has expired. Please log in again.');
                redirectToLoginPage();
            }else{
                console.error('Error updating row:', error);
                alert('Error updating row. Please try again.');
            }
        }
    });
}

// Open the delete confirmation modal
function openDeleteConfirmationModal(contactId, table) {
    $('#deleteConfirmationModal').modal('show');
    $('#deleteConfirmed').off().click(function() {

        // Retrieve the JWT token from localStorage
        const token = localStorage.getItem('accessToken');

        $.ajax({
            url: `http://127.0.0.1:8000/contacts/${contactId}/`,
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
                table.row($(`tr[data-id="${contactId}"]`)).remove().draw();
                $('#deleteConfirmationModal').modal('hide');
                alert('Row deleted successfully!');
            },
            error: function(xhr, status, error) {
                if(xhr.status === 401){
                    // Handle unauthorized access
                    alert('Your session has expired. Please log in again.');
                    redirectToLoginPage();
                }else{
                    console.error('Error deleting row:', error);
                    alert('Error deleting row. Please try again.');
                }
                
            }
        });
    });
}

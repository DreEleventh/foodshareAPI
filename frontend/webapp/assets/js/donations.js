import { fetchCurrentDonorName, logout } from './app_utils.js';

$(document).ready(function() {
    const table = $('#donations_table').DataTable({
        columnDefs: [
            {"aaSorting": [[0, "desc"]]},
            {'class': "compact"},
            // {"scrollX": true},
            { width: '15%', targets: 1 },
            { width: '18%', targets: 6 },
            { width: '25%', targets: 3 }, // Set width of the Actions column to 20%
            {
                targets: 5, // Assuming the date_donated column is at index 4 (zero-based index)
                render: function(data, type, row) {
                    // Parse the date string and format it as yyyy/mm/dd
                    if (type === 'display' && data) {
                        var date = new Date(data);
                        var year = date.getFullYear();
                        var month = ('0' + (date.getMonth() + 1)).slice(-2); // Adding leading zero if needed
                        var day = ('0' + date.getDate()).slice(-2); // Adding leading zero if needed
                        return year + '/' + month + '/' + day;
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
    $('#addRowForm').submit(function(event) {
        event.preventDefault();
        addDonation(table);
    });

    // Handle edit button click
    $('#donations_table tbody').on('click', 'button.edit-btn', function() {
        const rowData = table.row($(this).parents('tr')).data();
        const donationId = rowData[0]; // Assuming ID is in the first column
        openEditModal(rowData);
        // Handle form submission for editing row
        $('#editRowForm').off().submit(function(event) {
            event.preventDefault();
            updateDonation(table, donationId);
        });
    });

    // Handle delete button click
    $('#donations_table tbody').on('click', 'button.delete-btn', function() {
        const rowData = table.row($(this).parents('tr')).data();
        const donationId = rowData[0]; // Assuming ID is in the first column
        openDeleteConfirmationModal(donationId, table);
    });


    $('#logoutBtn').click(function() {
        logout();
      });
});

// Fetch data from API and update DataTable
function fetchDataAndUpdateTable(table) {
    const token = localStorage.getItem('accessToken');

    $.ajax({
        url: 'http://127.0.0.1:8000/donations/user',
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
                        item.donation_name,
                        item.quantity,
                        item.description,
                        item.donation_status,
                        item.date_donated,
                        '<button class="btn btn-primary edit-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Edit</button> ' +
                        '<button class="btn btn-danger delete-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Delete</button>' +
                        '<button class="btn btn-secondary post-btn" style="font-size: 16px; padding: 3px 5px; margin: 2px;">Post</button>'  
                    ]).draw(false);
                });
                } else {
                    console.error('Invalid data format in API response');
                }

            },
            error: function(xhr, status, error) {
                if (xhr.status === 401){
                    // Token has expired, handle token renewal or redirect to login
                    console.error('Token has expired');
                    redirectToLoginPage();
                }else{
                    console.error('Error fetching data', error);
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
async function addDonation(table) {
    // Extract data from form using destructuring assignment (assuming form ID is 'addRowForm')
    const donation_name = $('#name').val();
    const quantity = $('#quantity').val();
    const description = $('#description').val();

    // Retrieve the JWT token from localStorage
    const token = localStorage.getItem('accessToken');


    const response = await fetch('http://127.0.0.1:8000/donations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        },
        body: JSON.stringify({
            donation_name,
            quantity,
            description,
            // Add other fields as needed
        })
    });

    if (!response.ok) {
        throw new Error(`Error adding donation: ${await response.text()}`);
    }

    const data = await response.json();

    // Reset form and hide modal
    $('#addRowForm').trigger('reset');
    $('#addRowModal').modal('hide');

    // Display success message
    alert('Donation added successfully!'); // You can replace this with a more informative message


    return data; // You can return the response data if needed
}



// Open the edit modal and populate with current row data
function openEditModal(rowData) {
    $('#editName').val(rowData[1]);
    $('#editQuantity').val(rowData[2]);
    $('#editDescription').val(rowData[3]);
    $('#editStatus').val(rowData[4]);
    $('#editRowModal').modal('show');
}

// Update the row in the DataTable
function updateDonation(table, donationId) {
    const newName = $('#editName').val();
    const newQuantity = $('#editQuantity').val();
    const newDescription = $('#editDescription').val();

    // Retrieve the JWT token from localStorage
    const token = localStorage.getItem('accessToken');

    $.ajax({
        url: 'http://127.0.0.1:8000/donations/' + donationId + '/',
        method: 'PUT',
        contentType: 'application/json',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        data: JSON.stringify({
            donation_name: newName,
            quantity: newQuantity,
            description: newDescription
            // Add other fields as needed
        }),
        success: function(response) {
            $('#editRowModal').modal('hide');
            alert('Row updated successfully!');
            $('#editRowForm').trigger('reset');
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
function openDeleteConfirmationModal(donationId, table) {
    $('#deleteConfirmationModal').modal('show');
    $('#deleteConfirmed').off().click(function() {
        // const row = $(this).closest('tr'); // Use closest('tr') to target the row
        // const donationId = row.data()[0]; // Assuming ID is in the first column
        
        // Retrieve the JWT token from localStorage
        const token = localStorage.getItem('accessToken');

        $.ajax({
            url: 'http://127.0.0.1:8000/donations/' + donationId + '/',
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
                table.row($(this).parents('tr')).remove().draw();
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


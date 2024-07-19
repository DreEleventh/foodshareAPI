import { fetchCurrentRecipientName, logout } from './app_utils.js';

$(document).ready(function() {
    const table = $('#donation_pickup_table').DataTable({
        columnDefs: [ // Set width of the Actions column to 20%
            {'class': "compact"},
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

    fetchCurrentRecipientName();

    // Handle edit button click
    

    $('#logoutBtn').click(function() {
        logout();
      });

      // Event delegation for dynamically created buttons
    $('#donation_pickup_table tbody').on('click', '.view-btn', function() {
        let data = table.row($(this).parents('tr')).data();
        showDonationDetails(data);
    });


    $('#pickUpDonationBtn').click(function() {
        let donationId = $('#donationId').text();
        pickUpDonation(donationId);
    });

});

// Fetch data from API and update DataTable
function fetchDataAndUpdateTable(table) {
    // const token = localStorage.getItem('accessToken');

    $.ajax({
        url: 'http://127.0.0.1:8000/donations/all/posted',
        method: 'GET',
        dataType: 'json',

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
                        '<button class="btn btn-secondary view-btn" style="font-size: 16px; padding: 3px 5px; margin: 2px;">View</button>'
                        // '<button class="btn btn-primary pickup-btn" style="font-size: 16px; padding: 3px 5px; margin: 2px;">Pick Up</button>'
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

function showDonationDetails(data) {
    $('#donationId').text(data[0]);
    $('#donationName').text(data[1]);
    $('#donationQuantity').text(data[2]);
    $('#donationDescription').text(data[3]);
    $('#donationStatus').text(data[4]);
    $('#donationDate').text(data[5]);
    $('#donationModal').modal('show');
}


function pickUpDonation(donationId) {
    alert('Picking up donation with ID: ' + donationId);
    $.ajax({
        url: 'http://127.0.0.1:8000/donations/pickup/' + donationId + '/',
        method: 'PUT',
        contentType: 'application/json',
        success: function(response) {
            alert('Donation picked up successfully!');
            $('#donationModal').modal('hide');
            
            // Update the status in the DataTable
            var table = $('#donation_pickup_table').DataTable();
            var row = table.row(function(idx, data, node) {
                return data[0] == donationId; // Assuming the donation ID is in the first column
            });
            var data = row.data();
            data[4] = 'Picked'; // Assuming the status column is at index 4
            row.data(data).draw();
        },
        error: function(xhr, status, error) {
            alert('Error picking up donation: ' + xhr.responseText);
        }
    });
}


function redirectToLoginPage() {
    // Remove the access token from localStorage
    localStorage.removeItem('accessToken');

    // Redirect to the login page
    window.location.href = 'http://localhost:63342/foodshareAPI/frontend/webapp/donor_login_register_form.html';
}









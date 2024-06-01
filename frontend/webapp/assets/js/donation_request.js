$(document).ready(function() {
    const table = $('#request_table').DataTable({
        columnDefs: [
//            {"aaSorting": [[0, "desc"]]},
//            {'class': "compact"},
//            // {"scrollX": true},
//            { width: '15%', targets: 1 },
//            { width: '15%', targets: 6 },
//            { width: '25%', targets: 3 }, // Set width of the Actions column to 20%
            {
                targets: 4, // Assuming the date_donated column is at index 4 (zero-based index)
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
    $('#request_table tbody').on('click', 'button.edit-btn', function() {
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
    $('#request_table tbody').on('click', 'button.delete-btn', function() {
        const rowData = table.row($(this).parents('tr')).data();
        const donationId = rowData[0]; // Assuming ID is in the first column
        openDeleteConfirmationModal(donationId, table);
    });
});

// Fetch data from API and update DataTable
function fetchDataAndUpdateTable(table) {
    $.ajax({
        url: 'http://127.0.0.1:8000/donation_request',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            if (Array.isArray(response)) {
                response.forEach(function(item) {
                    table.row.add([
                        item.id,
                        item.recipient_id,
                        item.item_name,
                        item.quantity,
                        item.request_date,
                        '<button class="btn btn-primary edit-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Edit</button> ' +
                        '<button class="btn btn-danger delete-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Delete</button>'
                    ]).draw(false);
                });
                } else {
                    console.error('Invalid data format in API response');
                }

            },
            error: function(xhr, status, error) {
                console.error('Error fetching data:', error);
            }
        });
}

// Add a new row to the DataTable
async function addDonation(table) {
    // Extract data from form using destructuring assignment (assuming form ID is 'addRowForm')
    const recipient_id = $('#recipient_id').val();
    const item_name = $('#item_name').val();
    const quantity = $('#quantity').val();

    const response = await fetch('http://127.0.0.1:8000/donation_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            recipient_id,
            item_name,
            quantity,
//            description,
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

    // Add the new row to the table
    table.row.add([
        data.id,
        data.recipient_id,
        data.item_name,
        data.quantity,
        data.request_date,
        '<button class="btn btn-primary edit-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Edit</button> ' +
        '<button class="btn btn-danger delete-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Delete</button>'
    ]).draw();

    return data; // You can return the response data if needed
}



// Open the edit modal and populate with current row data
function openEditModal(rowData) {
    $('#editRecipient').val(rowData[1]);
    $('#editName').val(rowData[2]);
    $('#editQuantity').val(rowData[3]);
    $('#editRowModal').modal('show');
}

// Update the row in the DataTable
function updateDonation(table, itemId) {
    const newRecipientId = $('#editRecipient').val();
    const newName = $('#editName').val();
    const newQuantity = $('#editQuantity').val();

    $.ajax({
        url: 'http://127.0.0.1:8000/donation_request/' + itemId + '/',
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({
            recipient_id: newRecipientId,
            item_name: newName,
            quantity: newQuantity,
             // description: newDescription
            // Add other fields as needed
        }),
        success: function(response) {
            $('#editRowModal').modal('hide');
            alert('Row updated successfully!');
            $('#editRowForm').trigger('reset');

            // Update the row in the table
            const row = table.row($(this).closest('tr'));
            row.data([
                response.id,
                response.recipient_id,
                response.item_name,
                response.quantity,
                response.request_date,
                '<button class="btn btn-primary edit-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Edit</button> ' +
                '<button class="btn btn-danger delete-btn" style="font-size: 16px; padding: 3px 5px; margin: 1px;">Delete</button>'
            ]).draw();

        },
        error: function(xhr, status, error) {
            console.error('Error updating row:', error);
            alert('Error updating row. Please try again.');
        }

    });

}

// Open the delete confirmation modal
function openDeleteConfirmationModal(itemId, table) {
    $('#deleteConfirmationModal').modal('show');
    $('#deleteConfirmed').off().click(function() {
        // const row = $(this).closest('tr'); // Use closest('tr') to target the row
        // const donationId = row.data()[0]; // Assuming ID is in the first column
        $.ajax({
            url: 'http://127.0.0.1:8000/donation_request/' + itemId + '/',
            method: 'DELETE',
            success: function(response) {
                table.row($(this).parents('tr')).remove().draw();
                $('#deleteConfirmationModal').modal('hide');
                alert('Row deleted successfully!');
            },
            error: function(xhr, status, error) {
                console.error('Error deleting row:', error);
                alert('Error deleting row. Please try again.');
            }
        });
    });
}

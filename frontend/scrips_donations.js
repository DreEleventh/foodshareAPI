document.addEventListener('DOMContentLoaded', function() {
    // Code inside this function will run after the DOM is fully loaded

    function handleDonationFormSubmit(event) {
        event.preventDefault();
        const form = document.getElementById('donationForm');
        if (!form) {
            console.error('Error: donationForm element not found.');
            return;
        }
        const formData = new FormData(form);

        fetch('http://localhost:8000/donations/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData.entries()))
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Donation made successfully!');
            // Redirect or update UI as needed
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error making donation. Please try again.');
        });
    }

    function handleDonorRegistrationFormSubmit(event) {
        event.preventDefault();
        const form = document.getElementById('donorForm');
        if (!form) {
            console.error('Error: donorForm element not found.');
            return;
        }
        const formData = new FormData(form);

        fetch('http://localhost:8000/donors', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData.entries()))
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Donor registered successfully!');
            // Redirect or update UI as needed
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error registering donor. Please try again.');
        });
    }

    // Call the populateTable function to load data on page load
    // app.js - jQuery AJAX and DataTable function

    $(document).ready(function() {
      const table = $('#donations_table').DataTable();

      fetchDataAndUpdateTable(table);
    });

    function fetchDataAndUpdateTable(table) {
      $.ajax({
        url: 'http://127.0.0.1:8000/donations/',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
          if (response && response.donations && Array.isArray(response.donations)) {
            response.donations.forEach(function(item) {
              table.row.add([
                item.id,
                item.donation_name,
                item.description,
                item.donation_status,
                item.date_donated,
                item.quantity
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

    // Attach event listeners after the DOM is loaded
    // const donationTable = document.getElementById('donationsTable')
    const donationForm = document.getElementById('donationForm');
    const donorRegistrationForm = document.getElementById('donorForm');

    if (donationForm) {
        donationForm.addEventListener('submit', handleDonationFormSubmit);
    } else {
        console.error('Error: donationForm element not found.');
    }

    if (donorRegistrationForm) {
        donorRegistrationForm.addEventListener('submit', handleDonorRegistrationFormSubmit);
    } else {
        console.error('Error: donorForm element not found.');
    }
});

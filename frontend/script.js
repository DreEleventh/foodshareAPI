function fetchDropdownData() {
    return fetch('http://127.0.0.1:8000/donor_type')
        .then(response => response.json());
}

function populateDropdown() {
    fetchDropdownData()
        .then(data => {
            const dropdown = document.getElementById('type_dropdown');
            dropdown.innerHTML = ''; // Clear the dropdown
            data.forEach(value => {
                const option = document.createElement('option');
                option.textContent = value;
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching dropdown data:', error));
}

function handleFormSubmission(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(this); // Get form data
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Send form data to API endpoint
    fetch('http://127.0.0.1:8000/donors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            console.log('Form submitted successfully');
            populateDropdown();
            populateTable();
        } else {
            throw new Error('Failed to submit form');
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        // Optionally, display an error message to the user
    });
}

document.getElementById('donor-registration-form').addEventListener('submit', handleFormSubmission);
export function fetchCurrentDonorName() {
    const token = localStorage.getItem('accessToken');
  
    $.ajax({
      url: 'http://127.0.0.1:8000/donors/current_user/',
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      success: function(response) {
        const donorName = response.donor_name;
        $('#donor_name').text(donorName);
      },
      error: function(xhr, status, error) {
        if (xhr.status === 401) {
          // Handle unauthorized access
          alert('Your session has expired. Please log in again.');
          // Optionally, you can redirect to the login page
          // window.location.href = 'login.html';
        } else {
          console.error('Error fetching donor name:', error);
        }
      }
    });
  }



export function logout() {
    // Remove the access token from localStorage
    localStorage.removeItem('accessToken');
  
    // Redirect to the login page
    window.location.href = 'http://localhost:63342/foodshareAPI/frontend/webapp/login_register_form.html';
}
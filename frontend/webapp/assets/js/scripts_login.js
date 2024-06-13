const container = document.querySelector(".container"),
      pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password"),
      signUp = document.querySelector(".signup-link"),
      login = document.querySelector(".login-link");

    //   js code to show/hide password and change icon
    pwShowHide.forEach(eyeIcon =>{
        eyeIcon.addEventListener("click", ()=>{
            pwFields.forEach(pwField =>{
                if(pwField.type ==="password"){
                    pwField.type = "text";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye-slash", "uil-eye");
                    })
                }else{
                    pwField.type = "password";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye", "uil-eye-slash");
                    })
                }
            }) 
        })
    })

    // js code to appear signup and login form
    signUp.addEventListener("click", ( )=>{
        container.classList.add("active");
    });
    login.addEventListener("click", ( )=>{
        container.classList.remove("active");
    });

// Register a donor
 $(document).ready(function () {
    $('#donor_registration').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = {
            donor_name: $('#name').val(),
            email: $('#email').val(),
            phone_number: $('#phone_number').val(),
            address: $('#address').val(),
            password: $('#password').val()
        };

        // Send data to register donor endpoint
        $.ajax({
            type: 'POST',
            url: 'http://localhost:8000/donors',
            contentType: 'application/json',
            data: JSON.stringify({
                donor_name: formData.donor_name,
                email: formData.email,
                phone_number: formData.phone_number,
                address: formData.address
            }),
            success: function (donorResponse) {
                console.log('Donor registration successful:', donorResponse);

                // Once donor is registered, use the returned donor ID to create credentials
                var donorId = donorResponse.id;

                // Once donor is registered, use the email as username to create credentials
                var username = formData.email;

                // Send data to create credentials endpoint
                $.ajax({
                    type: 'POST',
                    url: 'http://127.0.0.1:8000/donor_credentials/',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        username: username,
                        password: formData.password,
                        donor_id: donorId // Use the donorId obtained from the donor registration response
                    }),
                    success: function (credentialsResponse) {
                        console.log('Credentials creation successful:', credentialsResponse);
                    },
                    error: function (error) {
                        console.error('Error creating credentials:', error.responseJSON.detail);
                    }
                });
            },
            error: function (error) {
                if (error.responseJSON) {
                    console.error('Error:', error.responseJSON.detail);
                } else {
                    console.error('Error:', error.statusText);
                }
            }
        });
    });
});

// Login a donor
// Get the form element
const loginForm = document.getElementById('login_form');

// Add an event listener for form submission
loginForm.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent the default form submission behavior

  // Get the form data
  const formData = new FormData(loginForm);
  const username = formData.get('username');
  const password = formData.get('password');

  try {
    // Send a POST request to the /donor_login endpoint
    const response = await fetch('http://127.0.0.1:8000/donor_login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    // Check if the response was successful
    if (response.ok) {
      // Parse the response data as JSON
      const data = await response.json();

      // Handle the response data (e.g., store the token, redirect to another page)
      const token = data.access_token;
      console.log('Access Token:', token);
      // You can store the token in localStorage or a cookie for future use
      localStorage.setItem('accessToken', token);

      // Optionally, you can redirect the user to another page after successful login
      window.location.href = 'http://localhost:63342/foodshareAPI/frontend/webapp/donor_dashboard.html?_ijt=b7qq01i25jpe0cpofco4elmfbg&_ij_reload=RELOAD_ON_SAVE';
    } else {
      // Handle the error response
      const errorData = await response.json();
      console.error('Login error:', errorData.detail);
      // Display an error message to the user
      alert(errorData.detail);
    }
  } catch (error) {
    console.error('Error occurred during login:', error);
    // Display an error message to the user
    alert('An error occurred during login. Please try again.');
  }
});
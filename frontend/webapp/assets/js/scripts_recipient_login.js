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
    $('#recipient_registration').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = {
            recipient_name: $('#name').val(),
            email: $('#email').val(),
            address: $('#address').val(),
            phone_number: $('#phone_number').val(),
            password: $('#password').val()
        };

        // Send data to register donor endpoint
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/recipients',
            contentType: 'application/json',
            data: JSON.stringify({
                name: formData.recipient_name,
                email: formData.email,
                address: formData.address,
                phone_number: formData.phone_number,
                
            }),
            success: function (recipientResponse) {
                console.log('Donor registration successful:', recipientResponse);

                // Once donor is registered, use the returned donor ID to create credentials
                var recipientId = recipientResponse.id;

                // Once donor is registered, use the email as username to create credentials
                var username = formData.email;

                // Send data to create credentials endpoint
                $.ajax({
                    type: 'POST',
                    url: 'http://127.0.0.1:8000/recipient_credentials/',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        username: username,
                        password: formData.password,
                        recipient_id: recipientId // Use the donorId obtained from the donor registration response
                    }),
                    success: function (credentialsResponse) {
                        console.log('Credentials creation successful:', credentialsResponse);

                        // Clear registration form fields
                        $('#recipient_registration input').val('');

                        // Pre-fill email in the username field of the login form
                        $('#login_form input[name="username"]').val(formData.email);

                        // Switch to the login form
                        container.classList.remove('active');

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
    const response = await fetch('http://127.0.0.1:8000/recipient_login', {
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
      window.location.href = 'http://localhost:63342/foodshareAPI/frontend/webapp/recipients/recipient_landing.html?_ijt=35res018oljtdsgn7a10sid2b7&_ij_reload=RELOAD_ON_SAVE';
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

// After successful credential creation
// $('#donor_registration input').val(''); // Clear registration form fields
// $('#login_form input[name="username"]').val(formData.email); // Pre-fill email in the username field
// container.classList.remove('active'); // Switch to the login form

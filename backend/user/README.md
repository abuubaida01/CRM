# API Documentations

# User Registration API
The `UserRegistrationView` is an API view that allows users to register for an account on the Sefarz platform. During registration, users provide their information, and the platform will send a verification email to the provided email address to ensure the user's identity. This API facilitates user account creation and email verification.

## Endpoint
- **URL:** `user/register/`
- **HTTP Method:** POST
- **View Class:** `UserRegistrationView`
- **Name:** `register`

## Permissions

- This API view is open to any user, whether they are authenticated or not, as it is the registration process.

## Request Parameters

- The request should be a POST request, and the data in the request should include the following parameters:

```json
{
    "email": "exmaple@gmail.com",
    "username": "example",
    "full_name": "example Khan",
    "religion": "Islam",
    "gender": "Male",
    "date_of_birth": "2xx1-xx-xx",
    "password": "exmaple123",
    "password2": "exmaple123"

}
```

## Response
```json
{
    "msg": "Registration Successful. Please check your email for verification instructions."
}
```

## Email Verification
During the registration process, an email verification link is sent to the user's provided email address. This link allows users to verify their email address and confirm their identity.

## Throttling
This API view includes a comment referencing throttling. Throttling can be used to limit the rate at which requests from the same user or IP address are processed. The comment mentions the use of the `OncePerDayUserThrottle` class, which restricts users to one request per day. Throttling helps protect the platform from abuse or excessive requests.

## Additional Information

- The registration process follows these steps:
  1. User provides registration details (email, username, password, and confirmation password).
  2. The provided details are validated to ensure correctness.
  3. If the details are valid, the user's account is created.
  4. An email with a verification link is sent to the provided email address.
  5. The user must follow the verification link to confirm their email address and activate their account.

'changeUserD/', ChangeUserDetailView


# Email Verification API
The `VerifyEmailView` is an API view responsible for verifying the email address of users who have registered on the Sefarz platform. Email verification is a crucial step in the registration process, ensuring that user-provided email addresses are valid and that users can be reached via this email. This API allows users to complete the email verification process.

## Endpoint
- **URL:** `user/verify/<str:token>/`
- **HTTP Method:** GET
- **View Class:** `VerifyEmailView`
- **user:** `verify-email`

## Permissions
- This API view is open to any user, whether they are authenticated or not. The email verification process should be accessible to all users.

## Request Parameters
- The request URL should include a token as a path parameter (`<str:token>`) that is used to verify the user's email address. This token is unique to each user and is sent in the verification email.

## Response
```json
{
    "msg": "Email verified successfully.",
    "Login here": "/login/"
}
```



# User Login API
The `UserLoginView` is an API view responsible for authenticating and logging in users on the Sefarz platform. Users provide their email address and password for authentication, and if the credentials are valid, they receive an access token, which allows them to access secured resources on the platform.

## Endpoint

- **URL:** `user/login/`
- **HTTP Method:** POST
- **View Class:** `UserLoginView`
- **Name:** `login`

## Permissions
- This API view is open to any user, whether they are authenticated or not. Users need to log in to access the platform's features, so this view does not require any specific permissions.

## Request Parameters
The request should include the following data in the request body:
- `email`: The user's email address.
- `password`: The user's password.

## Response
**Example Response (Successful Login):**
```json
{
    "token": "your_access_token_here",
    "msg": "Login Success"
}
```

**Example Response (Unverified Email):**
```json
{
    "msg": "Email not verified.",
    "Verify your email here": "/verify-email/some_verification_token/"
}
```




# User Change Password API
The `UserChangePasswordView` is an API view that allows authenticated users to change their password on the Sefarz platform. Users who wish to update their password can make a POST request to this endpoint.

## Endpoint
- **URL:** `user/changepassword/`
- **HTTP Method:** POST
- **View Class:** `UserChangePasswordView`
- **Name:** `changepassword`

## Permissions
- Only authenticated users have the permission to access this API view. Users must be logged in to change their password.

## Request Parameters
The request should include the following data in the request body:

- `old_password`: The user's current or old password.
- `new_password`: The new password the user wishes to set.

## Response
Upon successful password change, the API responds with a success message.

**Example Response (Password Change Success):**
```json
{
    "msg": "Password Changed Successfully"
}
```

## Password Change Process
The password change process follows these steps:

1. The user provides their current (old) password and the new password they wish to set.
2. The `UserChangePasswordView` API validates the provided data.
3. If the validation is successful, the user's password is updated with the new one.
4. A success message is sent to the user, confirming that the password change was successful.


# Send Password Reset Email API
The `SendPasswordResetEmailView` is an API view that allows users to request a password reset by sending them a password reset link via email. This API is accessible to both authenticated and unauthenticated users.

## Endpoint

- **URL:** `user/reswordEmail/`
- **HTTP Method:** POST
- **View Class:** `SendPasswordResetEmailView`
- **Name:** `send-reset-password-email`

## Permissions
- This API view allows any user (both authenticated and unauthenticated) to access it. It doesn't require user authentication to initiate a password reset request.

## Request
The request to this API should be a POST request. It doesn't require an authenticated user to access the view. The request body can include the following data:

- `email`: The email address associated with the user's account for which they want to reset the password.

## Response
**Example Response (Password Reset Initiated):**
```json
{
    "msg": "Password Reset link sent. Please check your Email"
}
```

## Password Reset Process
1. The user provides their email address to initiate the password reset.
2. The `SendPasswordResetEmailView` API validates the email address.
3. If the email address is associated with a user account, an email containing a password reset link is sent to the user.
4. The user will receive an email with instructions on how to reset their password.


# User Password Reset API
The `UserPasswordResetView` is an API view that allows users to reset their password after receiving a password reset link via email. This API is accessible to both authenticated and unauthenticated users.

## Endpoint

- **URL:** `user/reset/<uid>/<token>/`
- **HTTP Method:** POST
- **View Class:** `UserPasswordResetView`
- **Name:** `reset-password`

## Permissions
- This API view allows any user (both authenticated and unauthenticated) to access it. It doesn't require user authentication to reset a password using the provided reset token.

## Request
these parameters are in url
- `uid`: A unique identifier for the user. This identifier is typically included in the password reset link sent via email.
- `token`: A token that serves as a security measure for password reset. It's also included in the password reset link.

```json
{
    "password": "JaniMani",
    "password2": "JaniMani"
}
```


## Response
**Example Response (Password Reset Success):**
```json
{
    "msg": "Password Reset Successfully"
}
```




# Change User Detail API
The `ChangeUserDetailView` is an API view that allows authenticated users to change their user details, such as their profile information. This API is designed to handle updates to user profiles and other related information.

## Endpoint
- **URL:** `user/changeUserD/`
- **HTTP Method:** PUT
- **View Class:** `ChangeUserDetailView`

## Permissions
- Only authenticated users are permitted to access this API view. Users must be logged in to change their user details.

## Request
```json
{
    "username": "new_username",
    "email": "new_email@example.com",
    "full_name": "New Full Name",
    "profile_picture": "http://example.com/new_profile_picture.jpg",
    "other_fields": "Updated user details..."
}
```

## Response
Upon successfully changing the user's details, the API will respond with the updated user information in the response body.

```json
{
    "username": "new_username",
    "email": "new_email@example.com",
    "full_name": "New Full Name",
    "profile_picture": "http://example.com/new_profile_picture.jpg",
    "other_fields": "Updated user details..."
}
```


# List User Details API
The `listUserDetailsApi` is an API view that allows authenticated users to list their own user details. This API view is designed to retrieve and display the user's details and can be useful for users to view their own profile information.

## Endpoint
- **URL:** `user/getuserD/`
- **HTTP Method:** GET
- **View Class:** `listUserDetailsApi`

## Permissions
- Only authenticated users are permitted to access this API view. Users must be logged in to list their user details.

## Request
The request to this API should be a GET request, and it must be made by an authenticated user.

## Response
Upon a successful GET request, the API will respond with the user's details in the response body.

```json
{
    "id": 1,
    "username": "user_username",
    "email": "user_email@example.com",
    "full_name": "User Full Name",
    "profile_picture": "http://example.com/user_profile_picture.jpg",
    "other_fields": "User details..."
}
```

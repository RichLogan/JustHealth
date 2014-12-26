========================
Full API Listing
========================

Listed below is the complete list of possible API calls to JustHealth, broken down by their general function.

Each method will show its:

- URL
- Method type (POST or GET)
- POST / GET parameters
- Possible return values

------------------------
Login Functions
------------------------

.. autofunction:: justHealthServer.api.authenticate

  :URL: /api/authenticate
  :URL: /api/authenticate
  :HTTP_METHOD: POST

  :param username: The username to authenticate
  :param password: The attempted password to check

Return values:
  "Authenticated"
    - If both the username and password are correct and the account is not locked or deactivated.
  "Incorrect Username/Password"
    - Either the username or password is incorrect or the user does not exist.
  "Account deactivated"
    - The account has ``accountdeactivated = True``
  "Account not verified. Please check your email for instructions"
    - The account has ``verified = False``
  "Account is locked. Please check your email for instructions"
    - The account has ``accountlocked = True``

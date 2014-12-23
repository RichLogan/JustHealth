# Sphinx Readme

 ###1. Create RST document
  Pretty straightforward, you make a document call whatever.rst and start writing. Heading are shown by ----- or ========. Lists are done through 1. blah blah

To talk about code you do something like this:

```rst
.. autofunction:: justHealthServer.api.authenticate
```

Automatically links the source code of the file.

```
  :URL: /api/authenticate
  :URL: /api/authenticate
  :HTTP_METHOD: POST

  :param username: The username to authenticate
  :param password: The attempted password to check

```
Automatically will list these properly.

```
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
```
Do this to list all the return values.

 ###2. Link new file in index.rst

Just write the filename in the place you want it to go.

ggwp

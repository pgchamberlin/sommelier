# The Sommelier app

## Routes

### User authentication

Authentication:

    /authenticate

 - GET returns a login form
 - POST logs in the user or returns the login form with error schema

    /deauthenticate/%key%

 - GET deauthenticates the currently logged in user

I will not implement a fully featured login system - this project is more concerned with recommendations.


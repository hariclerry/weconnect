
[![Build Status](https://travis-ci.org/hariclerry/weconnect.svg?branch=fearture_challenge3_api)](https://travis-ci.org/hariclerry/weconnect)
[![Coverage Status](https://coveralls.io/repos/github/hariclerry/weconnect/badge.svg?branch=fearture_challenge3_api)](https://coveralls.io/github/hariclerry/weconnect?branch=fearture_challenge3_api)
# We Connect APP
INTRODUCTION
WeConnect Web App provides a platform that brings businesses and individuals together. 
This platform creates awareness for businesses and gives the users the ability to register their businesses and write reviews about the businesses they have interacted with. It is built using Python and Flask micro framework.

click here to access WeConnect https://hariclerry.github.io pages


FEATURES

with We Connect APP you can:
* create an account
* login into the account
* register a business
* update a business
* view a business
* delete a business
* add review on a business
* view reviews on a particular business
* logout

INSTRUCTIONS

1.Pre-requisites
2.Setup and intallations
3.Authors


PRE-REQUISITES

For developers, you need to have installed the following

1. Python 2.7 or Python 3

2. GitSys

3.[Postgresql](https://www.postgresql.org/download/)

Setup and Installation

clone the repo

`$git clone https://github.com/hariclerry/weconnect.git`

Setup your database, if you do not have postgresql installed please click on the 
link above.

To run the API on local server, navigate to `config.py` , change the user name and password to your username and password 
`postgresql://your_username:your_password@localhost/weconnect` 

For windows, run the 
`setup.bat`

The above setup file will install and initialise a virtual environment, install dependencies using `pip`
and run the server.

RUNNING TESTS
* Install nosetests `pip install nose`
* Run the tests `nosetests -v`

VERSIONS

The API runs with one version, Version 1 

Input `http:127.0.0.1:5000/` followed by any of the following endpoints to demo version 1.

|EndPoint|Functionality|
|---------|------------|
|[POST/v1/api/auth/register]|Creates a user account|
|[POST/v1/api/auth/login]|Logs in a user|
|[POST/v1/api/auth/logout]|Logs out a user|
|[POST/v1/api/auth/reset-password]|Password reset|
|[POST/v1/api/businesses]|Register a business|
|[PUT/v1/api/businesses/<business_id>]|Updates a business profile|
|[DELETE/v1/api/businesses/<business_id>]|Remove a business|
|[GET/v1/api/businesses]|Retrieves all businesses|
|[GET/v1/api/businesses/<business_id>]|Get a business|
|[POST/v1/api/businesses/<business_id>/reviews]|Add a review for a business|
|[GET/v1/api/businesses/<business_id>/reviews]|Get all reviews for a business|


For more about using the API check 127.0.0.1:5000/apidocs or [`https://weconnect-harriet5.herokuapp.com/apidocs/`](https://weconnect-harriet5.herokuapp.com/apidocs/)
How to run API on windows
* set 'FLASK_CONFIG=run.py'
* set 'APP_CONFIG=run.py'
* Run  `python run.py`
   |

Credits

[Harriet]: https://github.com/hariclerry

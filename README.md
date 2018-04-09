
[![Build Status](https://travis-ci.org/hariclerry/weconnect.svg?branch=fearture_challenge3_api)](https://travis-ci.org/hariclerry/weconnect)
[![Coverage Status](https://coveralls.io/repos/github/hariclerry/weconnect/badge.svg)](https://coveralls.io/github/hariclerry/weconnect)
# We Connect APP
### Introduction
WeConnect Web App provides a platform that brings businesses and individuals together. 
This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.

click here to access We Connect https://hariclerry.github.io pages

#### Getting Started
To start using the We Connect:
git clone:
'https://github.com/hariclerry/weconnect'
into your computer
* change your directory into `cd weconnect`
#### Usage
with We Connect APP you can:
* create an account
* login into the account
* register a business
* update a business
* view a business
* delete a business
* add review on a business
* logout
#### Setting
* First install the virtual environment globally `sudo pip instal virtualenv`
* create the virtual enviroment `virtualenv --python=python3 myvenv`
* activate virtual environment `source myvenv/bin/activate`
#### How to run flask on windows
* set 'FLASK_CONFIG=run.py'
* set 'APP_CONFIG=run.py'
* Run  `python run.py`

#### Testing:
* Install nosetests `pip install nose`
* Run the tests `nosetests -v`
#### Flask API endpoints

| Endpoints                                       |       Functionality                  |
| ------------------------------------------------|:------------------------------------:|
| `POST /api/auth/register                      |  registers a user                    |
| `POST /api/auth/login                         |  login a user                        |   
| `POST /api/v1/businesses                           |  register a business |
| `GET /api/v1/businesses                           |  Retrieves a business                  |
| `PUT /api/v1/businesses/businessid>                  |  updates a business                     |
| `DELETE /api/v1/businesses/<businessid>               |  deletes a business                    |
| `POST /api/v1/business/<businessid>/review             |  create a review                      |
| `GET /api/v1/business/<businessid>/review              |  returns reviews for a business                  | 
|` POST /api/v1/logout                          |  logout a user                       |

### Credits
* [Harriet][1]
[1]: https://github.com/hariclerry

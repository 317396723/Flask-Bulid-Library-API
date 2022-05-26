## Library System Description 
Author: Shuhao Guan
### Flask
The library book borrow and return api system is written by **Flask**, that lets you develop web applications easily. 

### Flask-SQLAlchemy
Flask doesn’t include an ORM (Object Relational Manager) or such features, so the api system use **Flask-SQLAlchemy**  extension that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

### MySQL
We use MySQL to be our database, that most popular Open Source SQL database management system. We use MySQL because MySQL is more reliable than sqlite that will always lock databse when operate in multi thread.

## API List

### Query Api List

#### Description
the query api is a method that return the api list and how to use the api

#### Api Url
> http://127.0.0.1:5000/api

#### Method
> GET

#### Data return
```
{
  "api_list": [
    {
      "description": "query all books", 
      "method": "GET", 
      "url": "/api/v1/books"
    }, 
    {
      "description": "borrow book", 
      "method": "POST", 
      "params": {
        "ids": "1,2,3", 
        "user_id": "1"
      }, 
      "url": "/api/v1/book/borrow"
    }, 
    {
      "description": "return book", 
      "method": "POST", 
      "params": {
        "ids": "1,2,3", 
        "user_id": "1"
      }, 
      "url": "/api/v1/book/return"
    }
  ], 
  "msg": "api list"
}
```

### Query Books Api

#### Description
The query books api that can query all the books and the book's inventory

#### Api Url
> http://127.0.0.1:5000/api/v1/books

#### Method
> GET


#### Data return 
```
[
  {
    "bookname": "A Doll's House", 
    "id": 1, 
    "num": 3
  }, 
  {
    "bookname": "A Farewell to Arms", 
    "id": 2, 
    "num": 2
  }, 
  {
    "bookname": "A Midsummer Night's Dream", 
    "id": 3, 
    "num": 1
  }, 
  {
    "bookname": "A Tale of Two Cities", 
    "id": 4, 
    "num": 1
  }, 
  {
    "bookname": "A Thousand and One Nights", 
    "id": 5, 
    "num": 1
  }, 
  {
    "bookname": "Adam Bede", 
    "id": 6, 
    "num": 1
  }, 
  {
    "bookname": "Wuthering Heights", 
    "id": 7, 
    "num": 1
  }, 
  {
    "bookname": "Wives and Daughters", 
    "id": 8, 
    "num": 1
  }
]
```



### Borrow Book Api

#### Description
The api that let user borrow book

#### Api Url
> http://127.0.0.1:5000/api/v1/book/borrow

#### Method
> POST

#### Request Body
param | example | type | required | desc
--- | --- | --- | --- | ---
ids | 1,2 | Text | yes | book id list that use dot connect
user_id | 1 | Text | yes | user id


#### Data return 
```
{
	"already_borrow_books": [],
	"can_borrow_books": [
		"A Doll's House",
		"A Farewell to Arms"
	],
	"msg": "action success"
}
```

### Return Book Api
#### Api Url
> http://127.0.0.1:5000/api/v1/book/return

#### Method
> POST

#### Request Body
param | example | type | required | desc
--- | --- | --- | --- | ---
ids | 1,2 | Text | yes | book id list that use dot connect
user_id | 1 | Text | yes | user id


#### Description
The api that let user return book

#### Data return 
```
{
	"msg": "action success"
}
```


## How to deploy?

First of all, you need to install MySQL, then follow the steps below.

### 1. Install python3 and install requirements

#### 1) Install python3

You can download python3 from [https://www.python.org/downloads/](https://www.python.org/downloads/), when you install python, DO NOT forget to install pip3 and Add python3 to your PATH.

#### 2) Install requirements

After you install python3, you can install requirements by command:

```
pip3 install -r requirements.txt
```

### 2. Change the manage.py file and create database

#### 1) Change the manage.py file
Open the `manage.py` file and change the `MYSQL_HOST`、`MYSQL_USER`、`MYSQL_PASSWORD`、`MYSQL_DB` and `MYSQL_PORT` to your own config.

#### 2) Create database
You can create database by command:

```
$env:FLASK_APP="mangage.py" # set the flask app
flask initdb # create database
```

### 3. Run the api system

You can run the api system by command:

```
flask run
```

### 4. Test the api system
You should install ApiPost or Postman to test the api system.

have fun!
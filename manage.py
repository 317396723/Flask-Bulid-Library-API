from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import random
import string 

strings=string.ascii_letters+string.digits

class Confg:
    """
    配置项
    """
    MYSQL_HOST='127.0.0.1'
    MYSQL_PORT=3306
    MYSQL_USER='root'
    MYSQL_PASSWORD='317396723'
    MYSQL_DB='book_api'
    MYSQL_CHARSET='utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST,MYSQL_PORT,MYSQL_DB,MYSQL_CHARSET)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '317396723'

#Initialising the app
app=Flask(__name__)
#Configure the app
app.config.from_object(Confg)
#Initialising the database
db=SQLAlchemy(app)

#Creating the database model

#Intermediate table, table of relationships between users and books
user_borrow_book=db.Table('user_borrow_book',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('book_id',db.Integer,db.ForeignKey('book.id'))
)

#User table
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True)

    #Define a method to insert a virtual user
    @staticmethod
    def generate_user():
        for i in range(10):
            user=User()
            user.username=''.join(random.sample(strings,5))
            db.session.add(user)
        db.session.commit()

#Book table
class Book(db.Model):
    __tablename__='book'
    id=db.Column(db.Integer,primary_key=True)
    bookname=db.Column(db.String(32),unique=True)
    num=db.Column(db.Integer,default=1)

    #Foreign key association
    users=db.relationship('User',secondary=user_borrow_book,backref=db.backref('books',lazy='dynamic'),lazy='dynamic')


    #Define a method to insert a virtual book
    @staticmethod
    def generate_book():
        books=["A Doll's House","A Farewell to Arms","A Midsummer Night's Dream","A Tale of Two Cities","A Thousand and One Nights","Adam Bede","Wuthering Heights","Wives and Daughters"]
        for bookname in books:
            book=Book()
            book.bookname=bookname
            db.session.add(book)
        db.session.commit()




#api:Find a list of all books
@app.route('/api/v1/books')
def get_books():
    #Search all books
    books=Book.query.all()
    #Create a list to hold information about books
    books_list=[]
    for book in books:
        books_list.append({
            'id':book.id,
            'bookname':book.bookname,
            'num':book.num
        })
    return jsonify(books_list)

#api:User Borrowed Books
@app.route('/api/v1/book/borrow',methods=['POST'])
def borrow_book():
    ids=request.form.get('ids')
    user_id=request.form.get('user_id')
    #Enquiry User
    user=User.query.get(user_id)
    #Enquiry Book
    books=Book.query.filter(Book.id.in_(ids.split(','))).all()
    #Two lists, one of available books and one of borrowed books
    can_borrow_books=[]
    already_borrow_books=[]
    for book in books:
        if book.num>0:
            can_borrow_books.append(book.bookname)
            book.num-=1
            book.users.append(user)
        else:
            already_borrow_books.append(book.bookname)
    db.session.commit()
    return jsonify({
        "msg":"action success",
        "can_borrow_books":can_borrow_books,
        "already_borrow_books":already_borrow_books
    })

#api:User return of books
@app.route('/api/v1/book/return',methods=['POST'])
def return_book():
    ids=request.form.get('ids')
    user_id=request.form.get('user_id')
    #Enquiry User
    user=User.query.get(user_id)
    #Enquiry Book
    for id in ids.split(','):
        book=Book.query.get(id)
        if book:
            if book.users.filter(User.id==user_id).first():
                book.num+=1
                book.users.remove(user)
    db.session.commit()
    return jsonify({
        "msg":"action success"
    })



#api:api list
@app.route('/api')
def api_list():
    data={
        "msg":"api list",
        "api_list":[
            {
                "url":"/api/v1/books",
                "method":"GET",
                "description":"query all books"
            },
            {
                "url":"/api/v1/book/borrow",
                "method":"POST",
                "description":"borrow book",
                "params":{
                    "ids":"1,2,3",
                    "user_id":"1"
                }
            },
            {
                "url":"/api/v1/book/return",
                "method":"POST",
                "description":"return book",
                "params":{
                    "ids":"1,2,3",
                    "user_id":"1"
                }
            }
        ]
    }
    return jsonify(data)


#cli:Initialising the database
@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    User.generate_user()
    Book.generate_book()
    print('Initialising the database')

if __name__=='__main__':
    """
    $env:FLASK_APP="manage.py"
    flask initdb #Initialising the database
    """
    import sys
    #initdb()
    app.run(debug=True)



    


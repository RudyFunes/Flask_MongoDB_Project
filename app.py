from flask import Flask,render_template,request,url_for
from flask_pymongo import PyMongo,MongoClient
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,SelectField,DecimalField
from wtforms.validators import DataRequired

import test

import api_methods
import main_functions

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456789QWEdfgfdgfdgdfgdfgdf"
app.config["MONGO_URI"] = "mongodb+srv://rudyj4000:zPYqm77mOiXhQRgJ@learningmongodb.rvgwn.mongodb.net/db?retryWrites=true&w=majority"

mongo = PyMongo(app)





class Expenses(FlaskForm):

    description = StringField("New Item Description")

    category = SelectField("Category",
                        choices=[('games','Video Games'),
                                ('music','Music'),
                                ('anime','Anime'),
                                ('movies','Movies'),
                                ('food','Food'),
                                ('books','Books'),
                                ('electronics','Electronics'),
                                ('cars','Cars'),
                                ('restaurants','Restaurants'),
                                ('clothing','Clothing')
                                ])
    cost = DecimalField(places=2, validators=[DataRequired("Please Enter Price:")])

    currency = SelectField("Currency",
                           choices = [
                                   ("USD","US Dollar"),
                                   ("USDMXN","Mexican Peso"),
                                   ("USDJPY","Japanese Yen"),
                                   ("USDINR","Indian Rupee"),
                                   ("USDCRC","Costa Rica Colon"),
                                   ("USDCAD","Canadian Dollar"),
                                   ("USDBRL","Brazilian Real"),
                                   ("USDEUR","Euro"),
                                   ("USDGBP", "British Pound")
                                    ])
    date = DateField(
        label='Start Date',
        format='%y-%m-%d',
        validators=[DataRequired("Please select a date:")])



def get_total_expenses(category):
    category_expenses = mongo.db.expenses.find()
    category_cost = 0
    for i in category_expenses:
        if category == i['category']:
            category_cost += float(i["cost"])
    return category_cost
    # TO BE COMPLETED (please delete the word pass above)

@app.route('/')
def index():
    my_expenses = mongo.db.expenses.find()

    total_cost=0
    last_item_bought = 0
    last_item_name = ''
    last_category =''
    for i in my_expenses:
        total_cost+=float(i["cost"])
        last_item_bought = float(i["cost"])
        last_item_name = i["description"]
        last_category = i["category"]
    expensesByCategory = [
         ("games" , get_total_expenses("games")),
        ("music", get_total_expenses("music")),
        ("anime", get_total_expenses("anime")),
        ("movies", get_total_expenses("movies")),
        ("food", get_total_expenses("food")),
        ("books", get_total_expenses("books")),
        ("electronics", get_total_expenses("electronics")),
        ("restaurants", get_total_expenses("restaurants")),
        ("clothing", get_total_expenses("clothing")),
         ("cars", get_total_expenses("cars"))]


    # expensesByCategory is a list of tuples
    # each tuple has two elements:
    ## a string containing the category label, for example, insurance
    ## the total cost of this category
    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory,lastPurchase=last_item_bought,lastItem= last_item_name,lastCategory=last_category)

@app.route('/addExpenses',methods=["GET","POST"])
def addExpenses():
    # INCLUDE THE FORM
    expensesForm = Expenses((request.form))
    if request.method == "POST":
        description = request.form['description']
        category  = request.form['category']
        cost = request.form['cost']
        currency = request.form['currency']
        date = request.form['date']
        # makes teh conversion if transaction ot in USD
        currencyAPI = api_methods.Currency()
        main_functions.save_to_file(currencyAPI, 'JSON_Files/Currencies.json')
        typeOfMoney = api_methods.get_Currencies_in_JSON()
        #makes the covertsion to USD if ttransaction not in USD
        if currency != "USD":
           for moneyType in typeOfMoney['quotes']:
               if moneyType == currency:
                   x = typeOfMoney['quotes'][currency]
                   cost = int(cost) / x



        #new document to be wstore in mongo documents
        new_document ={
            "description":description,
            "category":  category,
            "cost": cost,
            "date": date
        }


        # INSERT ONE DOCUMENT TO THE DATABASE
        collection = mongo.db.expenses
        collection.insert_one(new_document)

        # CONTAINING THE DATA LOGGED BY THE USER
        # REMEMBER THAT IT SHOULD BE A PYTHON DICTIONARY
        return render_template("expenseAdded.html")
    return render_template("addExpenses.html",form=expensesForm)


app.run(debug=True,port=5000)
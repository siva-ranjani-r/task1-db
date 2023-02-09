from flask import Flask,render_template,request,redirect,url_for
from pymongo import MongoClient

app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        client=MongoClient("mongodb://127.0.0.1:27017")
        database=client.shop
        collection=database.users
        collection.insert_one({"name":name,"password":password})
        client.close()

    client=MongoClient("mongodb://127.0.0.1:27017")
    database=client.shop
    collection=database.products
    data=collection.find()
    l=[]
    for i in data:
        l.append(i)
    client.close()
    
    return render_template("index.html",data=l)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/show",methods=["POST","GET"])
def show():
    if request.method=="POST":
        name=request.form.get("name")
        client=MongoClient("mongodb://127.0.0.1:27017")
        database=client.shop
        collection=database.ordered
        x=collection.find({"name":name})
        l=[]
        for i in x:
            l.append(i)
        client.close()
        return render_template("history.html",data=l)
    return render_template("show.html")

@app.route("/order",methods=["POST","GET"])
def order():
    if request.method=="POST":
        name=request.form.get("name")
        product=request.form.get("product")
        price=request.form.get("price")

        client=MongoClient("mongodb://127.0.0.1:27017")
        database=client.shop
        collection=database.ordered
        collection.insert_one({"name":name,"product":product,"price":price})
        client.close()
        return "<h1>order received</h1>"
    return render_template("order.html")

if __name__=="__main__":
    app.run(debug=True)
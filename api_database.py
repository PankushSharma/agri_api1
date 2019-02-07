# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 16:16:17 2019

@author: PANKUSH
"""
from flask import Flask,jsonify,request
import sqlalchemy as db
import pandas as pd
agri=Flask(__name__)
engine = db.create_engine('mysql://sql12277829:VQhDuGbs7b@sql12.freemysqlhosting.net:3306/sql12277829')
connection = engine.connect()
metadata = db.MetaData()
customer = db.Table('customer', metadata, autoload=True, autoload_with=engine)
#result=connection.execute(customer).fetchall()
# insert command
@agri.route("/create",methods=["Post"])
def posting():
    user=request.get_json()
    un=user["username"]
    pw=user["password"]
    try:
        ins_record = customer.insert().values(username=un,password=pw)
        ResultProxy = connection.execute(ins_record)
        return jsonify({"username created":user["username"]})
    except:
         return jsonify({"username already exist re-enter another username":user["username"]})

#update command
@agri.route("/update_username",methods=["PUT"])
def update():
        user=request.get_json() 
        un=user["username"]
        pw=user["password"]
        new_un=user["new_username"]
        new_pw=user["new_password"]
        try:
            Result_proxy=engine.execute("select *  from customer where customer.username='%s' and customer.password='%s'"%(un,pw))
            Record=Result_proxy.fetchall() 
            print(Record)    
            if len(Record)==1:
                if Record[0][1]==un:
                    result = engine.execute("update customer set username ='%s', password ='%s' where username='%s' and password='%s'" %(new_un,new_pw,un,pw))
                    return jsonify({"username updated new username":user["new_username"]})
            elif len(Record)==0:
                  return jsonify({"invalid username enter again":user["username"]})
        except:
             return jsonify({"username already exist re-enter another username":user["new_username"]})
@agri.route("/delete",methods=["DELETE"])
def Delete():
    user=request.get_json() 
    un=user["username"]
    pw=user["password"]
    Result_proxy=engine.execute("select *  from customer where customer.username='%s' and customer.password='%s'"%(un,pw))
    Record=Result_proxy.fetchall()
    print(Record)        
    if len(Record)==1:
            if Record[0][1]==un:
                result=engine.execute("DELETE FROM customer WHERE customer.username='%s'"%(un))
                return jsonify({"username deleted":user["username"]})
    elif len(Record)==0:
              return jsonify({"invalid username or password":user["username"]})
agri.run(port=2003)            
                
            
    
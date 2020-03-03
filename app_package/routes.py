from flask import render_template,flash,redirect,url_for
from app_package import app,db,mongo
from flask_login import current_user,login_user,logout_user,login_required
from app_package.forms import LoginForm,RegistrationForm,CreationForm,WithdrawForm,DepositForm,DeleteForm,BalanceForm,ConfirmForm
from app_package.models import User

cust_id=0
@app.route("/",methods=["GET","POST"])

def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:    
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid user")
                return redirect(url_for("index"))
            else:
                login_user(user,remember=form.remember_me.data)
                return redirect(url_for("menu"))
        else:
            return render_template("login.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=RegistrationForm()
        if form.validate_on_submit():
            user=User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User registered.You may login now")
            return redirect(url_for("index"))
        else:
            return render_template("register.html",form=form)

@app.route("/menu")
@login_required 
def menu():
     return render_template("menu.html")       
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
@app.route("/created",methods=["GET","POST"])
def created():
    form=CreationForm()
    if form.validate_on_submit():
        customer=Customer(customername=form.customername.data)
        db.session.add(customer)
        db.session.commit()
        flash("Customer registered successfully")
        return redirect(url_for("menu"))
    else:
        return render_template("create.html",form=form)

@app.route("/create",methods=["GET","POST"])
@login_required 
def create():
    global cust_id
    form=CreationForm()
    if form.validate_on_submit():
        fields=["_id","cid","name","acc_type","balance","mobile","aadhar"]
        cust_id+=1
        values=[cust_id,form.cid.data,form.name.data,form.acctype.data,form.balance.data,form.mobile.data,form.aadhar.data]
        customer=dict(zip(fields,values))
        cust_col=mongo.db.customers
        tmp=cust_col.insert_one(customer)
        if tmp.inserted_id==cust_id:
            flash("customer added")
            return redirect(url_for("menu"))
        else:
            flash("Problem adding customer")
            return redirect(url_for("logout"))
    else:
        return render_template("create.html",form=form)                
    
@app.route("/deposit",methods=["GET","POST"])
def deposit():
    form=DepositForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"cid":form.cid.data}
        cust=cust_col.find_one(query)
        bal=cust["balance"]
        new_bal=bal+form.amt.data
        new_data={"$set":{"balance":new_bal}}
        cust_col.update_one(query,new_data)       
        flash("Deposited")
        return redirect(url_for("menu"))
    else:
        return render_template("deposit.html",form=form)    
@app.route("/withdraw",methods=["GET","POST"])
def withdraw():
    form=WithdrawForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"cid":form.cid.data}
        cust=cust_col.find_one(query)
        bal=cust["balance"]
        atype=cust["acc_type"]
        new_bal=bal-form.amt.data
        if atype=="priority" and new_bal<50000 or atype=="ordinary" and new_bal<10000:
            flash("upon withdrawal min balance is not maintained")
            return redirect(url_for("menu"))
        else:
            new_data={"$set":{"balance":new_bal}}
            cust_col.update_one(query,new_data)       
            flash("Withdrawal done")
            return redirect(url_for("menu"))
    else:
        return render_template("deposit.html",form=form)  
          
@app.route("/balance",methods=["GET","POST"])
def balance():
    form=BalanceForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"cid":form.cid.data}
        customers=cust_col.find(query)
        return render_template("display_customer.html",customers=customers)  
    else:
        return render_template("balance.html",form=form) 
    
       
@app.route("/delete",methods=["GET","POST"])
def delete():
    form=DeleteForm()
    f2=ConfirmForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"cid":form.cid.data}
        customers=cust_col.find(query)
        return render_template("confirm.html",f2=f2,customers=customers)  
    else:
        return render_template("delete_customer.html",form=form)        
    
        
@app.route("/confirm",methods=["GET","POST"])
def confirm():
    f2=ConfirmForm()
    cust_col=mongo.db.customers
    query={"cid":f2.cid.data}
    cust_col.delete_one(query)
    flash("Customer deleted")
    return redirect(url_for("menu"))

   


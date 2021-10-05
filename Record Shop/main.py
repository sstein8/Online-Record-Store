from flask import Flask, session
from flask import render_template, request
import mysql.connector
app = Flask('app')
app.secret_key = 'mysecretkey'
mydb = mysql.connector.connect(host="ec2-23-21-57-219.compute-1.amazonaws.com", user="sstein1208", password="seas",database="shoppingcart")


@app.route('/')
def Home_Page():
  return render_template("Home_Page.html")

@app.route('/search', methods=['GET','POST'])
def search():
  #depending on what they search, bring them to that page
  if request.method == 'POST':
    c = mydb.cursor()
    searchWord = request.form['searchWord']
    c.execute('SELECT genre FROM product WHERE pname=%s', (searchWord,))
    genre = c.fetchone()
    
    if(genre): #if the album they searched for exists
      genre = genre[0]
      if(genre == 'Rock'):
        return render_template("Rock_Albums.html")
      elif(genre == 'Pop'):
        return render_template("Pop_Albums.html")
      elif(genre == 'HipHop'):
         return render_template("HipHop_Albums.html")
      else:
        return render_template("Disco_Albums.html")
    elif(genre is None): #the album they searched for does not exist
      message="The album you are looking for is not in stock"
      return render_template("Home_Page.html", notInStock=message)
    c.close()

@app.route('/login', methods=['GET','POST'])
def login():
  
  if request.method == 'POST':
    c = mydb.cursor()
    
    UserName = request.form['UserName']
    Password = request.form['Password']

    #create session that stores username that can be accessed from other pages
    session["UserName"] = UserName

    c.execute("SELECT Username, Password FROM customer WHERE UserName=%s AND Password=%s", (UserName, Password))

    results = c.fetchone()
    if results:
      return render_template('LogIn_Page.html', message="Successful login")
    elif results is None: 
      # return 'UserName/Password incorrect.'
      return render_template('LogIn_Page.html', message="Username or Password incorrect")
    c.close()
    

  return render_template('LogIn_Page.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
  message = ''
  if request.method == 'POST':
    
    #get the registration info from the sign up page
    FirstName = request.form['FirstName']
    LastName = request.form['LastName']
    UserName = request.form['UserName']
    Password = request.form['Password']

    c = mydb.cursor()
    c.execute('SELECT * FROM customer WHERE UserName=%s', (UserName,))

    results = c.fetchone()
    if results:
      msg = "Username is already taken, try another one."
    else:
      c.execute('''INSERT INTO customer (FirstName, LastName, UserName, Password) VALUES (%s, %s, %s, %s)''', (FirstName, LastName, UserName, Password))
      message='Signup Complete'
      
  return render_template('SignUp_Page.html', message= message)
  c.close()

@app.route('/rock', methods=['GET','POST'])
def rock():
  c = mydb.cursor()
  if request.method == 'POST':
    if("UserName" not in session):
      byemessage="Please log in to purchase items"
      return render_template('Home_Page.html', byemessage=byemessage)

    message=""

    #receive the information about the album selected (name, quantity, price, ID)
    quantity = request.form['quantity']
    quantity = int(quantity)
    price = request.form['price']
    price = float(price)
    totPrice = (quantity * price) 
    productID = request.form['productID']
    productID = int(productID)
    pname = request.form['pname']

    #see how many are left in stock
    c.execute('SELECT quantity FROM product WHERE pname =%s', (pname,))
    quantityLeft = c.fetchone() #get the current quantity 
    SQ = quantityLeft[0] - quantity 
  
    #check if user is logged in
    if("UserName" in session):
      subtractQuantity = quantityLeft[0] - quantity 

      if(subtractQuantity >= 0): #you can make a valid purchase
        c.execute('SELECT * FROM cart where pname=%s', (pname,))
        rowInCart = c.fetchone()
        if not rowInCart: #you are selecting an item that is not already in the cart
          c.execute('UPDATE product SET quantity=%s where pname=%s', (subtractQuantity, pname,))
          c.execute('''INSERT INTO cart (pname, productID, sumPrice, quantity) VALUES (%s, %s, %s, %s)''', (pname, productID, totPrice, quantity))
    
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
        else: #you are adding to the quantity of an item already in cart
          c.execute('SELECT quantity, sumPrice FROM cart where pname=%s', (pname,))
          row = c.fetchone()
          quantityInCart = row[0]
          priceInCart = row[1]
          newQuantity = quantity + quantityInCart
          newPrice = totPrice + priceInCart
      
          c.execute('UPDATE cart SET quantity=%s, sumPrice=%s where pname=%s', (newQuantity, newPrice, pname))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
      else:
        ATCmessage = "Not enough items in stock, select fewer, " + str(quantityLeft[0]) + " albums left"

      return render_template('Rock_Albums.html', ATCmessage=ATCmessage)

  return render_template('Rock_Albums.html')
  c.close()

@app.route('/disco', methods=['GET','POST'])
def disco():
  if request.method == 'POST':
    if("UserName" not in session):
      byemessage="Please log in to see items"
      return render_template('Home_Page.html', byemessage=byemessage)

    message=""

    #receive the information about the album selected (name, quantity, price, ID)
    quantity = request.form['quantity']
    quantity = int(quantity)
    price = request.form['price']
    price = float(price)
    totPrice = (quantity * price) 
    productID = request.form['productID']
    productID = int(productID)
    pname = request.form['pname']

    c = mydb.cursor()

    #see how many are left in stock
    c.execute('SELECT quantity FROM product WHERE pname =%s', (pname,))
    quantityLeft = c.fetchone() #get the current quantity 
    SQ = quantityLeft[0] - quantity 
  
    #check if user is logged in
    if("UserName" in session):
      subtractQuantity = quantityLeft[0] - quantity 

      if(subtractQuantity >= 0): #you can make a valid purchase
        c.execute('SELECT * FROM cart where pname=%s', (pname,))
        rowInCart = c.fetchone()
        if not rowInCart: #you are selecting an item that is not already in the cart
          c.execute('UPDATE product SET quantity=%s where pname=%s', (subtractQuantity, pname,))
          c.execute('''INSERT INTO cart (pname, productID, sumPrice, quantity) VALUES (%s, %s, %s, %s)''', (pname, productID, totPrice, quantity))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
        else: #you are adding to the quantity of an item already in cart
          c.execute('SELECT quantity, sumPrice FROM cart where pname=%s', (pname,))
          row = c.fetchone()
          quantityInCart = row[0]
          priceInCart = row[1]
          newQuantity = quantity + quantityInCart
          newPrice = totPrice + priceInCart
          c.execute('UPDATE cart SET quantity=%s, sumPrice=%s where pname=%s', (newQuantity, newPrice, pname))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
      else:
        ATCmessage = "Not enough items in stock, select fewer, " + str(quantityLeft[0]) + " albums left"

      return render_template('Disco_Albums.html', ATCmessage=ATCmessage)
  
  
  return render_template('Disco_Albums.html')
  c.close()

@app.route('/pop', methods=['GET','POST'])
def pop():
  if request.method == 'POST':
    if("UserName" not in session):
      byemessage="Please log in to see items"
      return render_template('Home_Page.html', byemessage=byemessage)

    message=""

    #receive the information about the album selected (name, quantity, price, ID)
    quantity = request.form['quantity']
    quantity = int(quantity)
    price = request.form['price']
    price = float(price)
    totPrice = (quantity * price) 
    productID = request.form['productID']
    productID = int(productID)
    pname = request.form['pname']

    c = mydb.cursor()

    #see how many are left in stock
    c.execute('SELECT quantity FROM product WHERE pname =%s', (pname,))
    quantityLeft = c.fetchone() #get the current quantity 
    SQ = quantityLeft[0] - quantity 
  
    #check if user is logged in
    if("UserName" in session):
      subtractQuantity = quantityLeft[0] - quantity 

      if(subtractQuantity >= 0): #you can make a valid purchase
        c.execute('SELECT * FROM cart where pname=%s', (pname,))
        rowInCart = c.fetchone()
        if not rowInCart: #you are selecting an item that is not already in the cart
          c.execute('UPDATE product SET quantity=%s where pname=%s', (subtractQuantity, pname,))
          c.execute('''INSERT INTO cart (pname, productID, sumPrice, quantity) VALUES (%s, %s, %s, %s)''', (pname, productID, totPrice, quantity))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
        else: #you are adding to the quantity of an item already in cart
          c.execute('SELECT quantity, sumPrice FROM cart where pname=%s', (pname,))
          row = c.fetchone()
          quantityInCart = row[0]
          priceInCart = row[1]
          newQuantity = quantity + quantityInCart
          newPrice = totPrice + priceInCart
          c.execute('UPDATE cart SET quantity=%s, sumPrice=%s where pname=%s', (newQuantity, newPrice, pname))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
      else:
        ATCmessage = "Not enough items in stock, select fewer, " + str(quantityLeft[0]) + " albums left"

      return render_template('Pop_Albums.html', ATCmessage=ATCmessage)
  
  
  return render_template('Pop_Albums.html')
  c.close()

@app.route('/hiphop', methods=['GET','POST'])
def hiphop():
  if request.method == 'POST':
    if("UserName" not in session):
      byemessage="Please log in to see items"
      return render_template('Home_Page.html', byemessage=byemessage)

    message=""

    #receive the information about the album selected (name, quantity, price, ID)
    quantity = request.form['quantity']
    quantity = int(quantity)
    price = request.form['price']
    price = float(price)
    totPrice = (quantity * price) 
    productID = request.form['productID']
    productID = int(productID)
    pname = request.form['pname']

    c = mydb.cursor()

    #see how many are left in stock
    c.execute('SELECT quantity FROM product WHERE pname =%s', (pname,))
    quantityLeft = c.fetchone() #get the current quantity 
    SQ = quantityLeft[0] - quantity 
  
    #check if user is logged in
    if("UserName" in session):
      subtractQuantity = quantityLeft[0] - quantity 

      if(subtractQuantity >= 0): #you can make a valid purchase
        c.execute('SELECT * FROM cart where pname=%s', (pname,))
        rowInCart = c.fetchone()
        if not rowInCart: #you are selecting an item that is not already in the cart
          c.execute('UPDATE product SET quantity=%s where pname=%s', (subtractQuantity, pname,))
          c.execute('''INSERT INTO cart (pname, productID, sumPrice, quantity) VALUES (%s, %s, %s, %s)''', (pname, productID, totPrice, quantity))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
        else: #you are adding to the quantity of an item already in cart
          c.execute('SELECT quantity, sumPrice FROM cart where pname=%s', (pname,))
          row = c.fetchone()
          quantityInCart = row[0]
          priceInCart = row[1]
          newQuantity = quantity + quantityInCart
          newPrice = totPrice + priceInCart
          c.execute('UPDATE cart SET quantity=%s, sumPrice=%s where pname=%s', (newQuantity, newPrice, pname))
          ATCmessage = pname + " Added to cart, " + str(SQ) + " left in stock"
      else:
        ATCmessage = "Not enough items in stock, select fewer, " + str(quantityLeft[0]) + " albums left"

      return render_template('HipHop_Albums.html', ATCmessage=ATCmessage)
  
  return render_template('HipHop_Albums.html')
  c.close()

@app.route('/cart', methods=['GET','POST'])
def cart():
  if("UserName" not in session):
    byemessage="Please log in to see cart"
    return render_template('Cart.html', byemessage=byemessage)

  else:
    message=""
    emptyPrice=" "
    c = mydb.cursor()
    c.execute('SELECT pname, quantity, sumPrice FROM cart')
    cartRows = c.fetchall()
    c.execute('SELECT SUM(sumPrice) FROM cart')
    totalPrice = c.fetchone()
    totalPrice = (totalPrice[0])
    # totalPrice = float(round(totalPrice, 2))
    # session["totalPrice"] = totalPrice
    if(totalPrice):
      totPrice = totalPrice
    else:
      totPrice = emptyPrice
    if(not cartRows):
      message="Nothing in cart"
  
    return render_template('Cart.html', table=cartRows, byemessage=message, totalPrice=totPrice)
    c.close()

@app.route('/checkout')
def checkout():

  # clear everything in the cart
  c = mydb.cursor()
  #make sure that there are items in the cart to check out
  c.execute('SELECT COUNT(*) FROM cart')
  count = c.fetchone()[0]

  if(count == 0): #there is nothing in the cart
    header="No items to checkout"
    footer=" "
  else:
    header="Checkout Successful"
    footer="Thank's for shopping at Murray Hill Vinyl!"

    c.execute('DELETE FROM cart')
  return render_template('Checkout_Page.html', header=header, footer=footer)
  c.close()

@app.route('/remove_from_cart', methods=['GET','POST'])
def remove_from_cart():
  if request.method == 'POST':
    pname = request.form['pname']
    print(pname)
    c = mydb.cursor()
    c.execute('DELETE FROM cart WHERE pname=%s', (pname,))
    message= pname + " removed from cart"
    #now that row is deleted from cart

    #get the updated rows from cart
    emptyPrice = " "
    c.execute('SELECT pname, quantity, sumPrice FROM cart')
    cartRows = c.fetchall()
    c.execute('SELECT SUM(sumPrice) FROM cart')
    totalPrice = c.fetchone()
    totalPrice = totalPrice[0]

    if(totalPrice):
      totPrice = totalPrice
    else:
      totPrice = emptyPrice
    if(not cartRows):
      message="Nothing in cart"
    
    return render_template('Cart.html', table=cartRows, byemessage=message, totalPrice=totPrice)
    c.close()


@app.route('/edit_cart', methods=['GET','POST'])
def edit_cart():
  if request.method == "POST":
    #retreive the amount that they entered
    amountToChange = request.form['changeQuantity'] #amount they want instead
    c = mydb.cursor()
    if(int(amountToChange) <= 5):
    #if the new quantity is valid, update the quantity and pricein the cart
      pname = request.form['pname']
   
      c.execute('SELECT price FROM product WHERE pname=%s', (pname,))
      price = c.fetchone()
      price = float(price[0])
      newPrice = price * int(amountToChange)
      c.execute('UPDATE cart SET quantity=%s, sumPrice=%s where pname=%s', (amountToChange, newPrice, pname))
      #display the new table
      c.execute('SELECT pname, quantity, sumPrice FROM cart')
      cartRows = c.fetchall()
      c.execute('SELECT SUM(sumPrice) FROM cart')
      totalPrice = c.fetchone()
      totalPrice = totalPrice[0]
      message="Quantity of " + pname + " updated to " + amountToChange 
    
      return render_template('Cart.html', table=cartRows, byemessage=message, totalPrice=totalPrice)

    else:
      #if not a valid amount, give message
      message="Please choose a quantity between 1 and 5"
      c.execute('SELECT pname, quantity, sumPrice FROM cart')
      cartRows = c.fetchall()
      c.execute('SELECT SUM(sumPrice) FROM cart')
      totalPrice = c.fetchone()
      totalPrice = totalPrice[0]
  
      return render_template('Cart.html', table=cartRows, byemessage=message, totalPrice=totalPrice)
      c.close()
     


@app.route('/logout')
def logout():
  LOmessage="Logged Out"
  session.clear()
  return render_template('Home_Page.html', message = LOmessage)
  c.close()


app.run(host='0.0.0.0', port=8080)

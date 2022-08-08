from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
from datetime import date





app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'productImages'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def getCart():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'productId' not in session:
            totalCart = 0
            return "not in session."
        else:
            cart = cur.execute("SELECT * from kart")
            return cart
            
    conn.close()
    return (totalCart)


@app.route('/home')
def home():
    
    with sqlite3.connect('database.db') as conn:
        itemData,cartData,sum=fetchItemData_cardData(conn)
   
    return render_template('home.html',itemData=itemData,cartData=cartData,sum=sum)



@app.route('/stats' ,methods=['GET', 'POST'])
def stats():
    with sqlite3.connect('database.db') as conn:
        statsData = fetchMostSales(conn)
        uniqueData = fetchUniqueSales(conn)
        lastDays = fetchLastDays(conn)
    
    return render_template('stats.html',statsData=statsData,uniqueData=uniqueData,lastDays=lastDays)

def fetchMostSales(conn):
    cur = conn.cursor()
    cur.execute('SELECT name,unitsSold FROM products ORDER BY unitsSold DESC LIMIT 5')
    statsData = cur.fetchall()
    print(statsData)
    return statsData

def fetchUniqueSales(conn):
    cur = conn.cursor()
    cur.execute('SELECT name,uniquePurchase FROM products ORDER BY unitsSold DESC LIMIT 5')
    statsData = cur.fetchall()
    print(statsData)
    return statsData


def fetchLastDays(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM calendar ORDER BY Id DESC LIMIT 5')
    lastDays = cur.fetchall()
    return lastDays
    
    

def fetchItemData_cardData(con):
    
    cur = con.cursor()
    cur.execute('SELECT name,price,description,image FROM products')
    itemData = cur.fetchall()
    cur = con.cursor()
    cur.execute('SELECT name,price FROM kart')
    cartData = cur.fetchall()
    sum=0    
    for item in cartData:
        sum+=item[1]
    cartData = parse(cartData)
    itemData = parse(itemData)
    return(itemData,cartData,sum)
    

@app.route('/addToCart/',methods=['GET','POST'])
def addToCart():
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT name,price,description,image FROM products')
            itemData = cur.fetchall()
            productName = request.form['productNameAddToCart']
            productPrice = request.form['productPriceAddCart']

        itemData = parse(itemData)
        if request.method == "POST":
            with sqlite3.connect('database.db') as conn:
                try:
                    cur = conn.cursor()
                    cur.execute('''INSERT INTO kart(name,price) VALUES(?,?) ''',(productName,productPrice))
                    conn.commit()
                except:
                    print("Insert into kart failed.")
                    conn.rollback() 
        return redirect('/home')
    
@app.route('/addItem/',methods=["GET", "POST"]) 
def addItem():
    error=None
    if request.method == "POST":
            print("POST achived.")
            productName = request.form['productNameAdd']
            productDescription = request.form['descriptionAdd']
            productPrice = request.form['productPriceAdd']
            imagename = request.form['imageLinkAdd']
            
            with sqlite3.connect('database.db') as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute('''INSERT INTO products (name, price, description,image) VALUES (?,?,?,?)''',(productName,productPrice,productDescription,imagename))
                        conn.commit()
                    except:
                        message="error found, update failed."
                        print(message)
                        conn.rollback()                     
                
    
    return redirect('/')


@app.route('/checkout/',methods=["GET", "POST"]) 
def checkout():
    if request.method == "POST":
        with sqlite3.connect('database.db') as conn:
                itemData,cartData,sum=fetchItemData_cardData(conn)
                cur = conn.cursor()
                cur.execute('''DELETE from kart where productId > 0''')
                conn.commit()
                uniquePurchase(cartData)
                addProfit(sum,conn)        
    return redirect('/home')

def addProfit(sum,conn):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    cur = conn.cursor()
    cur.execute('''INSERT OR IGNORE INTO calendar(date, profit) VALUES(?, ?) ''',(today,sum))
    conn.commit()
    cur = conn.cursor()
    cur.execute ('''UPDATE calendar SET profit=profit+'''+str(sum)+''' where date = ? ''',(today,))


def uniquePurchase(order):
    unique_list = []
    general_list = []


    for products in order:
        for product in products:
            for info in product:
                res = isinstance(info, str)
                if res == True:
                    general_list.append(info)
                if info not in unique_list and res == True:
                    unique_list.append(info) 
                    break


    with sqlite3.connect('database.db') as conn:
        for products in general_list:
            try:
                products = products.lstrip()
                print(products)
                cur = conn.cursor()
                cur.execute('''UPDATE products SET unitsSold=unitsSold+1  where name = ?''',(products,))
                conn.commit()
            except:
                print("not yo")

    with sqlite3.connect('database.db') as conn:
        for products in unique_list:
            try:        
                products = products.lstrip()
                print(products)
                cur = conn.cursor()
                cur.execute('''UPDATE products SET uniquePurchase=uniquePurchase+1  where name = ?''',(products,))
                conn.commit()
                print("unique succeed")
            except:
                print("failed unique list")
            
           

    for something in unique_list:
            print(something)       
    print("done unique")
    return

   
            
@app.route("/", methods=['GET', 'POST'])
def root():
    print("route page")
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT name,price,description,image FROM products')
        itemData = cur.fetchall()
        
    itemData = parse(itemData)
    
    if request.method == "POST":
        print("POST achived.")
        oldTitle = request.form['titleUpdate']
        productName = request.form['productNameEditText']
        productDescription = request.form['description']
        productPriceUpdate = request.form['productPriceUpdate']
        productImageLink = request.form['imageLink']
        print(oldTitle)
        
        with sqlite3.connect('database.db') as conn:
                try:
                    print("old was:"+oldTitle+" new should be:"+productName)
                    cur = conn.cursor()
                    cur.execute('''UPDATE products SET name = ? , price = ?, description = ? , image = ? where name = ?''',(productName,productPriceUpdate,productDescription,productImageLink, oldTitle))
                    conn.commit()
                    message="Edit successfully."
                    print(message)
                except:
                    message="error found, update failed."
                    print(message)
                    conn.rollback()
    return render_template('admin.html',itemData=itemData)


@app.route("/delete/", methods=['POST'])
def move_forward():
    oldTitle = request.form['titleDelete']
    print("delete "+oldTitle+" please")
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        print("connected, let's delete")
        delete_query = """DELETE from products where name = ? """
        cursor.execute(delete_query,(oldTitle,))
        connection.commit()
        cursor.close()
    except:
        print("delete")    
    finally:
        if(connection):
            connection.close()
    return redirect('/')

  
def allowed_file(fileName):
    return '.' in fileName and \
            fileName.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/updateItem",methods=['GET', 'POST'])
def editItem():
    print("edit this")
    return render_template('admin.html',itemData=itemData)


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(4):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

    

if __name__ == '__main__':
    
    #app.run(host='0.0.0.0')
    app.run(debug=True)
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()

    
    

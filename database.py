import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table

conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		price REAL,
		description TEXT,
  		unitsSold INTEGER DEFAULT 0,
  		uniquePurchase INTEGER DEFAULT 0,
		image TEXT
		)''')

conn.execute('''CREATE TABLE kart
		(
		productId INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		price REAL,
		total REAL,
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')



conn.execute('''CREATE TABLE calendar
            (Id INTEGER PRIMARY KEY AUTOINCREMENT,
			date TEXT,
  			profit INTEGER,
         	UNIQUE(date)
             )''')

conn.close()


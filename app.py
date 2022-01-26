from flask import Flask, render_template      
import pyodbc
import os
from dotenv import load_dotenv
  
app = Flask(__name__)  
load_dotenv()
server_name = os.environ.get("SQL_SERVER_NAME")
database_name = os.environ.get("SQL_DATABASE_NAME")
username = os.environ.get("SQL_USERNAME")
password = os.environ.get("SQL_PASSWORD")
storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
 
def get_data():
    try:
        connection_string = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{server_name}.database.windows.net,1433;Database={database_name};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        cursor.execute("SELECT id, name, description, imageUrl FROM Product.Products") 

        rows = cursor.fetchall()

        products = [{
            'id': row[0], 
            'name': row[1], 
            'description': row[2], 
            'imageUrl': f'https://{storage_account_name}.blob.core.windows.net/{row[3]}' 
            } for row in rows]
        return products
    except:
        return None

@app.route('/')   
def home():  
    return render_template("home.html")

@app.route('/produktai')   
def products(): 

    products = get_data()

    if products ==None:
        return render_template("nothing.html")

    return render_template("products.html", products = products)

@app.route('/produktas/<id>')
def product(id):
    
    try:
        product_id = int(id)
    except ValueError:
        return render_template("404.html")

    products = get_data()

    product = next(filter(lambda product: product['id'] == product_id, products), None)

    if (product):
        return render_template("product_details.html", product = product)
    
    return render_template("404.html")

@app.route('/statusas')   
def status():  
    if (not server_name or not database_name or
        not username or not password or not storage_account_name):
       return {'žinutė': 'Trūksta aplinkos parametrų'} 

    try: 
        products = get_data()
    except Exception as ex: 
        return {'žinutė': 'Klaida jungiantis prie DB', 'klaida': str(ex)} 

    if not products:
        return {'žinutė': 'Trūksta duomenų'} 

    return {'žinutė': 'Viskas veikia!'}

@app.errorhandler(404)
def handle_404(e):
    return render_template("404.html")

if __name__ =='__main__':  
    app.run(debug = True)  
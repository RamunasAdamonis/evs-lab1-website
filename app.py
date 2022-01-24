from flask import Flask, render_template       
  
app = Flask(__name__)  
 
@app.route('/')   
def home():  
    return render_template("home.html")

@app.route('/products')   
def products(): 
    products = [{'id': 1, 'name': 'vardas', 'description': 'aprasymas'}] 
    return render_template("products.html", products = products)
  
if __name__ =='__main__':  
    app.run(debug = True)  
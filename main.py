#we import the flask class and the render template function to help us load html functions

from flask import Flask,render_template,request,redirect

import psycopg2
app= Flask(__name__)
#conn=psycopg2.connect(user="postgres",password="pucci2020", host="127.0.0.1",port="5432",database="myduka")
conn=psycopg2.connect(user="yevcxsepulljbn",password="db10b3e7c871f33c71d8783442b4ce718a073cc489cf445b8d20850ec46fee37", host="ec2-3-248-121-12.eu-west-1.compute.amazonaws.com",port="5432",database="d1mg4difddp615")

#declare a cursor used to navigate in the database
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY,name VARCHAR(100),buying_price INT,selling_price INT,stock_quantity INT);") 
cur.execute("CREATE TABLE IF NOT EXISTS sales (sales_id serial PRIMARY KEY,id INT, quality INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), FOREIGN KEY(id) REFERENCES products(id) ON DELETE CASCADE);") 
conn.commit()


#html for home route (landing page)
@app.route("/")

def home ():
    #return html file
         hello="hello world"
         return render_template("index.html",h=hello)
         
#products
@app.route("/products")
def products():
    cur.execute("select * FROM products")
    products=cur.fetchall()
    print(products)
    return render_template("products.html",products=products)

#sales
@app.route("/sales")
def sales():
    cur.execute("select * FROM sales")
    sales=cur.fetchall()
    print(sales)
    return render_template("sales.html",sales=sales)

#dashboard
@app.route("/dashboard")
def dashboard ():
        cur.execute("""select sum((products.selling_price-products.buying_price)*sales.quality) as profit, products.name from sales 
        join products on products.id=sales.id
        GROUP BY products.name""")
        graph=cur.fetchall()
        product_names=[]

        profits=[]
        for tpl in graph:
            product_names.append(tpl[1])
        print(product_names)
        for tpl in graph:
            profits.append(tpl[0])
        print(profits)
        print(graph)
        return render_template("dashboard.html",profits=profits,product_names=product_names)
        

#sales for specific product
@app.route("/sale/<int:id>")
def salesspec(id):
    x=id
    cur.execute("""select * from sales where id=%(id)s""", {"id": x})
    sales=cur.fetchall()
    return render_template("sales.html",sales=sales)


#formroute
@app.route('/formdata',methods= ['POST','GET']) 
def form():
           if request.method == 'GET':
               return render_template("form.html") 
           else: 
               prod_name = request.form['fname']
               quant = request.form['lname']
               print(prod_name)
               print(quant)
               return redirect ("/formdata")

#productformroute
@app.route('/productdata',methods= ['POST','GET']) 
def prodform():
           if request.method == 'GET':
               return render_template("products.html") 
           else: 
            
               pr_name = request.form['prname']
               q_name = request.form['qname']
               cat_name = request.form['catname']
               bp_name = request.form['bpname']
               sp_name = request.form['spname']
               
               print(pr_name)
               print(q_name)
               print(cat_name)
               print(bp_name)
               print(sp_name)
               cur.execute("""INSERT INTO products (id,buying_price,selling_price,stock_quantity) VALUES(%(n)s,%(bp)s,%(sp)s,%(st)s)""",
               {"n":pr_name,"bp":q_name,"sp":cat_name,"st":bp_name})           
               conn.commit()
               return redirect ("/products")
              

#salesformroute
@app.route('/saledata',methods= ['POST','GET']) 
def saleform():
           if request.method == 'GET':
                  cur.execute("select * FROM sales")
                  sales=cur.fetchall()
                  print(sales)
                  return render_template("sales.html",sales=sales)


           else: 
               p_id=request.form['Item-id'] 
               q_name = request.form['qnae']            
               print(q_name)

               cur.execute("""INSERT INTO sales (id,quality) VALUES(%(id)s,%(qu)s)""",
               {"id":p_id,"qu":q_name})           

 
               conn.commit()
               return redirect ("/products")
                          
app.run()



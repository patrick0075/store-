from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

@get("/admin")
def admin_portal():
	return template("pages/admin.html")



@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

connection = pymysql.connect(host = "localhost",
                             user = "root",
                             password = "gtowc",
                             db="store",
                             charset="utf8",
                             cursorclass = pymysql.cursors.DictCursor)

@get('/categories')
def get_categories():
    try:
        with connection.cursor() as cursor:
            sql = "select * from category"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS":"SUCCESS","CATEGORIES":result,"code":200})
    except Exception as e:
        print(e)
        return json.dumps({"STATUS":"ERROR","MSG":"internal error","code":500})

@post('/category')
def create_Category():
    try:
        with connection.cursor() as cursor:
            name = request.POST.get("name")
            sql = "INSERT INTO categories VALUES (0,'{0}')".format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "200"})
    except Exception as e:
        print (repr(e))
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

@get('/products')
def get_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Products"
            cursor.execute(sql)
            result = cursor.fetchall()
            status = "success"
            msg = ""
            print "success code -200"

    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg, "PRODUCTS": products}
    return json.dumps(result)



@get("/category/<id>/products")
def list_products_cat(id):
    print"inside cat"
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM products WHERE category=("{}")' .format(id)
            cursor.execute(sql)
            products = cursor.fetchall()
            connection.commit()
            status = "success"
            msg=""
            print "success code - 200"

    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg, "PRODUCTS":products}
    return json.dumps(result)






@post('/product')
def update_product():
    id = request.POST.get("id")
    name = request.POST.get("title")
    description = request.POST.get("description")
    price = request.POST.get("price")
    image = request.POST.get("img_url")
    category = request.POST.get("category")
    favorite = 1 if request.POST.get("favorite") == "on" else 0
    try:
        with connection.cursor() as cursor:
            if id == "":
                sql = "insert into products values(0, '{}', '{}', {}, '{}', '{}', {})".format(name, description, price, image, category, favorite)
            else:
                sql = "update products set title = '{}', description = '{}', price = {}, img_url = '{}', category = {}, favorite = {} where id = {}".format(name, description, price, image, category, favorite, id)
            cursor.execute(sql)
            connection.commit()
            prod_id = cursor.lastrowid
            return json.dumps({"STATUS": "SUCCESS", "PRODUCT_ID": prod_id, "CODE": 201,
                               "MSG": "Product Created / Updated Successfully"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "CODE": 500, "MSG": repr(e)})



@delete("/category/<id>")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id = {}".format(id)
            cursor.execute(sql)
            sqla = "DELETE FROM products where category = {}".format(id)
            cursor.execute(sqla)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was deleted successfully", "CODE": "200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "The category was not deleted due to an error", "CODE": "500"})

@get('/product/<id>')
def get_Products(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products WHERE id = {0}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

@delete("/product/<id>")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products where id = {}".format(id)
            cursor.execute(sql)
        return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": "The product was deleted successfully", "CODE": "200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "The product was not deleted due to an error", "CODE": "500"})


def main():
    run(host='localhost', port=8000)

if __name__=='__main__':
    main()

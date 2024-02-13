from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
import sqlite3
from django.http import JsonResponse
import json

def validate_user_credentials(username, password):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    select_statement = """
    SELECT password FROM myapp_user WHERE username = ?;
    """
    cursor.execute(select_statement, (username,))
    row = cursor.fetchone()
    if row is not None:
        hashed_password = row[0]
        # Here, you would typically compare the hashed_password with the provided password
        # For demonstration purposes, we'll print the hashed password
        print("Retrieved hashed password:", hashed_password)
        if hashed_password==password:
            return True
        else:
            return False
        # Check if the provided password matches the hashed password (you'll need to use Django's check_password)
        # if password_matches:
        #     return True  # Credentials are valid
    else:
        print("User not found")  # User does not exist in the database
        return False

    # Close the cursor and connection
    cursor.close()
    conn.close()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = validate_user_credentials(username=username, password=password)
        print("user",user)
        if user:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            select_statement = "SELECT count(*) FROM myapp_category;"
            cursor.execute(select_statement)
            num_categories = cursor.fetchone()[0]
            select_statement = "SELECT count(*) FROM myapp_items;"
            cursor.execute(select_statement)
            num_items = cursor.fetchone()[0]
            select_statement = "SELECT name FROM myapp_category;"
            cursor.execute(select_statement)
            cat = cursor.fetchall()
            categories=[]
            for cate in cat:
                categories.append(cate[0])
            select_statement = "SELECT * FROM myapp_items;"
            cursor.execute(select_statement)
            temp = cursor.fetchall()
            #print("temp",temp)
            items = []
            cols=['sku','name','tags','description','price','in_stock','net_stock','available_stock','quantity_sold_this_month','quantity_sold_last_month','user','category']
            for i in temp:
                dict_temp={}
                for j in range(len(cols)):
                    dict_temp[cols[j]]=i[j+1]
                items.append(dict_temp)

            """
            context = {
                'total_categories': num_categories,
                'total_items': num_items,
            }
            print(num_items,num_categories)
            """

            # Store total_categories and total_items in session
            request.session['total_categories'] = num_categories
            request.session['total_items'] = num_items
            request.session['categories'] = categories
            request.session['items'] = items
            request.session['username'] = username
            cursor.close()
            conn.close()
            return redirect('dashboard')  # Redirect to dashboard upon successful login
            #return render(request, 'dashboard.html', context)
        else:
            messages.error(request, 'Incorrect username or password.')  # Display error message
            return redirect('login')  # Redirect back to login page
    else:
        return render(request, 'login.html')


def dashboard_view(request):
    total_categories = [request.session.get('total_categories', 0)]  # Convert to list
    total_items = [request.session.get('total_items', 0)]  # Convert to list
    categories = request.session.get('categories', [])  # Use empty list as default value
    items = request.session.get('items', [])  # Use empty list as default value
    username = request.session.get('username', '')  # Use empty string as default value
    context = {
        'total_categories': total_categories,
        'total_items': total_items,
        'categories': categories,
        'items': items,
        'username': username
    }
    return render(request, 'dashboard.html', context)


def registration_view(request):
    # Render the registration template
    return render(request, 'registration.html')

def is_username_exists(username):
    #print("un",username)
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    select_statement = "SELECT count(*) FROM myapp_user WHERE username = ?"
    cursor.execute(select_statement, (username,))
    row = cursor.fetchone()
    count = row[0]
    #print("unmame",uname)
    cursor.close()
    conn.close()
    return count>0

def check_username_availability(request):
    if request.method == 'POST':
        #print(request.POST)
        #print(request.body)
        data = json.loads(request.body)
        username = data.get('username')
        #print("1un",username)
        if is_username_exists(username):
            return JsonResponse({'is_taken': True})
        else:
            return JsonResponse({'is_taken': False})
def create_account(request):
    if request.method == 'POST':
        post_request = request.POST
        first_name = post_request['first_name']
        last_name = post_request['last_name']
        email = post_request['email']
        username = post_request['username']
        password = post_request['password']
        business_name = post_request['business_name']
        phone_number = post_request['phone_number']
        country = post_request['country']
        nature_of_operations = post_request['nature_of_operations']
        membership = post_request['membership']
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        insert_statement = "INSERT INTO myapp_user values(?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert_statement, (password,email,business_name,country,first_name,last_name,membership,nature_of_operations,phone_number,username))
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({'success': True})
def reset_password(request):
    return render(request, 'reset_password.html')

def create_category(request):
    if request.method == "POST":
        post_request = request.POST
        name = request.POST.get("name")
        parent = request.POST.get("parent")
        description=''
        keywords=''
        default_location=''
        if 'description' in post_request.keys():
            description = request.POST.get("description")
        if 'keywords' in post_request.keys():
            keywords = request.POST.get("keywords")
        if 'default-location' in post_request.keys():
            default_location = request.POST.get("default-location")
        #print(name,parent,default_location,description,keywords)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        insert_statement = "insert into myapp_category values(?,?,?,?,?)"
        cursor.execute(insert_statement, (name,description,keywords,default_location,parent))
        conn.commit()
        select_statement = "SELECT count(*) FROM myapp_category;"
        cursor.execute(select_statement)
        num_categories = cursor.fetchone()[0]
        print("number",num_categories)
        cursor.close()
        conn.close()
        #request.session['total_categories'] = num_categories
        updated_data = {
            'total_categories': num_categories
        }
        return JsonResponse(updated_data)
        #return redirect('dashboard')
        #return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

def check_category_name(request):
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET['name']
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        select_statement = "SELECT name FROM myapp_category;"
        cursor.execute(select_statement)
        row = cursor.fetchall()
        names=[]
        for r in row:
            names.append(r[0])
        if name in names:
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request'})

def add_item(request):
    if request.method == "POST":
        post_request = request.POST
        sku=post_request['sku']
        name=post_request['name']
        tags=post_request['tags']
        desc=post_request['description']
        cat=post_request['category']
        price=post_request['price']
        instock=post_request['instock']
        netstock=post_request['netstock']
        avstock=post_request['availablestock']
        username=post_request['username']
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        insert_statement = "insert into myapp_items('sku','name','tags','description','price','in_stock','net_stock','available_stock','user_id','category_id') values(?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert_statement, (sku,name,tags,desc,price,instock,netstock,avstock,username,cat))
        conn.commit()
        select_statement = "SELECT count(*) FROM myapp_category;"
        cursor.execute(select_statement)
        num_categories = cursor.fetchone()[0]
        select_statement = "SELECT count(*) FROM myapp_items;"
        cursor.execute(select_statement)
        num_items = cursor.fetchone()[0]
        select_statement = "SELECT name FROM myapp_category;"
        cursor.execute(select_statement)
        cat = cursor.fetchall()
        categories = []
        for cate in cat:
            categories.append(cate[0])
        select_statement = "SELECT * FROM myapp_items;"
        cursor.execute(select_statement)
        temp = cursor.fetchall()
        #print("temp", temp)
        items = []
        cols = ['sku', 'name', 'tags', 'description', 'price', 'in_stock', 'net_stock', 'available_stock',
                'quantity_sold_this_month', 'quantity_sold_last_month', 'user', 'category']
        for i in temp:
            dict_temp = {}
            for j in range(len(cols)):
                dict_temp[cols[j]] = i[j + 1]
            items.append(dict_temp)
        cursor.close()
        conn.close()
        """
        # Store total_categories and total_items in session
        request.session['total_categories'] = num_categories
        request.session['total_items'] = num_items
        request.session['categories'] = categories
        request.session['items'] = items
        request.session['username'] = username
        return redirect('dashboard')"""

        updated_data = {
            'total_categories': num_categories,
            'total_items': num_items,
            'categories': categories,
            'items': items,
            'username': username

        }
        return JsonResponse(updated_data)
        #return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

def your_search_view(request):
    if request.method == 'GET':
        name = request.GET['search']
        print("name",name)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        select_statement = "SELECT count(*) FROM myapp_category;"
        cursor.execute(select_statement)
        num_categories = cursor.fetchone()[0]
        select_statement = "SELECT count(*) FROM myapp_items;"
        cursor.execute(select_statement)
        num_items = cursor.fetchone()[0]
        select_statement = "SELECT name FROM myapp_category;"
        cursor.execute(select_statement)
        cat = cursor.fetchall()
        categories = []
        for cate in cat:
            categories.append(cate[0])
        select_statement = "SELECT * FROM myapp_items where name=?;"
        cursor.execute(select_statement,(name,))
        temp = cursor.fetchall()
        items = []
        cols = ['sku', 'name', 'tags', 'description', 'price', 'in_stock', 'net_stock', 'available_stock',
                'quantity_sold_this_month', 'quantity_sold_last_month', 'user', 'category']
        if temp!=[]:
            for i in temp:
                dict_temp = {}
                for j in range(len(cols)):
                    dict_temp[cols[j]] = i[j + 1]
                items.append(dict_temp)
        """
        request.session['total_categories'] = num_categories
        request.session['total_items'] = num_items
        request.session['categories'] = categories
        request.session['items'] = items
        return redirect('dashboard')"""
        cursor.close()
        conn.close()
        updated_data = {
            'total_categories': num_categories,
            'total_items': num_items,
            'categories': categories,
            'items': items,

        }
        return JsonResponse(updated_data)
    else:
        return JsonResponse({'error': 'Invalid request'})
def your_filter_view(request):
    if request.method == 'GET':
        print("req",request.GET)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        category = request.GET.get('category', '')
        name = request.GET.get('name', '')
        sku = request.GET.get('sku', '')
        if category!='' and name!='' and sku!='':
            select_statement = "SELECT * FROM myapp_items where name=? and category=? and sku=?;"
            cursor.execute(select_statement,(name,category,sku))
        elif name!='' and sku!='':
            select_statement = "SELECT * FROM myapp_items where name=? and sku=?;"
            cursor.execute(select_statement, (name, sku))
        elif category!='' and sku!='':
            select_statement = "SELECT * FROM myapp_items where category=? and sku=?;"
            cursor.execute(select_statement, (category, sku))
        elif name!='' and category!='':
            select_statement = "SELECT * FROM myapp_items where name=? and category=?;"
            cursor.execute(select_statement, (name, category))
        elif name!='':
            select_statement = "SELECT * FROM myapp_items where name=?;"
            cursor.execute(select_statement, (name,))
        elif sku!='':
            select_statement = "SELECT * FROM myapp_items where sku=?;"
            cursor.execute(select_statement, (sku,))
        elif category!='':
            select_statement = "SELECT * FROM myapp_items where category=?;"
            cursor.execute(select_statement, (category,))
        temp = cursor.fetchall()
        items = []
        cols = ['sku', 'name', 'tags', 'description', 'price', 'in_stock', 'net_stock', 'available_stock',
                'quantity_sold_this_month', 'quantity_sold_last_month', 'user', 'category']
        if temp != []:
            for i in temp:
                dict_temp = {}
                for j in range(len(cols)):
                    dict_temp[cols[j]] = i[j + 1]
                items.append(dict_temp)
        select_statement = "SELECT count(*) FROM myapp_category;"
        cursor.execute(select_statement)
        num_categories = cursor.fetchone()[0]
        select_statement = "SELECT count(*) FROM myapp_items;"
        cursor.execute(select_statement)
        num_items = cursor.fetchone()[0]
        select_statement = "SELECT name FROM myapp_category;"
        cursor.execute(select_statement)
        cat = cursor.fetchall()
        categories = []
        for cate in cat:
            categories.append(cate[0])


        """
        request.session['total_categories'] = num_categories
        request.session['total_items'] = num_items
        request.session['categories'] = categories
        request.session['items'] = items
        return redirect('dashboard')"""
        cursor.close()
        conn.close()
        updated_data = {
            'total_categories': num_categories,
            'total_items': num_items,
            'categories': categories,
            'items': items,
        }
        return JsonResponse(updated_data)
    else:
        return JsonResponse({'error': 'Invalid request'})


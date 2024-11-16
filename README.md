# Inventory Management Django App

This is a simple inventory management system built with Django and MySQL. It allows users to perform CRUD (Create, Read, Update, Delete) operations on products.

## Features

- Add new products
- View a list of all products
- Edit existing products
- Delete products

## Prerequisites

- Python 3.x
- Django
- MySQL

## Installation

### Step 1: Set Up the Environment

1. **Install Python and Django**:
   Ensure you have Python installed. Install Django using pip:
   ```bash
   pip install django
   ```

2. **Install MySQL and MySQL Client**:
   Install MySQL on your system. Then, install the MySQL client for Python:
   ```bash
   pip install mysqlclient
   ```

### Step 2: Create a Django Project

1. **Create a Django Project**:
   Use the `django-admin` command to create a new project:
   ```bash
   django-admin startproject inventory_management
   cd inventory_management
   ```

2. **Create a Django App**:
   Create a new app within the project:
   ```bash
   python manage.py startapp inventory
   ```

### Step 3: Configure MySQL Database

1. **Create a MySQL Database**:
   Log in to your MySQL server and create a new database:
   ```sql
   CREATE DATABASE inventory_db;
   ```

2. **Configure Database Settings**:
   Update the `DATABASES` setting in `inventory_management/settings.py` to use MySQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'inventory_db',
           'USER': 'your_mysql_user',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### Step 4: Define Models

1. **Create Models**:
   Define the models for your inventory app in `inventory/models.py`:
   ```python
   from django.db import models

   class Product(models.Model):
       name = models.CharField(max_length=100)
       description = models.TextField()
       price = models.DecimalField(max_digits=10, decimal_places=2)
       quantity = models.IntegerField()

       def __str__(self):
           return self.name
   ```

2. **Apply Migrations**:
   Create and apply migrations to create the database tables:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Step 5: Create Views and Templates

1. **Create Views**:
   Define views for listing, adding, editing, and deleting products in `inventory/views.py`:
   ```python
   from django.shortcuts import render, get_object_or_404, redirect
   from .models import Product
   from .forms import ProductForm

   def product_list(request):
       products = Product.objects.all()
       return render(request, 'inventory/product_list.html', {'products': products})

   def product_create(request):
       if request.method == 'POST':
           form = ProductForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('product_list')
       else:
           form = ProductForm()
       return render(request, 'inventory/product_form.html', {'form': form})

   def product_update(request, pk):
       product = get_object_or_404(Product, pk=pk)
       if request.method == 'POST':
           form = ProductForm(request.POST, instance=product)
           if form.is_valid():
               form.save()
               return redirect('product_list')
       else:
           form = ProductForm(instance=product)
       return render(request, 'inventory/product_form.html', {'form': form})

   def product_delete(request, pk):
       product = get_object_or_404(Product, pk=pk)
       if request.method == 'POST':
           product.delete()
           return redirect('product_list')
       return render(request, 'inventory/product_confirm_delete.html', {'product': product})
   ```

2. **Create Forms**:
   Create a form for the `Product` model in `inventory/forms.py`:
   ```python
   from django import forms
   from .models import Product

   class ProductForm(forms.ModelForm):
       class Meta:
           model = Product
           fields = ['name', 'description', 'price', 'quantity']
   ```

3. **Create Templates**:
   Create HTML templates for listing, adding, editing, and deleting products in `inventory/templates/inventory/`:
   - `product_list.html`:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>Product List</title>
     </head>
     <body>
         <h1>Product List</h1>
         <a href="{% url 'product_create' %}">Add Product</a>
         <ul>
             {% for product in products %}
                 <li>{{ product.name }} - <a href="{% url 'product_update' product.pk %}">Edit</a> - <a href="{% url 'product_delete' product.pk %}">Delete</a></li>
             {% endfor %}
         </ul>
     </body>
     </html>
     ```

   - `product_form.html`:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>Product Form</title>
     </head>
     <body>
         <h1>Product Form</h1>
         <form method="post">
             {% csrf_token %}
             {{ form.as_p }}
             <button type="submit">Save</button>
         </form>
     </body>
     </html>
     ```

   - `product_confirm_delete.html`:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>Confirm Delete</title>
     </head>
     <body>
         <h1>Are you sure you want to delete {{ product.name }}?</h1>
         <form method="post">
             {% csrf_token %}
             <button type="submit">Yes, delete</button>
         </form>
         <a href="{% url 'product_list' %}">Cancel</a>
     </body>
     </html>
     ```

### Step 6: Configure URLs

1. **Update App URLs**:
   Define URL patterns for the inventory app in `inventory/urls.py`:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.product_list, name='product_list'),
       path('create/', views.product_create, name='product_create'),
       path('update/<int:pk>/', views.product_update, name='product_update'),
       path('delete/<int:pk>/', views.product_delete, name='product_delete'),
   ]
   ```

2. **Include App URLs in Project URLs**:
   Include the inventory app URLs in the main project `urls.py`:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('products/', include('inventory.urls')),
   ]
   ```

### Step 7: Run the Server

1. **Run the Development Server**:
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000/products/` to see the product list and perform CRUD operations.

## Summary

- **Project Setup**: Installed Django and MySQL client, created a Django project and app.
- **Database Configuration**: Configured MySQL as the database backend.
- **Models**: Defined the `Product` model.
- **Views**: Created views for listing, adding, editing, and deleting products.
- **Forms**: Created a form for the `Product` model.
- **Templates**: Created HTML templates for the views.
- **URLs**: Configured URL patterns for the app and included them in the project URLs.
- **Run Server**: Started the development server and accessed the application.



### Project Structure

```
inventory_management/
├── inventory_management/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── inventory/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   │   ├── __init__.py
│   ├── models.py
│   ├── templates/
│   │   ├── inventory/
│   │   │   ├── product_confirm_delete.html
│   │   │   ├── product_form.html
│   │   │   ├── product_list.html
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── manage.py
├── venv/
│   ├── ...
├── README.md
```

### Explanation

- **inventory_management/**: The main project directory.
  - **inventory_management/**: The project configuration directory.
    - `__init__.py`: Initializes the package.
    - `asgi.py`: ASGI configuration.
    - `settings.py`: Project settings.
    - `urls.py`: Project URL configuration.
    - `wsgi.py`: WSGI configuration.
  - **inventory/**: The inventory app directory.
    - `__init__.py`: Initializes the package.
    - `admin.py`: Admin configuration.
    - `apps.py`: App configuration.
    - `forms.py`: Forms for the app.
    - **migrations/**: Database migrations.
      - `__init__.py`: Initializes the package.
    - `models.py`: Data models.
    - **templates/**: HTML templates.
      - **inventory/**: Templates specific to the inventory app.
        - `product_confirm_delete.html`: Template for confirming product deletion.
        - `product_form.html`: Template for product form.
        - `product_list.html`: Template for listing products.
    - `tests.py`: Tests for the app.
    - `urls.py`: URL configuration for the app.
    - `views.py`: Views for the app.
  - `manage.py`: Django's command-line utility.
  - **venv/**: Virtual environment directory (not included in version control).
  - README.md: Project documentation.
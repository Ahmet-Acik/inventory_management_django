from django.test import TestCase
from .models import Product
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(
            name="Test Product",
            description="A product for testing.",
            price=9.99,
            quantity=5
        )

    def test_product_str(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(str(product), "Test Product")

    
    def test_product_fields(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.description, "A product for testing.")
        self.assertEqual(product.price, Decimal('9.99'))  # Fix here
        self.assertEqual(product.quantity, 5)
        
from django.urls import reverse

class ProductViewTest(TestCase):
    def setUp(self):
        Product.objects.create(
            name="View Product",
            description="View test.",
            price=Decimal('5.00'),
            quantity=2
        )


    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Product")
 
        
    def test_product_create_view(self):
        response = self.client.post(reverse('product_create'), {
            'name': 'Created Product',
            'description': 'Created via view.',
            'price': '7.50',
            'quantity': 3
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Product.objects.filter(name='Created Product').exists())

    
    def test_product_update_view(self):
        product = Product.objects.get(name="View Product")
        response = self.client.post(reverse('product_update', args=[product.id]), {
            'name': 'Updated Product',
            'description': 'Updated description.',
            'price': '10.00',
            'quantity': 4
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Product')
        self.assertEqual(product.description, 'Updated description.')
        self.assertEqual(product.price, Decimal('10.00'))
        self.assertEqual(product.quantity, 4)
        
        
    def test_product_update_view2(self):
        product = Product.objects.create(
            name="Update Product",
            description="Update test.",
            price=Decimal('10.00'),
            quantity=1
        )
        response = self.client.post(reverse('product_update', args=[product.pk]), {
            'name': 'Updated Product',
            'description': 'Updated via view.',
            'price': '12.00',
            'quantity': 4
        })
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Product')
        self.assertEqual(product.price, Decimal('12.00'))


    def test_product_delete_view(self):
        product = Product.objects.get(name="View Product")
        response = self.client.post(reverse('product_delete', args=[product.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Product.objects.filter(name="View Product").exists())

from .forms import ProductForm

class ProductFormTest(TestCase):
    def test_invalid_price(self):
        form = ProductForm(data={
            'name': 'Invalid Product',
            'description': 'Negative price',
            'price': '-1.00',
            'quantity': 1
        })
        self.assertFalse(form.is_valid())
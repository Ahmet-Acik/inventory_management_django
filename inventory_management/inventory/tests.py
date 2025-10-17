from django.test import TestCase
from .models import Product
from .forms import ProductForm
from decimal import Decimal
from .forms import ProductForm
from django.urls import reverse
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):

    def setUp(self):
        Product.objects.create(
            name="Test Product",
            description="A product for testing.",
            price=9.99,
            quantity=5,
        )

    def test_negative_quantity_model(self):
        product = Product(
            name="Negative Quantity",
            description="Should fail",
            price=Decimal("1.00"),
            quantity=-1,
        )
        with self.assertRaises(Exception):
            product.full_clean()

    def test_str_method_empty_name(self):
        product = Product(
            name="", description="No name", price=Decimal("1.00"), quantity=1
        )
        self.assertEqual(str(product), "")

    def test_negative_price_model(self):
        product = Product(
            name="Negative Price",
            description="Should fail",
            price=Decimal("-1.00"),
            quantity=1,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_zero_price_and_quantity(self):
        product = Product.objects.create(
            name="Zero Product",
            description="Zero values",
            price=Decimal("0.00"),
            quantity=0,
        )
        self.assertEqual(product.price, Decimal("0.00"))
        self.assertEqual(product.quantity, 0)

    def test_max_length_name(self):
        name = "A" * 100  # max_length is 100
        product = Product.objects.create(
            name=name, description="Max length name", price=Decimal("1.00"), quantity=1
        )
        self.assertEqual(product.name, name)

    def test_missing_required_fields(self):
        product = Product(description="Missing name", price=Decimal("1.00"), quantity=1)
        with self.assertRaises(Exception):
            product.full_clean()  # This will raise a ValidationError

    def test_product_str(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(str(product), "Test Product")

    def test_product_fields(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.description, "A product for testing.")
        self.assertEqual(product.price, Decimal("9.99"))  # Fix here
        self.assertEqual(product.quantity, 5)


class ProductViewTest(TestCase):
    def setUp(self):
        Product.objects.create(
            name="View Product",
            description="View test.",
            price=Decimal("5.00"),
            quantity=2,
        )

    def test_product_list_view(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Product")
        self.assertTemplateUsed(response, "inventory/product_list.html")

    def test_product_create_view(self):
        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Created Product",
                "description": "Created via view.",
                "price": "7.50",
                "quantity": 3,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Product.objects.filter(name="Created Product").exists())
        # Check redirect location
        self.assertRedirects(response, reverse("product_list"))

    def test_product_update_view(self):
        product = Product.objects.get(name="View Product")
        response = self.client.post(
            reverse("product_update", args=[product.pk]),
            {
                "name": "Updated Product",
                "description": "Updated description.",
                "price": "10.00",
                "quantity": 4,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after update
        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Product")
        self.assertEqual(product.description, "Updated description.")
        self.assertEqual(product.price, Decimal("10.00"))
        self.assertEqual(product.quantity, 4)

    def test_product_update_view2(self):
        product = Product.objects.create(
            name="Update Product",
            description="Update test.",
            price=Decimal("10.00"),
            quantity=1,
        )
        response = self.client.post(
            reverse("product_update", args=[product.pk]),
            {
                "name": "Updated Product",
                "description": "Updated via view.",
                "price": "12.00",
                "quantity": 4,
            },
        )
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Product")
        self.assertEqual(product.price, Decimal("12.00"))

    def test_product_delete_view(self):
        product = Product.objects.get(name="View Product")
        response = self.client.post(reverse("product_delete", args=[product.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Product.objects.filter(name="View Product").exists())
        self.assertRedirects(response, reverse("product_list"))


class ProductFormTest(TestCase):
    def test_negative_price(self):
        form = ProductForm(
            data={
                "name": "Test Product",
                "description": "Test negative price",
                "price": -1,
                "quantity": 1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_negative_quantity(self):
        form = ProductForm(
            data={
                "name": "Test Product",
                "description": "Test negative quantity",
                "price": 1,
                "quantity": -1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)

    def test_missing_name(self):
        form = ProductForm(data={"description": "No name", "price": 1, "quantity": 1})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_valid_form(self):
        form = ProductForm(
            data={
                "name": "Valid Product",
                "description": "All fields valid.",
                "price": 10,
                "quantity": 5,
            }
        )
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.name, "Valid Product")
        self.assertEqual(product.description, "All fields valid.")
        self.assertEqual(product.price, Decimal("10"))
        self.assertEqual(product.quantity, 5)

    def test_zero_quantity(self):
        form = ProductForm(
            data={
                "name": "Zero Quantity Product",
                "description": "Testing zero quantity.",
                "price": 5,
                "quantity": 0,
            }
        )
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.quantity, 0)

    def test_zero_price(self):
        form = ProductForm(
            data={
                "name": "Zero Price Product",
                "description": "Testing zero price.",
                "price": 0,
                "quantity": 10,
            }
        )
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.price, Decimal("0"))

    def test_large_quantity(self):
        form = ProductForm(
            data={
                "name": "Large Quantity Product",
                "description": "Testing large quantity.",
                "price": 15,
                "quantity": 1000000,
            }
        )
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.quantity, 1000000)

    def test_large_price(self):
        form = ProductForm(
            data={
                "name": "Large Price Product",
                "description": "Testing large price.",
                "price": 9999999.99,
                "quantity": 10,
            }
        )
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.price, Decimal("9999999.99"))

    def test_whitespace_name(self):
        form = ProductForm(
            data={
                "name": "   ",
                "description": "Whitespace name.",
                "price": 10,
                "quantity": 5,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_zero_price_and_quantity(self):
        form = ProductForm(
            data={
                "name": "Zero Product",
                "description": "Zero values",
                "price": 0,
                "quantity": 0,
            }
        )
        self.assertTrue(form.is_valid())

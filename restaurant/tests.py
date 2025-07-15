from django.test import TestCase
from .models import YourModel  # Replace with your actual model

class YourModelTestCase(TestCase):
    def setUp(self):
        # Set up any initial data for your tests here
        YourModel.objects.create(name="Test Item", description="This is a test item.")

    def test_model_creation(self):
        """Test that the model is created correctly."""
        item = YourModel.objects.get(name="Test Item")
        self.assertEqual(item.description, "This is a test item.")

    def test_model_str(self):
        """Test the string representation of the model."""
        item = YourModel.objects.get(name="Test Item")
        self.assertEqual(str(item), "Test Item")  # Adjust based on your model's __str__ method
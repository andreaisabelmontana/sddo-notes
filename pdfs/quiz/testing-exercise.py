"""
Python Testing Fundamentals - Practical Exercise (Student Version)
===================================================================

This exercise covers:
1. Unit Testing with unittest and pytest
2. Integration Testing
3. Mocking external dependencies
4. Patching functions and methods

Setup:
------
pip install pytest pytest-mock requests --break-system-packages

Run tests:
----------
pytest testing_exercise_student.py -v
or
python -m pytest testing_exercise_student.py -v
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime


# ============================================================================
# PART 1: Simple Functions for Unit Testing
# ============================================================================

def calculate_total_price(price: float, quantity: int, discount_percent: float = 0) -> float:
    """
    Calculate total price with optional discount.
    
    Args:
        price: Unit price
        quantity: Number of items
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Total price after discount
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    subtotal = price * quantity
    discount_amount = subtotal * (discount_percent / 100)
    return subtotal - discount_amount


def validate_email(email: str) -> bool:
    """Simple email validation."""
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    username, domain = parts
    if not username or not domain or '.' not in domain:
        return False
    
    return True


# ============================================================================
# PART 2: Classes for Integration Testing
# ============================================================================

class Database:
    """Simulated database connection."""
    
    def __init__(self):
        self.data = {}
        self.connected = False
    
    def connect(self):
        """Simulate database connection."""
        self.connected = True
        return True
    
    def disconnect(self):
        """Simulate database disconnection."""
        self.connected = False
    
    def save(self, key: str, value: any) -> bool:
        """Save data to database."""
        if not self.connected:
            raise ConnectionError("Database not connected")
        self.data[key] = value
        return True
    
    def get(self, key: str) -> Optional[any]:
        """Retrieve data from database."""
        if not self.connected:
            raise ConnectionError("Database not connected")
        return self.data.get(key)


class UserRepository:
    """Repository for user operations."""
    
    def __init__(self, database: Database):
        self.db = database
    
    def create_user(self, user_id: str, name: str, email: str) -> Dict:
        """Create a new user."""
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        user = {
            'id': user_id,
            'name': name,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        
        self.db.save(f"user:{user_id}", user)
        return user
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Retrieve a user by ID."""
        return self.db.get(f"user:{user_id}")


# ============================================================================
# PART 3: External API Calls (for Mocking/Patching)
# ============================================================================

class WeatherService:
    """Service that calls external weather API."""
    
    def __init__(self, api_key: str = "demo"):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"
    
    def get_temperature(self, city: str) -> float:
        """
        Fetch current temperature for a city.
        This makes a real API call - we'll mock this in tests!
        """
        response = requests.get(
            f"{self.base_url}/current",
            params={'city': city, 'key': self.api_key}
        )
        response.raise_for_status()
        data = response.json()
        return data['temperature']
    
    def is_good_weather(self, city: str) -> bool:
        """Determine if weather is good (above 20°C)."""
        temp = self.get_temperature(city)
        return temp > 20


class NotificationService:
    """Service for sending notifications."""
    
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """
        Send an email notification.
        In reality, this would call an email service.
        """
        # Simulate email sending
        print(f"Sending email to {to}: {subject}")
        return True
    
    @staticmethod
    def send_sms(phone: str, message: str) -> bool:
        """Send SMS notification."""
        print(f"Sending SMS to {phone}: {message}")
        return True


class OrderProcessor:
    """Process orders with notifications and weather checks."""
    
    def __init__(self, weather_service: WeatherService, notification_service: NotificationService):
        self.weather_service = weather_service
        self.notification_service = notification_service
    
    def process_order(self, order_id: str, customer_email: str, city: str) -> Dict:
        """
        Process an order and send notification.
        Checks weather to add special message.
        """
        # Check weather
        is_good = self.weather_service.is_good_weather(city)
        
        # Prepare message
        message = f"Order {order_id} confirmed!"
        if is_good:
            message += " Enjoy the nice weather!"
        
        # Send notification
        sent = self.notification_service.send_email(
            customer_email,
            "Order Confirmation",
            message
        )
        
        return {
            'order_id': order_id,
            'notification_sent': sent,
            'weather_checked': True,
            'is_good_weather': is_good
        }


# ============================================================================
# TESTS START HERE
# ============================================================================

import pytest
from unittest import mock
from unittest.mock import Mock, MagicMock, patch, call


# ============================================================================
# EXERCISE 1: Basic Unit Tests
# ============================================================================

class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price function."""
    
    def test_basic_calculation_no_discount(self):
        """Test basic price calculation without discount."""
        # TODO: Call calculate_total_price with price=10.0, quantity=5
        # TODO: Assert the result equals 50.0
        assert False, "TODO: Implement this test"
    
    def test_calculation_with_discount(self):
        """Test price calculation with discount."""
        # TODO: Call calculate_total_price with price=100.0, quantity=2, discount=10
        # TODO: Assert the result equals 180.0 (200 - 20)
        assert False, "TODO: Implement this test"
    
    def test_calculation_with_50_percent_discount(self):
        """Test with 50% discount."""
        # TODO: Call calculate_total_price with price=50.0, quantity=4, discount=50
        # TODO: Assert the result equals 100.0 (200 - 100)
        assert False, "TODO: Implement this test"
    
    def test_zero_quantity(self):
        """Test with zero quantity."""
        # TODO: Call calculate_total_price with price=10.0, quantity=0
        # TODO: Assert the result equals 0.0
        assert False, "TODO: Implement this test"
    
    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be non-negative")
        # TODO: Call calculate_total_price with price=-10.0, quantity=5
        assert False, "TODO: Implement this test"
    
    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be non-negative")
        # TODO: Call calculate_total_price with price=10.0, quantity=-5
        assert False, "TODO: Implement this test"
    
    def test_invalid_discount_over_100(self):
        """Test that discount over 100 raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be between 0 and 100")
        # TODO: Call calculate_total_price with discount=101
        assert False, "TODO: Implement this test"
    
    def test_invalid_discount_negative(self):
        """Test that negative discount raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be between 0 and 100")
        # TODO: Call calculate_total_price with discount=-10
        assert False, "TODO: Implement this test"


class TestValidateEmail:
    """Unit tests for email validation."""
    
    def test_valid_email(self):
        """Test valid email format."""
        # TODO: Call validate_email with "user@example.com"
        # TODO: Assert the result is True
        assert False, "TODO: Implement this test"
    
    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        # TODO: Call validate_email with "user@mail.example.com"
        # TODO: Assert the result is True
        assert False, "TODO: Implement this test"
    
    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        # TODO: Call validate_email with "userexample.com"
        # TODO: Assert the result is False
        assert False, "TODO: Implement this test"
    
    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        # TODO: Call validate_email with "user@"
        # TODO: Assert the result is False
        assert False, "TODO: Implement this test"
    
    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        # TODO: Call validate_email with "user@example"
        # TODO: Assert the result is False
        assert False, "TODO: Implement this test"
    
    def test_invalid_email_empty(self):
        """Test empty email."""
        # TODO: Call validate_email with ""
        # TODO: Assert the result is False
        assert False, "TODO: Implement this test"
    
    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        # TODO: Call validate_email with "user@@example.com"
        # TODO: Assert the result is False
        assert False, "TODO: Implement this test"


# ============================================================================
# EXERCISE 2: Integration Tests
# ============================================================================

class TestUserRepositoryIntegration:
    """Integration tests for UserRepository with Database."""
    
    @pytest.fixture
    def database(self):
        """Create a database instance for testing."""
        # TODO: Create a Database instance
        # TODO: Call connect() on the database
        # TODO: Use yield to return the database
        # TODO: After yield, call disconnect() on the database
        raise NotImplementedError("TODO: Implement this fixture")
    
    @pytest.fixture
    def user_repo(self, database):
        """Create a UserRepository with connected database."""
        # TODO: Create and return a UserRepository with the database
        raise NotImplementedError("TODO: Implement this fixture")
    
    def test_create_and_retrieve_user(self, user_repo):
        """Test creating and retrieving a user (integration test)."""
        # TODO: Create a user with id="123", name="John Doe", email="john@example.com"
        # TODO: Assert user['id'] == "123"
        # TODO: Assert user['name'] == "John Doe"
        # TODO: Assert user['email'] == "john@example.com"
        # TODO: Assert 'created_at' is in user
        
        # TODO: Retrieve the user by id "123"
        # TODO: Assert retrieved user is not None
        # TODO: Assert retrieved['id'] == "123"
        # TODO: Assert retrieved['name'] == "John Doe"
        assert False, "TODO: Implement this test"
    
    def test_create_user_with_invalid_email(self, user_repo):
        """Test that creating user with invalid email raises error."""
        # TODO: Use pytest.raises(ValueError, match="Invalid email")
        # TODO: Try to create a user with email="invalid-email"
        assert False, "TODO: Implement this test"
    
    def test_get_nonexistent_user(self, user_repo):
        """Test retrieving a user that doesn't exist."""
        # TODO: Get user with id="999"
        # TODO: Assert the result is None
        assert False, "TODO: Implement this test"
    
    def test_database_not_connected_raises_error(self):
        """Test that operations fail when database is not connected."""
        # TODO: Create a Database instance (don't connect it)
        # TODO: Create a UserRepository with this database
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to create a user
        assert False, "TODO: Implement this test"


# ============================================================================
# EXERCISE 3: Mocking External Dependencies
# ============================================================================

class TestWeatherServiceMocking:
    """Tests demonstrating mocking of external API calls."""
    
    @patch('requests.get')
    def test_get_temperature_success(self, mock_get):
        """Test getting temperature with mocked API response."""
        # TODO: Create a Mock() object for the response
        # TODO: Set mock_response.json.return_value = {'temperature': 25.5}
        # TODO: Set mock_response.raise_for_status.return_value = None
        # TODO: Set mock_get.return_value = mock_response
        
        # TODO: Create a WeatherService with api_key="test"
        # TODO: Call get_temperature("London")
        
        # TODO: Assert temp equals 25.5
        # TODO: Assert mock_get was called once with correct URL and params
        assert False, "TODO: Implement this test"
    
    @patch('requests.get')
    def test_is_good_weather_true(self, mock_get):
        """Test good weather detection (temp > 20)."""
        # TODO: Create a Mock() for the response
        # TODO: Set json return value with temperature: 25.0
        # TODO: Set mock_get.return_value
        
        # TODO: Create WeatherService instance
        # TODO: Call is_good_weather("Paris")
        # TODO: Assert result is True
        assert False, "TODO: Implement this test"
    
    @patch('requests.get')
    def test_is_good_weather_false(self, mock_get):
        """Test bad weather detection (temp <= 20)."""
        # TODO: Create mock response with temperature: 15.0
        # TODO: Set mock_get.return_value
        
        # TODO: Create WeatherService instance
        # TODO: Call is_good_weather("Berlin")
        # TODO: Assert result is False
        assert False, "TODO: Implement this test"
    
    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Test handling of API errors."""
        # TODO: Set mock_get.side_effect to raise requests.exceptions.RequestException
        
        # TODO: Create WeatherService instance
        # TODO: Use pytest.raises to expect RequestException
        # TODO: Call get_temperature("Tokyo")
        assert False, "TODO: Implement this test"


# ============================================================================
# EXERCISE 4: Advanced Mocking and Patching
# ============================================================================

class TestOrderProcessorMocking:
    """Tests demonstrating complex mocking scenarios."""
    
    def test_process_order_with_good_weather(self):
        """Test order processing with mocked weather and notification services."""
        # TODO: Create Mock(spec=WeatherService)
        # TODO: Set is_good_weather.return_value = True
        
        # TODO: Create Mock(spec=NotificationService)
        # TODO: Set send_email.return_value = True
        
        # TODO: Create OrderProcessor with both mocks
        # TODO: Call process_order("ORD-001", "customer@example.com", "Madrid")
        
        # TODO: Assert result['order_id'] == "ORD-001"
        # TODO: Assert result['notification_sent'] is True
        # TODO: Assert result['is_good_weather'] is True
        
        # TODO: Assert mock_weather.is_good_weather was called once with "Madrid"
        # TODO: Assert mock_notification.send_email was called once
        # TODO: Check that email body contains "Enjoy the nice weather"
        assert False, "TODO: Implement this test"
    
    def test_process_order_with_bad_weather(self):
        """Test order processing with bad weather."""
        # TODO: Create mocks for weather and notification services
        # TODO: Set is_good_weather.return_value = False
        # TODO: Set send_email.return_value = True
        
        # TODO: Create OrderProcessor and call process_order
        
        # TODO: Assert result['is_good_weather'] is False
        # TODO: Verify the email body does NOT contain "Enjoy the nice weather"
        assert False, "TODO: Implement this test"
    
    @patch.object(NotificationService, 'send_email')
    @patch.object(WeatherService, 'is_good_weather')
    def test_process_order_with_patch_object(self, mock_weather, mock_email):
        """Test using patch.object decorator."""
        # TODO: Set mock_weather.return_value = True
        # TODO: Set mock_email.return_value = True
        
        # TODO: Create actual WeatherService and NotificationService instances
        # TODO: Create OrderProcessor with these instances
        # TODO: Call process_order("ORD-003", "test@example.com", "Barcelona")
        
        # TODO: Assert result['notification_sent'] is True
        # TODO: Verify mock_weather was called once with "Barcelona"
        # TODO: Verify mock_email was called once
        assert False, "TODO: Implement this test"
    
    def test_notification_failure_handling(self):
        """Test handling notification service failures."""
        # TODO: Create mocks for weather and notification services
        # TODO: Set is_good_weather.return_value = True
        # TODO: Set send_email.return_value = False (email fails)
        
        # TODO: Create OrderProcessor and call process_order
        
        # TODO: Assert result['notification_sent'] is False
        assert False, "TODO: Implement this test"


# ============================================================================
# EXERCISE 5: Pytest Fixtures and Parametrize
# ============================================================================

class TestPytestFeatures:
    """Demonstrate pytest-specific features."""
    
    @pytest.fixture
    def sample_prices(self):
        """Fixture providing sample price data."""
        return [
            (10.0, 5, 0, 50.0),
            (10.0, 5, 10, 45.0),
            (100.0, 2, 25, 150.0),
        ]
    
    @pytest.mark.parametrize("price,quantity,discount,expected", [
        (10.0, 5, 0, 50.0),
        (10.0, 5, 10, 45.0),
        (100.0, 2, 25, 150.0),
        (50.0, 10, 20, 400.0),
        (25.0, 4, 50, 50.0),
    ])
    def test_calculate_total_price_parametrized(self, price, quantity, discount, expected):
        """Test multiple scenarios using parametrize."""
        # TODO: Call calculate_total_price with price, quantity, discount
        # TODO: Assert result equals expected
        assert False, "TODO: Implement this test"
    
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("test@mail.example.org", True),
        ("invalid", False),
        ("no-at-sign.com", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
    ])
    def test_validate_email_parametrized(self, email, expected):
        """Test email validation with multiple cases."""
        # TODO: Call validate_email with email
        # TODO: Assert result equals expected
        assert False, "TODO: Implement this test"


# ============================================================================
# BONUS: Mock Best Practices Examples
# ============================================================================

class TestMockBestPractices:
    """Examples of best practices when using mocks."""
    
    def test_using_spec_prevents_invalid_attributes(self):
        """Using spec prevents accessing non-existent attributes."""
        # TODO: Create Mock(spec=WeatherService)
        
        # TODO: Set mock_weather.get_temperature.return_value = 20.0 (this works)
        
        # TODO: Use pytest.raises(AttributeError) to verify that
        # TODO: accessing mock_weather.non_existent_method() raises an error
        assert False, "TODO: Implement this test"
    
    def test_verify_exact_calls_with_assert_called_with(self):
        """Verify exact arguments passed to mocked method."""
        # TODO: Create a Mock()
        # TODO: Call mock_notification.send_email("test@example.com", "Subject", "Body")
        
        # TODO: Use assert_called_with to verify exact arguments
        assert False, "TODO: Implement this test"
    
    def test_verify_call_count(self):
        """Verify how many times a mock was called."""
        # TODO: Create a Mock()
        
        # TODO: Call mock_service.some_method() three times
        
        # TODO: Assert mock_service.some_method.call_count == 3
        assert False, "TODO: Implement this test"
    
    def test_mock_side_effects(self):
        """Use side_effect for exceptions or varying returns."""
        # TODO: Create a Mock()
        
        # TODO: Set mock_api.fetch.side_effect = [10, 20, 30]
        
        # TODO: Call mock_api.fetch() three times
        # TODO: Assert first call returns 10
        # TODO: Assert second call returns 20
        # TODO: Assert third call returns 30
        assert False, "TODO: Implement this test"
    
    def test_reset_mock(self):
        """Reset a mock to clear call history."""
        # TODO: Create a Mock()
        
        # TODO: Call mock_service.method()
        # TODO: Assert mock_service.method.called is True
        
        # TODO: Call mock_service.reset_mock()
        # TODO: Assert mock_service.method.called is False
        assert False, "TODO: Implement this test"


if __name__ == "__main__":
    print("Run tests with: pytest testing_exercise_student.py -v")
    print("\nOr with coverage: pytest testing_exercise_student.py -v --cov")

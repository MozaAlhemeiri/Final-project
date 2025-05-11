##############################
# models.py
##############################

from datetime import datetime
import uuid

class Person:
    # Base class for all persons in the system
    
    def __init__(self, name, email, phone):
        # Initialize a person with basic details
        self.name = name
        self.email = email
        self.phone = phone

class User(Person):
    # User class that inherits from Person
    
    def __init__(self, username, password, name, email, phone):
        # Initialize a user with login credentials and personal details
        super().__init__(name, email, phone)
        self.username = username
        self.password = password
        self.created_at = datetime.now()
        self.purchase_history = []  # Aggregation: User has many Purchase Orders
    
    def add_purchase(self, purchase):
        # Add a purchase to user's history
        self.purchase_history.append(purchase)
    
    def get_purchase_history(self):
        # Get user's purchase history
        return self.purchase_history

class AdminUser(User):
    # Admin user class that inherits from User
    
    def __init__(self, username, password, name, email, phone, admin_level=1):
        # Initialize an admin user with additional admin privileges
        super().__init__(username, password, name, email, phone)
        self.admin_level = admin_level
        self.last_login = datetime.now()

class TicketDetails:
    # Class to store details of a ticket Composition with Ticket class
    
    def __init__(self, price, validity, features):
        # Initialize ticket details
        self.price = price
        self.validity = validity
        self.features = features

class Ticket:
    # Base class for all tickets
    
    def __init__(self, name, description, price, validity, features):
        # Initialize a ticket with basic details and compose with TicketDetails
        self.ticket_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        # Composition: Ticket contains TicketDetails
        self.details = TicketDetails(price, validity, features)
    
    def get_price(self):
        # Get the price of the ticket
        return self.details.price
    
    def get_validity(self):
        # Get the validity period of the ticket
        return self.details.validity
    
    def get_features(self):
        # Get the features of the ticket
        return self.details.features

class SingleRaceTicket(Ticket):
    # Single race ticket class that inherits from Ticket
    
    def __init__(self, race_date, race_name, seat_type):
        # Initialize a single race ticket with specific details
        name = "Single Race Pass"
        description = "Access to " + race_name + " on " + race_date
        price = 150.0  # Base price
        
        # Adjust price based on seat type
        if seat_type == "VIP":
            price = 300.0
        elif seat_type == "Premium":
            price = 250.0
        
        validity = "Valid only on " + race_date
        features = ["Access to " + race_name, seat_type + " seating", "Race program"]
        
        super().__init__(name, description, price, validity, features)
        self.race_date = race_date
        self.race_name = race_name
        self.seat_type = seat_type

class WeekendPackageTicket(Ticket):
    # Weekend package ticket class that inherits from Ticket
    
    def __init__(self, weekend_dates, event_name, includes_parking=False):
        # Initialize a weekend package ticket with specific details
        name = "Weekend Package"
        description = "Full access to " + event_name + " weekend events"
        price = 350.0  # Base price
        
        # Add parking fee if included
        if includes_parking:
            price += 50.0
        
        validity = "Valid from " + weekend_dates
        features = [
            "Access to all weekend races", 
            "Pit lane walk", 
            "Driver autograph session"
        ]
        
        if includes_parking:
            features.append("Weekend parking pass")
        
        super().__init__(name, description, price, validity, features)
        self.weekend_dates = weekend_dates
        self.event_name = event_name
        self.includes_parking = includes_parking

class SeasonMembershipTicket(Ticket):
    # Season membership ticket class that inherits from Ticket
    
    def __init__(self, season_year, membership_level):
        # Initialize a season membership ticket with specific details
        name = membership_level + " Season Membership"
        description = "Full season access for " + season_year + " with " + membership_level + " benefits"
        
        # Set price based on membership level
        if membership_level == "Gold":
            price = 2000.0
            features = [
                "Access to all season races",
                "VIP seating at all events",
                "Exclusive paddock access",
                "Meet and greet with drivers",
                "Complimentary parking for all events",
                "Season merchandise pack"
            ]
        elif membership_level == "Silver":
            price = 1500.0
            features = [
                "Access to all season races",
                "Premium seating at all events",
                "Paddock access for 3 races",
                "Complimentary parking for 5 events",
                "Season merchandise pack"
            ]
        else:  # Bronze
            price = 1000.0
            features = [
                "Access to all season races",
                "Standard seating at all events",
                "Paddock access for 1 race",
                "Season merchandise pack"
            ]
        
        validity = "Valid for entire " + season_year + " season"
        
        super().__init__(name, description, price, validity, features)
        self.season_year = season_year
        self.membership_level = membership_level

class Payment:
    # Base class for all payment types
    
    def __init__(self, amount, payment_date=None):
        # Initialize a payment with basic details
        self.payment_id = str(uuid.uuid4())
        self.amount = amount
        self.payment_date = payment_date if payment_date else datetime.now()
        self.status = "Pending"
    
    def process_payment(self):
        # Process the payment (to be implemented by subclasses)
        pass
    
    def get_payment_details(self):
        # Get payment details
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "status": self.status
        }

class CreditCardPayment(Payment):
    # Credit card payment class that inherits from Payment
    
    def __init__(self, amount, card_number, expiry_date, cvv):
        # Initialize a credit card payment with specific details
        super().__init__(amount)
        # Only store last 4 digits for security
        self.card_number = "XXXXXXXXXXXX" + card_number[-4:]
        self.expiry_date = expiry_date
        self.payment_type = "Credit Card"
    
    def process_payment(self):
        # Process a credit card payment
        # In a real system, this would connect to a payment gateway
        self.status = "Completed"
        return True
    
    def get_payment_details(self):
        # Get payment details with credit card specific info
        details = super().get_payment_details()
        details["payment_type"] = self.payment_type
        details["card_number"] = self.card_number
        details["expiry_date"] = self.expiry_date
        return details

class DigitalWalletPayment(Payment):
    # Digital wallet payment class that inherits from Payment
    
    def __init__(self, amount, wallet_type, wallet_id):
        # Initialize a digital wallet payment with specific details
        super().__init__(amount)
        self.wallet_type = wallet_type  # e.g "PayPal", "Apple Pay"
        self.wallet_id = wallet_id
        self.payment_type = "Digital Wallet"
    
    def process_payment(self):
        # Process a digital wallet payment
        self.status = "Completed"
        return True
    
    def get_payment_details(self):
        # Get payment details with digital wallet specific info
        details = super().get_payment_details()
        details["payment_type"] = self.payment_type
        details["wallet_type"] = self.wallet_type
        details["wallet_id"] = self.wallet_id
        return details

class PurchaseOrder:
    # Class to represent a complete purchase order
    
    def __init__(self, user, tickets, payment, discount_code=None, discount_amount=0):
        # Initialize a purchase order with user, tickets, and payment
        self.order_id = str(uuid.uuid4())
        self.user = user  # Association: Purchase order is associated with a User
        self.tickets = tickets  # Aggregation: Purchase order contains many Tickets
        self.payment = payment  # Association: Purchase order is associated with a Payment
        self.order_date = datetime.now()
        self.discount_code = discount_code
        self.discount_amount = discount_amount
        self.status = "Created"
    
    def confirm_order(self):
        # Confirm the order after payment is processed
        payment_result = self.payment.process_payment()
        if payment_result:
            self.status = "Confirmed"
            return True
        return False
    
    def cancel_order(self):
        # Cancel the order
        self.status = "Cancelled"
    
    def get_order_total(self):
        # Calculate the total price of the order
        total = sum(ticket.get_price() for ticket in self.tickets)
        return total - self.discount_amount
    
    def get_order_details(self):
        # Get complete order details
        tickets_info = []
        for ticket in self.tickets:
            tickets_info.append({
                "name": ticket.name,
                "price": ticket.get_price()
            })
        
        return {
            "order_id": self.order_id,
            "user": self.user.username,
            "tickets": tickets_info,
            "payment": self.payment.get_payment_details(),
            "order_date": self.order_date,
            "discount_code": self.discount_code,
            "discount_amount": self.discount_amount,
            "total": self.get_order_total(),
            "status": self.status
        }
##############################
# database.py
##############################

import pickle
import os
from datetime import datetime

class Database:
    # This class handles all database operations using pickle for binary file storage
    
    def __init__(self):
        # Initialize database and create necessary folders and files
        self.users_file = "data/users.pkl"
        self.tickets_file = "data/tickets.pkl"
        self.sales_file = "data/sales.pkl"
        self.discounts_file = "data/discounts.pkl"
        
        # Create directory if it does not exist
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Initialize files if they do not exist
        self._initialize_files()
    
    def _initialize_files(self):
        # Initialize all database files if they do not exist
        
        # Initialize users file
        if not os.path.exists(self.users_file):
            self._save_data(self.users_file, {})
        
        # Initialize tickets file
        if not os.path.exists(self.tickets_file):
            self._save_data(self.tickets_file, {})
        
        # Initialize sales file
        if not os.path.exists(self.sales_file):
            self._save_data(self.sales_file, {})
        
        # Initialize discounts file
        if not os.path.exists(self.discounts_file):
            # Default discounts
            discounts = {
                "WELCOME10": {"percentage": 10, "active": True},
                "GROUP20": {"percentage": 20, "active": True},
                "SEASON25": {"percentage": 25, "active": True}
            }
            self._save_data(self.discounts_file, discounts)
    
    def _load_data(self, file_path):
        # Load data from a pickle file
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            # Return empty dict if file does not exist or is empty
            return {}
    
    def _save_data(self, file_path, data):
        # Save data to a pickle file
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    
    # User-related methods
    def add_user(self, user):
        # Add a new user to the database
        users = self._load_data(self.users_file)
        users[user.username] = user
        self._save_data(self.users_file, users)
    
    def get_user(self, username):
        # Get a user by username
        users = self._load_data(self.users_file)
        return users.get(username)
    
    def update_user(self, user):
        # Update an existing user
        self.add_user(user)
    
    def delete_user(self, username):
        # Delete a user from the database
        users = self._load_data(self.users_file)
        if username in users:
            del users[username]
            self._save_data(self.users_file, users)
            return True
        return False
    
    def get_all_users(self):
        # Get all users from the database
        return self._load_data(self.users_file)
    
    # Ticket-related methods
    def add_ticket(self, ticket_id, ticket):
        # Add a new ticket to the database
        tickets = self._load_data(self.tickets_file)
        tickets[ticket_id] = ticket
        self._save_data(self.tickets_file, tickets)
    
    def get_ticket(self, ticket_id):
        # Get a ticket by ID
        tickets = self._load_data(self.tickets_file)
        return tickets.get(ticket_id)
    
    def update_ticket(self, ticket_id, ticket):
        # Update an existing ticket
        self.add_ticket(ticket_id, ticket)
    
    def delete_ticket(self, ticket_id):
        # Delete a ticket from the database
        tickets = self._load_data(self.tickets_file)
        if ticket_id in tickets:
            del tickets[ticket_id]
            self._save_data(self.tickets_file, tickets)
            return True
        return False
    
    def get_all_tickets(self):
        # Get all tickets from the database
        return self._load_data(self.tickets_file)
    
    # Sales-related methods
    def add_sale(self, sale):
        # Add a new sale to the database
        sales = self._load_data(self.sales_file)
        
        # Group sales by date
        date_str = sale['date'].strftime('%Y-%m-%d')
        if date_str not in sales:
            sales[date_str] = []
        
        sales[date_str].append(sale)
        self._save_data(self.sales_file, sales)
    
    def get_sales_by_date(self, date_str):
        # Get sales for a specific date
        sales = self._load_data(self.sales_file)
        return sales.get(date_str, [])
    
    def get_all_sales(self):
        # Get all sales from the database
        return self._load_data(self.sales_file)
    
    # Discount-related methods
    def get_all_discounts(self):
        # Get all discounts from the database
        return self._load_data(self.discounts_file)
    
    def update_discount(self, code, active):
        # Update discount status (active/inactive)
        discounts = self._load_data(self.discounts_file)
        if code in discounts:
            discounts[code]['active'] = active
            self._save_data(self.discounts_file, discounts)
            return True
        return False
    
    def is_valid_discount(self, code):
        # Check if a discount code is valid
        discounts = self._load_data(self.discounts_file)
        return code in discounts and discounts[code]['active']
    
    def get_discount_percentage(self, code):
        # Get discount percentage for a code
        discounts = self._load_data(self.discounts_file)
        if code in discounts and discounts[code]['active']:
            return discounts[code]['percentage']
        return 0
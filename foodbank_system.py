"""
Charity Food Bank Booking System
A simple Python system demonstrating BDD principles for a non-profit organisation.
"""

import re

class BookingError(Exception):
    """Custom exception for booking failures."""
    pass

class FoodBankBooking:
    """
    Handles food bank slot bookings with eligibility checking and postcode validation.
    """
    
    def __init__(self):
        # Simulated slot availability for demonstration
        self.available_slots = {
            "2026-06-20": 0,  # Fully booked - used for edge case testing
            "2026-06-21": 3,
            "2026-06-22": 5,
            "2026-06-23": 2
        }
        self.booking_counter = 1000
    
    def is_valid_postcode(self, postcode):
        """
        Validates UK postcode format.
        Accepts standard formats like M1 1AE, SW1A 1AA, etc.
        """
        # Simplified pattern for demonstration
        pattern = r'^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$'
        return bool(re.match(pattern, postcode.upper().strip()))
    
    def check_eligibility(self, income_criterion):
        """
        Checks if a user meets the eligibility criteria.
        In a real system, this would query a database or external service.
        """
        # Simplified for demonstration
        eligible_criteria = ["below poverty line", "universal credit", "low income"]
        return income_criterion.lower() in eligible_criteria
    
    def book_slot(self, postcode, eligible, requested_date):
        """
        Books a collection slot for an eligible user with valid postcode.
        
        Args:
            postcode (str): User's postcode
            eligible (bool): Whether user meets income criteria
            requested_date (str): Desired collection date in YYYY-MM-DD format
            
        Returns:
            str: Booking reference number
            
        Raises:
            BookingError: If validation fails or no slots available
        """
        # Validate postcode
        if not self.is_valid_postcode(postcode):
            raise BookingError("Invalid postcode format")
        
        # Check eligibility
        if not eligible:
            raise BookingError("User does not meet income eligibility criteria")
        
        # Check if date exists in booking calendar
        if requested_date not in self.available_slots:
            raise BookingError(f"Date {requested_date} is not available for booking")
        
        # Check slot availability
        if self.available_slots[requested_date] <= 0:
            # Suggest alternative dates with available slots
            alternatives = [
                d for d, count in self.available_slots.items() 
                if count > 0
            ]
            alternatives_str = ", ".join(alternatives)
            raise BookingError(
                f"No slots on {requested_date}. Alternatives: {alternatives_str}"
            )
        
        # Book the slot
        self.available_slots[requested_date] -= 1
        self.booking_counter += 1
        return f"BK-{self.booking_counter}"
    
    def get_available_slots(self):
        """Returns a dictionary of dates with available slot counts."""
        return {date: count for date, count in self.available_slots.items() if count > 0}
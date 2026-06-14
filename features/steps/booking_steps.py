from behave import given, when, then
import sys
import os

# Add the parent directory to the path so we can import foodbank_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from foodbank_system import FoodBankBooking, BookingError

@given('the user provides a valid postcode "{postcode}"')
def step_given_valid_postcode(context, postcode):
    context.postcode = postcode

@given('the user provides an invalid postcode "{postcode}"')
def step_given_invalid_postcode(context, postcode):
    context.postcode = postcode

@given('the user meets the income criteria "{criteria}"')
def step_given_income_criteria(context, criteria):
    # In a real system, this would query a database or external service
    context.is_eligible = (criteria == "below poverty line")

@given('the requested date "{date}" has no available slots')
def step_given_no_slots(context, date):
    context.no_slots_date = date

@when('the user requests to book a slot for "{date}"')
def step_when_request_booking(context, date):
    booking_system = FoodBankBooking()
    # Store the booking system in context so we can reuse it if needed
    context.booking_system = booking_system
    try:
        context.result = booking_system.book_slot(
            context.postcode, 
            context.is_eligible, 
            date
        )
    except BookingError as e:
        context.error = str(e)
        # Capture alternative dates if provided in error message
        if "Alternatives:" in context.error:
            alt_part = context.error.split("Alternatives: ")[1]
            context.alternative_dates = [d.strip() for d in alt_part.split(", ")]

@then('the system should confirm booking with reference "{reference}"')
def step_then_confirm_booking(context, reference):
    # Check if result exists in context
    assert hasattr(context, 'result'), "No result was set. The booking may have failed."
    assert context.result == reference, \
        f"Expected {reference}, got {context.result}"

@then('the system should reject with message "{message}"')
def step_then_reject(context, message):
    assert hasattr(context, 'error'), "No error was raised but one was expected"
    assert message in str(context.error), \
        f"Expected '{message}' in '{context.error}'"

@then('the system should suggest alternative dates "{dates}"')
def step_then_suggest_dates(context, dates):
    expected_dates = dates.split(", ")
    assert hasattr(context, 'alternative_dates'), "No alternative dates captured"
    # Sort both lists for comparison to avoid order issues
    assert sorted(context.alternative_dates) == sorted(expected_dates), \
        f"Expected {expected_dates}, got {context.alternative_dates}"
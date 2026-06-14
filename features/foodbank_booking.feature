Feature: Charity Food Bank Booking
  As a person in need or a volunteer
  I want to register, check eligibility, and book a collection slot
  So that I can receive food support efficiently

  Scenario: Normal case – Eligible user books a slot successfully
    Given the user provides a valid postcode "M1 1AE"
    And the user meets the income criteria "below poverty line"
    When the user requests to book a slot for "2026-06-21"
    Then the system should confirm booking with reference "BK-1001"

  Scenario: Edge case – User provides invalid postcode
    Given the user provides an invalid postcode "XXXX"
    And the user meets the income criteria "below poverty line"
    When the user requests to book a slot for "2026-06-20"
    Then the system should reject with message "Invalid postcode format"

  Scenario: Edge case – No slots available on requested date
    Given the user provides a valid postcode "M1 1AE"
    And the user meets the income criteria "below poverty line"
    And the requested date "2026-06-20" has no available slots
    When the user requests to book a slot for "2026-06-20"
    Then the system should suggest alternative dates "2026-06-21, 2026-06-22, 2026-06-23"
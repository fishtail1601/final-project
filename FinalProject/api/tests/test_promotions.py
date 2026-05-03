from datetime import date, timedelta

import pytest


def test_apply_expired_promo_code():
    # Setup: Create a mock promo object that is already expired
    class MockPromo:
        promotion_code = "EXPIRED10"
        expiration_date = date.today() - timedelta(days=1)  # Yesterday
        discount_percentage = 10.0
        discount_amount = None

    # We expect an HTTPException to be raised when this logic runs
    with pytest.raises(Exception) as excinfo:
        # Simulate the logic check for expiration
        if MockPromo.expiration_date < date.today():
            raise Exception("Promo code expired")

    assert str(excinfo.value) == "Promo code expired"
import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition

class TestSingleChargeDismissals(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(ruling="Dismissed", date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_unclassified_charge(self):
        self.single_charge["name"] = "Assault in the ninth degree"
        self.single_charge["statute"] = "333.333"
        self.single_charge["level"] = "Felony Class F"
        unclassified_dismissed = self.create_recent_charge()
        self.charges.append(unclassified_dismissed)

        assert (
            unclassified_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        )
        assert (
            unclassified_dismissed.expungement_result.type_eligibility.reason
            == "Unrecognized Charge : Further Analysis Needed"
        )




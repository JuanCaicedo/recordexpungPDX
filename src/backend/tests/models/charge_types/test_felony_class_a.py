import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition

class TestFelonyClassAConvicted(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_convicted = self.create_recent_charge()
        self.charges.append(felony_class_a_convicted)

        assert felony_class_a_convicted.type_name == "Felony Class A"
        assert felony_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert felony_class_a_convicted.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"


class TestFelonyClassAAcquittals(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(ruling="Acquitted", date=last_week)
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_acquitted_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_acquitted = self.create_recent_charge()
        self.charges.append(felony_class_a_acquitted)

        assert felony_class_a_acquitted.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_acquitted.expungement_result.type_eligibility.reason == "Eligible under 137.225(1)(b)"

    def test_felony_class_a_dismissed_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_dismissed = self.create_recent_charge()
        self.charges.append(felony_class_a_dismissed)

        assert felony_class_a_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_dismissed.expungement_result.type_eligibility.reason == "Eligible under 137.225(1)(b)"

class TestSingleChargeNoComplaint(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build()
        self.single_charge["disposition"] = Disposition(date=last_week, ruling="No Complaint")
        self.charges = []

    def create_recent_charge(self):
        return ChargeFactory.save(self.single_charge)

    def test_felony_class_a_charge(self):
        self.single_charge["name"] = "Assault in the first degree"
        self.single_charge["statute"] = "163.185"
        self.single_charge["level"] = "Felony Class A"
        felony_class_a_no_complaint = self.create_recent_charge()
        self.charges.append(felony_class_a_no_complaint)

        assert felony_class_a_no_complaint.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert felony_class_a_no_complaint.expungement_result.type_eligibility.reason == "Eligible under 137.225(1)(b)"


class TestMultipleCharges(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        disposition = Disposition(ruling="Convicted", date=last_week)
        self.charge = ChargeFactory.build(disposition=disposition)
        self.charges = []

    def create_charge(self):
        charge = ChargeFactory.save(self.charge)
        return charge

    def test_two_charges(self):
        # first charge
        self.charge["name"] = "Theft of services"
        self.charge["statute"] = "164.125"
        self.charge["level"] = "Misdemeanor Class A"
        charge = self.create_charge()
        self.charges.append(charge)

        # second charge
        self.charge["name"] = "Traffic Violation"
        self.charge["statute"] = "801.000"
        self.charge["level"] = "Class C Traffic Violation"
        charge = self.create_charge()
        self.charges.append(charge)

        assert self.charges[0].expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.charges[0].expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

        assert self.charges[1].expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert self.charges[1].expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

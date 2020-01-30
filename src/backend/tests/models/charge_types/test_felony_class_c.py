import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictions(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_misdemeanor(self):
        self.single_charge["name"] = "Criminal Trespass in the Second Degree"
        self.single_charge["statute"] = "164.245"
        self.single_charge["level"] = "Misdemeanor Class C"
        misdemeanor_charge = self.create_recent_charge()
        self.charges.append(misdemeanor_charge)

        assert misdemeanor_charge.type_name == "Misdemeanor"
        assert misdemeanor_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert misdemeanor_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_marijuana_ineligible_statute_475b3493c(self):
        self.single_charge["name"] = "Unlawful Manufacture of Marijuana Item"
        self.single_charge["statute"] = "475B.349(3)(C)"
        self.single_charge["level"] = "Felony Class C"
        marijuana_felony_class_c = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_c)

        assert marijuana_felony_class_c.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_c.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_c.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_subsection_12_163205(self):
        self.single_charge["name"] = "Criminal mistreatment in the first degree"
        self.single_charge["statute"] = "163.205"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_subsection_12_163535(self):
        self.single_charge["name"] = "Abandonment of a child"
        self.single_charge["statute"] = "163.535"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_subsection_12_163275(self):
        self.single_charge["name"] = "Coercion"
        self.single_charge["statute"] = "163.275"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"
    
    def test_subsection_12_163525(self):
        self.single_charge["name"] = "Incest"
        self.single_charge["statute"] = "163.525"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_subsection_12_164395(self):
        self.single_charge["name"] = "Robbery in the third degree"
        self.single_charge["statute"] = "164.395"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_subsection_12_163165(self):
        self.single_charge["name"] = "Assault in the third degree"
        self.single_charge["statute"] = "163.165"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_subsection_12_166220(self):
        self.single_charge["name"] = "Unlawful use of weapon"
        self.single_charge["statute"] = "166.220"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"
    
    def test_subsection_12_charge_that_includes_sub_chapter(self):
        self.single_charge["name"] = "Unlawful use of weapon"
        self.single_charge["statute"] = "166.220(1)(b)"
        self.single_charge["level"] = "Felony Class C"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_pcs_475992(self):
        self.single_charge["name"] = "Poss Controlled Sub 2"
        self.single_charge["statute"] = "4759924B"
        self.single_charge["level"] = "Felony Class C"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_misdemeanor_164043(self):
        self.single_charge["name"] = "Theft in the third degree"
        self.single_charge["statute"] = "164.043"
        self.single_charge["level"] = "Misdemeanor Class C"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.type_name == "Misdemeanor"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_misdemeanor_164055(self):
        self.single_charge["name"] = "Theft in the first degree"
        self.single_charge["statute"] = "164.055"
        self.single_charge["level"] = "Felony Class C"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.type_name == "Felony Class C"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

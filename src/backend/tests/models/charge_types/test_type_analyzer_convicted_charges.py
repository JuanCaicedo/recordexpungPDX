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

    def test_marijuana_ineligible_statute_475b359(self):
        self.single_charge["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
        self.single_charge["statute"] = "475b.359"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b367(self):
        self.single_charge["name"] = "Causing another person to ingest marijuana"
        self.single_charge["statute"] = "475B.367"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_475b371(self):
        self.single_charge["name"] = "Administration to another person under 18 years of age"
        self.single_charge["statute"] = "475B.371"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    def test_marijuana_ineligible_statute_167262(self):
        self.single_charge["name"] = "Use of minor in controlled substance or marijuana item offense"
        self.single_charge["statute"] = "167.262"
        self.single_charge["level"] = "Misdemeanor Class A"
        marijuana_misdemeanor_class_a = self.create_recent_charge()
        self.charges.append(marijuana_misdemeanor_class_a)

        assert marijuana_misdemeanor_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    # List B Tests - Currently being marked as "Further Analysis Needed"

    def test_subsection_12_163200(self):
        self.single_charge["name"] = "Criminal mistreatment in the second degree"
        self.single_charge["statute"] = "163.200"
        self.single_charge["level"] = "Misdemeanor Class A"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    def test_subsection_12_163575(self):
        self.single_charge["name"] = "Endangering the welfare of a minor"
        self.single_charge["statute"] = "163.575"
        self.single_charge["level"] = "Misdemeanor Class A"
        subsection_12_charge = self.create_recent_charge()
        self.charges.append(subsection_12_charge)

        assert subsection_12_charge.type_name == "Subsection 12"
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert subsection_12_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"

    # Test sub-chapters are not compared when not necessary.

    def test_marijuana_ineligible_statute_475b3592a(self):
        self.single_charge["name"] = "Arson incident to manufacture of cannabinoid extract in first degree"
        self.single_charge["statute"] = "475b.359(2)(a)"
        self.single_charge["level"] = "Felony Class A"
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.type_name == "Marijuana Ineligible"
        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == "Ineligible under 137.226"

    # Possession of controlled substance tests

    def test_pcs_475854(self):
        self.single_charge["name"] = "Unlawful possession of heroin"
        self.single_charge["statute"] = "475.854"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475874(self):
        self.single_charge["name"] = "Unlawful possession of 3,4-methylenedioxymethamphetamine"
        self.single_charge["statute"] = "475.874"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475884(self):
        self.single_charge["name"] = "Unlawful possession of cocaine"
        self.single_charge["statute"] = "475.884"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475894(self):
        self.single_charge["name"] = "Unlawful possession of methamphetamine"
        self.single_charge["statute"] = "475.894"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    # Eligible misdemeanor and class C felony tests

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

    def test_misdemeanor_164125(self):
        self.single_charge["name"] = "Theft of services"
        self.single_charge["statute"] = "164.125"
        self.single_charge["level"] = "Misdemeanor Class A"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.type_name == "Misdemeanor"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_drug_free_zone_variance_misdemeanor(self):
        self.single_charge["name"] = "	Drug Free Zone Variance"
        self.single_charge["statute"] = "14B20060"
        self.single_charge["level"] = "Misdemeanor Unclassified"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.type_name == "Misdemeanor"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_charge_that_falls_through(self):
        self.single_charge["name"] = "Aggravated theft in the first degree"
        self.single_charge["statute"] = "164.057"
        self.single_charge["level"] = "Felony Class F"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.type_name == "Unclassified"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"

    # Test non-traffic violation

    def test_non_traffic_violation(self):
        self.single_charge["name"] = "Viol Treatment"
        self.single_charge["statute"] = "1615662"
        self.single_charge["level"] = "Violation Unclassified"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.type_name == "Non-traffic Violation"
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(d)"

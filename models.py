#engine of the Divishana Eligibility check

class Applicant:
    def __init__(self,district,family_size,monthly_income,employment,has_elderly,has_disabled,has_children,has_pregnant,housing):
        self.district = district
        self.family_size = int(family_size)
        self.monthly_income = monthly_income
        self.employment = employment
        self.has_elderly = has_elderly      #person with age 70 or above
        self.has_disabled = has_disabled    #person with disability
        self.has_children = has_children    #cildren under 18 years old
        self.has_pregnant = has_pregnant    #pregnant/breastfeeding mother
        self.housing = housing

        @property
        def income_per_person(self):
            if self.family_size <= 0:
                return 0
            return self.monthly_income / self.family_size
        @property
        def is_small_family(self):
            return self.family_size <= 2
        
class Benefit:
    def __init__(self):
        self.name       = ""
        self.name_si    = ""
        self.icon       = ""
        self.amount     = ""
        self.where      = ""
        self.hotline    = ""
        self.steps      = []

    def is_eligible(self, applicant):
        raise NotImplementedError("Each benefit must define its own rules")
 
    def get_result(self, applicant):
        return {
            "name":     self.name,
            "name_si":  self.name_si,
            "icon":     self.icon,
            "amount":   self.amount,
            "where":    self.where,
            "hotline":  self.hotline,
            "steps":    self.steps,
        }
class AswesumaBenefit(Benefit):
    """
    Sri Lanka's main welfare programme.
    1,737,141 families receiving payments as of 2025.
    Uses 22 indicators — we simplify to income per person.
    """
    def __init__(self):
        super().__init__()
        self.name    = "Aswesuma Welfare Programme"
        self.name_si = "අස්වෙසුම ප්‍රතිලාභ වැඩසටහන"
        self.icon    = "🏠"
        self.where   = "Nearest Divisional Secretariat office"
        self.hotline = "1924"
        self.steps   = [
            "Visit your nearest Divisional Secretariat office",
            "Bring your National Identity Card (NIC)",
            "Fill the Aswesuma application form — free of charge",
            "A field officer will visit your home to verify",
            "If approved, payment starts within 4–6 weeks",
            "Online: eservices.wbb.gov.lk",
        ]
 
    def is_eligible(self, applicant):
        # Based on income per person — simplified from 22-indicator score
        return applicant.income_per_person < 13000
 
    def get_result(self, applicant):
        result = super().get_result(applicant)
        tier, amount = self._get_tier(applicant)
        result["tier"]   = tier
        result["amount"] = amount
        result["note"]   = "Amount halved for families of 2 or fewer members" \
                           if applicant.is_small_family else ""
        return result
 
    def _get_tier(self, applicant):
        ipp = applicant.income_per_person
        if ipp < 2500:  return ("Extremely Poor", "Rs. 15,000 / month")
        if ipp < 5000:  return ("Poor",           "Rs. 8,500 / month")
        if ipp < 8500:  return ("Vulnerable",     "Rs. 5,000 / month")
        return              ("Near Threshold",    "Rs. 2,500 / month")
 
class ElderlyBenefit(Benefit):
    """
    Elderly Persons' Allowance.
    580,944 adults receiving this as of 2025.
    Age 70+ threshold. Paid alongside Aswesuma.
    """
    def __init__(self):
        super().__init__()
        self.name    = "Elderly Persons' Allowance"
        self.name_si = "වැඩිහිටි දීමනාව"
        self.icon    = "👴"
        self.amount  = "Rs. 3,000 / month per person"
        self.where   = "Department of Social Services"
        self.hotline = "011-2186 000"
        self.steps   = [
            "Visit the Department of Social Services",
            "Bring NIC and birth certificate of the elderly person",
            "Fill the elderly allowance application form",
            "Allowance paid monthly to a nominated bank account",
            "Can receive alongside Aswesuma — separate benefit",
        ]
 
    def is_eligible(self, applicant):
        return applicant.has_elderly
 
 
class DisabilityBenefit(Benefit):
    """
    Disability Allowance + Kidney Patient Allowance.
    Administered by Department of Social Services.
    """
    def __init__(self):
        super().__init__()
        self.name    = "Disability Allowance"
        self.name_si = "ආබාධිත දීමනාව"
        self.icon    = "♿"
        self.amount  = "Rs. 3,000 / month"
        self.where   = "Department of Social Services"
        self.hotline = "011-2186 000"
        self.steps   = [
            "Get a disability certificate from a government hospital",
            "Visit the Department of Social Services with the certificate",
            "Bring your NIC and medical records",
            "Submit application — approved within 30 days",
            "Paid monthly to bank account. Can receive alongside Aswesuma.",
        ]
 
    def is_eligible(self, applicant):
        return applicant.has_disabled
 
 
class MaternityBenefit(Benefit):
    """
    Pregnant Mother's Allowance.
    Cash transfer + free Thriposha nutritional supplement.
    """
    def __init__(self):
        super().__init__()
        self.name    = "Pregnant Mother's Allowance"
        self.name_si = "ගර්භිණී මාතා දීමනාව"
        self.icon    = "🤱"
        self.amount  = "Cash transfer + free Thriposha nutrition supplement"
        self.where   = "Nearest Public Health Midwife (PHM) clinic"
        self.hotline = "1990 (Suwa Seriya)"
        self.steps   = [
            "Register at your nearest Public Health Midwife (PHM) immediately",
            "Attend all prenatal clinic appointments — free at government hospitals",
            "Apply at Divisional Secretariat for the cash transfer",
            "Receive Thriposha nutritional supplement free through MOH clinics",
        ]
 
    def is_eligible(self, applicant):
        return applicant.has_pregnant
 
 
class ScholarshipBenefit(Benefit):
    """
    President's Fund School Scholarship.
    Rs. 3,000/month for up to 12 months per year.
    Government schools, Grades 1–11.
    """
    def __init__(self):
        super().__init__()
        self.name    = "President's Fund School Scholarship"
        self.name_si = "ජනාධිපති අරමුදල් ශිෂ්‍යත්වය"
        self.icon    = "📚"
        self.amount  = "Rs. 3,000 / month (up to 12 months per year)"
        self.where   = "Through your child's school principal"
        self.hotline = "011-2354 354"
        self.steps   = [
            "Apply through your child's school principal",
            "Bring NIC, child's birth certificate, and income proof",
            "Income means test conducted by the school",
            "Scholarship credited at the start of each term",
            "Grades 1–5: need 50%+ competency. Grades 6–11: top 20 in class.",
        ]
 
    def is_eligible(self, applicant):
        return applicant.has_children and applicant.income_per_person < 10000
 
 
class HousingBenefit(Benefit):
    """
    State Housing Assistance.
    For families with no permanent home.
    """
    def __init__(self):
        super().__init__()
        self.name    = "State Housing Assistance"
        self.name_si = "රාජ්‍ය නිවාස ආධාර"
        self.icon    = "🏗️"
        self.amount  = "Housing grant — amount varies by program"
        self.where   = "National Housing Development Authority (NHDA)"
        self.hotline = "011-2696 031"
        self.steps   = [
            "Visit the National Housing Development Authority (NHDA)",
            "Bring NIC and proof of lack of permanent housing",
            "Apply for the relevant housing grant program",
            "Field assessment conducted by NHDA officer",
        ]
 
    def is_eligible(self, applicant):
        return applicant.housing == "none"
 
 

class EligibilityChecker:
    def __init__(self):
        # Load all benefit types — add new ones here easily
        self.benefits = [
            AswesumaBenefit(),
            ElderlyBenefit(),
            DisabilityBenefit(),
            MaternityBenefit(),
            ScholarshipBenefit(),
            HousingBenefit(),
        ]
 
    def check(self, applicant):
        """
        Run every benefit's eligibility check against this applicant.
        Returns a list of benefit result dicts the family qualifies for.
        """
        results = []
        for benefit in self.benefits:
            if benefit.is_eligible(applicant):
                results.append(benefit.get_result(applicant))
        return results
 
 
            
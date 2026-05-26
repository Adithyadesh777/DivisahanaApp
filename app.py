#deployment of Divishana app 

from flask import Flask, render_template,request,session 
from models import Applicant, EligibilityChecker

app = Flask(__name__)
app.secret_key = "divisahana_secret_2026"  # Replace with a real secret key


DISTRICTS = [
    "Colombo", "Gampaha", "Kalutara", "Kandy", "Matale",
    "Nuwara Eliya", "Galle", "Matara", "Hambantota", "Jaffna",
    "Kilinochchi", "Mannar", "Vavuniya", "Mullaitivu", "Batticaloa",
    "Ampara", "Trincomalee", "Kurunegala", "Puttalam", "Anuradhapura",
    "Polonnaruwa", "Badulla", "Monaragala", "Ratnapura", "Kegalle"
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", districts=DISTRICTS)
 
@app.route("/check", methods=["POST"])
def check():

    district       = request.form.get("district", "")
    family_size    = request.form.get("family_size", 1)
    monthly_income = request.form.get("monthly_income", 0)
    employment     = request.form.get("employment", "")
    housing        = request.form.get("housing", "")
 
    # Checkboxes — these come through only if ticked
    has_elderly  = "has_elderly"  in request.form
    has_disabled = "has_disabled" in request.form
    has_children = "has_children" in request.form
    has_pregnant = "has_pregnant" in request.form
 
    applicant = Applicant(
        district       = district,
        family_size    = family_size,
        monthly_income = monthly_income,
        employment     = employment,
        has_elderly    = has_elderly,
        has_disabled   = has_disabled,
        has_children   = has_children,
        has_pregnant   = has_pregnant,
        housing        = housing,
    )
 
    # ── Step 3: Run the eligibility checker ──────────────────────────────────
    checker = EligibilityChecker()
    qualified_benefits = checker.check(applicant)
 
    # ── Step 4: Send results to the result page ───────────────────────────────
    return render_template(
        "result.html",
        applicant  = applicant,
        benefits   = qualified_benefits,
        count      = len(qualified_benefits),
        district   = district,
        income_pp  = round(applicant.income_per_person),
    )
 

if __name__ == "__main__":
    app.run(debug=True)
 

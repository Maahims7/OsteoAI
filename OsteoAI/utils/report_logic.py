
# bone deficiency and prescription logic

def estimate_expected_density(age, sex):
    """Estimate expected bone density based on age and sex"""
    base = 100
    if sex.lower() in ['female', 'f']:
        base -= 5
    if age > 60:
        base -= 10
    elif age > 50:
        base -= 5
    return base


def calculate_deficiency(expected, actual):
    """Calculate bone density deficiency percentage"""
    return expected - actual


def classify_risk(deficiency):
    """Classify risk category based on deficiency percentage"""
    if deficiency <= 5:
        return 'Normal'
    elif deficiency <= 15:
        return 'Mild'
    elif deficiency <= 25:
        return 'Moderate'
    else:
        return 'Severe'


def generate_prescription(age, sex, weight, deficiency, risk_category):
    """
    Generate personalized vitamin and food recommendations
    based on age, sex, weight, and deficiency level
    """
    disclaimer = '⚠️ This is AI-assisted screening, not a medical diagnosis. Consult healthcare professionals.'
    prescriptions = []
    
    # Base recommendations by risk level
    if risk_category == 'Normal':
        prescriptions.append('💚 Maintain healthy lifestyle with balanced diet')
        prescriptions.append('🚴 Continue regular physical activity (150 min/week)')
        prescriptions.append('☀️ Daily sun exposure: 15-30 minutes')
        prescriptions.append('🥛 Include calcium-rich foods in daily diet')
        
    elif risk_category == 'Mild':
        prescriptions.append('💛 Increase sun exposure to 20-30 minutes daily')
        prescriptions.append('🥛 Calcium intake: 800-1000 mg daily')
        if weight < 70:
            prescriptions.append('💊 Vitamin D3: 800 IU daily')
        else:
            prescriptions.append('💊 Vitamin D3: 1000 IU daily')
        prescriptions.append('🍇 Recommended foods: Milk, yogurt, cheese, spinach, broccoli, almonds, sardines')
        prescriptions.append('🏋️ Resistance exercises: 2-3 times per week')
        
    elif risk_category == 'Moderate':
        prescriptions.append('🟠 Consult healthcare provider for evaluation')
        if sex.lower() in ['female', 'f'] and age >= 50:
            prescriptions.append('💊 Vitamin D3: 1000-2000 IU daily (higher dose recommended)')
        else:
            prescriptions.append('💊 Vitamin D3: 1000 IU daily')
        prescriptions.append('🥛 Calcium intake: 1000-1200 mg daily (consider supplements)')
        prescriptions.append('🍇 Foods: Fortified milk, yogurt, kale, bok choy, salmon, tuna, tofu')
        prescriptions.append('🏋️ Resistance training: 3-4 times per week')
        prescriptions.append('⏰ Avoid smoking and limit alcohol consumption')
        
    elif risk_category == 'Severe':
        prescriptions.append('🔴 URGENT: Schedule appointment with endocrinologist or rheumatologist')
        prescriptions.append('🏥 Request DEXA scan for precise bone density measurement')
        prescriptions.append('💊 Prescription medication evaluation (bisphosphonates, etc.)')
        prescriptions.append('💊 Vitamin D3: 2000 IU daily + Calcium: 1200-1500 mg daily')
        prescriptions.append('🍇 Foods as above + fortified cereals, orange juice, eggs')
        prescriptions.append('🏃 Gentle exercise: Walking, swimming (avoid high-impact)')
        prescriptions.append('⚠️ Fall prevention measures at home')
    
    # Age-specific recommendations
    if age > 60:
        prescriptions.append('👴 Age 60+: Consider additional vitamin K2-rich foods (natto, sauerkraut)')
    elif age >= 70:
        prescriptions.append('👵 Age 70+: Balance exercises for fall prevention recommended')
    
    # Sex-specific recommendations
    if sex.lower() in ['female', 'f']:
        if 45 <= age <= 55:
            prescriptions.append('🌺 Perimenopause period: Enhanced calcium intake critical')
        elif age > 55:
            prescriptions.append('🌺 Postmenopausal: Monitor bone density regularly (DEXA scan every 1-2 years)')
    
    # Weight-based recommendations
    if weight < 60:
        prescriptions.append('⚠️ Low body weight increases fracture risk - extra care needed')
    elif weight > 100:
        prescriptions.append('✓ Higher body weight provides some bone density protection')
    
    # General lifestyle
    prescriptions.append('😴 Sleep: 7-9 hours per night for bone health')
    prescriptions.append('🚫 Avoid: Excessive caffeine, carbonated drinks with phosphates')
    
    return prescriptions, disclaimer


def create_pdf_report(data, output_path):
    """Optional PDF generator using reportlab"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        y = height - 50

        c.setFont('Helvetica-Bold', 16)
        c.drawString(50, y, 'OsteoAI Patient Report')
        y -= 40

        c.setFont('Helvetica', 12)
        for key, value in data.items():
            c.drawString(50, y, f"{key}: {value}")
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False

import random
from fpdf import FPDF
import os

# Define job roles and their associated details
job_roles = [
    ("Software Engineer", ["Python", "Java", "SQL", "Machine Learning"], "Bachelor's in Computer Science", ["AWS Certified Developer"]),
    ("Data Scientist", ["Python", "R", "Statistics", "Data Analysis"], "Master's in Data Science", ["Google Data Analytics"]),
    ("Marketing Manager", ["SEO", "Social Media", "Branding", "Google Ads"], "MBA in Marketing", ["Google Ads Certification"]),
    ("Mechanical Engineer", ["AutoCAD", "SolidWorks", "Thermodynamics"], "Bachelor's in Mechanical Engineering", ["PE License"]),
    ("Teacher", ["Curriculum Design", "Classroom Management", "Educational Technology"], "Master's in Education", ["Teaching Certification"]),
    ("Accountant", ["Financial Reporting", "QuickBooks", "Tax Preparation"], "Bachelor's in Accounting", ["CPA"]),
    ("Graphic Designer", ["Photoshop", "Illustrator", "Typography"], "Diploma in Graphic Design", ["Adobe Certified Expert"]),
    ("HR Specialist", ["Recruitment", "Employee Relations", "Payroll"], "Bachelor's in Human Resources", ["SHRM Certified"]),
    ("Nurse", ["Patient Care", "Medical Records", "Emergency Response"], "Bachelor's in Nursing", ["RN License"]),
    ("Construction Worker", ["Blueprint Reading", "Concrete Mixing", "Power Tools"], "High School Diploma", []),
    ("Electrician", ["Wiring", "Circuit Testing", "Blueprint Reading"], "Vocational Training", ["Electrician License"]),
    ("Journalist", ["Writing", "Editing", "Interviewing"], "Bachelor's in Journalism", []),
    ("Sales Representative", ["Customer Relations", "Negotiation", "CRM Software"], "Associate's in Business", []),
    ("Restaurant Manager", ["Inventory Management", "Staff Training", "Customer Service"], "Diploma in Hospitality", []),
    ("UX Designer", ["Figma", "User Research", "Prototyping"], "Bachelor's in Interaction Design", []),
    ("Pilot", ["Flight Planning", "Aircraft Maintenance", "Navigation"], "Bachelor's in Aviation", ["FAA Commercial Pilot License"]),
    ("Biologist", ["Lab Research", "Data Analysis", "Field Studies"], "Master's in Biology", []),
    ("Security Guard", ["Surveillance", "Conflict Resolution", "CPR"], "High School Diploma", ["Security Certification"]),
    ("Pharmacist", ["Prescription Handling", "Medical Knowledge", "Customer Service"], "Doctorate in Pharmacy", ["Pharmacist License"]),
    ("Artist", ["Painting", "Sculpting", "Art Theory"], "Fine Arts Degree", [])
]

# Function to generate work experience
def generate_experience(role):
    years = random.randint(2, 10)
    exp = [
        (f"{role} at Company A", f"201{random.randint(0, 5)} - 201{random.randint(6, 9)}"),
        (f"{role} at Company B", f"201{random.randint(2, 6)} - Present")
    ]
    return exp

# Function to generate a resume
def generate_resume(role, skills, education, certifications):
    name = random.choice(["John Doe", "Jane Smith", "Michael Johnson", "Emily Davis", "David Brown", "Bob TheBuilder"])
    contact = f"Email: {name.replace(' ', '').lower()}@example.com | Phone: (555) {random.randint(100,999)}-{random.randint(1000,9999)}"
    summary = f"A dedicated and skilled {role} with experience in {', '.join(skills[:3])}. Passionate about delivering quality results."

    experience = generate_experience(role)
    projects = [f"{role} Portfolio Website", f"Contributed to {role} Open Source Project"]

    resume_text = f"""
    {name}
    {contact}

    Summary:
    {summary}

    Skills:
    {', '.join(skills)}

    Work Experience:
    """

    for job, duration in experience:
        resume_text += f"\n    - {job} ({duration})"

    resume_text += f"\n\nEducation:\n    {education}"

    if certifications:
        resume_text += f"\n\nCertifications:\n    {', '.join(certifications)}"

    resume_text += f"\n\nProjects:\n    {', '.join(projects)}"

    return name, resume_text

# Function to format text into paragraphs for PDF
def format_text_for_pdf(text, max_line_length=90):
    formatted_text = ""
    words = text.split()
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > max_line_length:
            formatted_text += line.strip() + "\n"
            line = ""
        line += word + " "
    
    formatted_text += line.strip()  # Add the last line
    return formatted_text

# Updated function to save resume as PDF with text wrapping
def save_resume_as_pdf(resume_text, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section in resume_text.split("\n"):
        formatted_section = format_text_for_pdf(section)
        pdf.multi_cell(0, 10, formatted_section)
        pdf.ln(5)  # Add spacing between sections

    pdf.output(filename)

# Regenerate and save properly formatted resumes
output_dir = "resumes"
os.makedirs(output_dir, exist_ok=True)

for i, (role, skills, education, certifications) in enumerate(random.sample(job_roles * 2, 20)):
    name, resume_text = generate_resume(role, skills, education, certifications)
    filename = os.path.join(output_dir, f"resume_{i+1}.pdf")
    save_resume_as_pdf(resume_text, filename)

# Show the directory where fixed resumes are saved
output_dir

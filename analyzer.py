import pydicom
import os
from colorama import Fore, Style, init

init(autoreset=True)

# --- These are the fields that contain private patient info ---
SENSITIVE_FIELDS = [
    "PatientName",
    "PatientID",
    "PatientBirthDate",
    "PatientSex",
    "PatientAge",
    "InstitutionName",
    "ReferringPhysicianName",
    "StudyDate",
    "PatientAddress",
    "PatientTelephoneNumbers"
]

def analyze_dicom(file_path):
    print(f"\n{'='*50}")
    print(f"📂 Analyzing file: {file_path}")
    print(f"{'='*50}")

    # Load the DICOM file
    try:
        ds = pydicom.dcmread(file_path)
    except Exception as e:
        print(Fore.RED + f"❌ Could not read file: {e}")
        return

    found_sensitive = []

    # Check each sensitive field
    for field in SENSITIVE_FIELDS:
        if hasattr(ds, field):
            value = getattr(ds, field)
            print(Fore.RED + f"⚠️  FOUND sensitive field  →  {field}: {value}")
            found_sensitive.append(field)
        else:
            print(Fore.GREEN + f"✅ Not present           →  {field}")

    # Summary
    print(f"\n{'='*50}")
    if found_sensitive:
        print(Fore.YELLOW + f"🔐 RESULT: {len(found_sensitive)} sensitive field(s) found! Patient privacy at risk.")
    else:
        print(Fore.GREEN + "🎉 RESULT: No sensitive data found. File looks clean!")
    print(f"{'='*50}\n")

def anonymize_dicom(file_path):
    ds = pydicom.dcmread(file_path)
    for field in SENSITIVE_FIELDS:
        if hasattr(ds, field):
            setattr(ds, field, "ANONYMIZED")
    
    # Save the cleaned file
    new_path = file_path.replace(".dcm", "_anonymized.dcm")
    ds.save_as(new_path)
    print(Fore.CYAN + f"\n✅ Anonymized file saved as: {new_path}")

# --- MAIN PROGRAM ---
print(Fore.CYAN + "\n🏥 DICOM Security Analyzer")
print("="*50)

file = input("Enter the path to your .dcm file: ").strip()

if not os.path.exists(file):
    print(Fore.RED + "❌ File not found. Check the path and try again.")
else:
    analyze_dicom(file)
    choice = input("\nDo you want to anonymize (remove) sensitive data? (yes/no): ").strip().lower()
    if choice == "yes":
        anonymize_dicom(file)
    else:
        print("\nOkay! No changes made to the file.")
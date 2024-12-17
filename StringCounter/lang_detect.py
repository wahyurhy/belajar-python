# pip install pyinstaller
# pip install prettytable openpyxl langdetect
# pyinstaller --onefile count_words.py

import xml.etree.ElementTree as ET
from collections import Counter
import re
from tkinter import Tk, filedialog
from prettytable import PrettyTable  # For tabular display
import openpyxl  # For Excel file creation
from langdetect import detect  # For language detection

# Example specialized dictionaries
LEGAL_TERMS = {
    "contract", "law", "agreement", "liability", "jurisdiction", 
    "litigation", "arbitration", "appeal", "plaintiff", "defendant",
    "witness", "testimony", "evidence", "subpoena", "verdict",
    "damages", "settlement", "breach", "clause", "amendment",
    "dispute", "arbitrator", "legal", "counsel", "attorney",
    "barrister", "solicitor", "prosecutor", "defense", "trial",
    "judge", "court", "constitution", "statute", "regulation",
    "ordinance", "decree", "precedent", "common law", "civil law",
    "penalty", "injunction", "tort", "negligence", "compensation",
    "fiduciary", "contractual", "breach of contract", "trust",
    "property", "ownership", "intellectual property", "copyright",
    "trademark", "patent", "licensing", "liquidation", "bankruptcy",
    "fraud", "embezzlement", "money laundering", "compliance",
    "policy", "code of conduct", "non-disclosure", "confidentiality",
    "warranty", "guarantee", "indemnity", "litigator", "hearing",
    "motion", "plea", "judgment", "enforcement", "mediation",
    "conciliation", "rescission", "novation", "force majeure",
    "arbitral", "litigant", "perjury", "probate", "equity",
    "due diligence", "malpractice", "libel", "slander",
    "civil rights", "human rights", "appealable", "injurious",
    "liable", "non-compete", "arrest", "detention", "bail",
    "parole", "probation", "sentence", "acquittal", "guilty",
    "innocent", "public defender", "pro bono", "criminal",
    "civil", "penal code", "code of law", "legal framework",
    "legislation", "bylaw", "injury", "statutory", "jurisprudence",
    "adjudication", "notary", "affidavit", "power of attorney",
    "proxy", "treaty", "diplomatic immunity", "extradition",
    "search warrant", "arrest warrant", "civil litigation",
    "criminal prosecution", "case law", "discovery process",
    "interrogation", "deposition", "probative", "inquisition",
    "admissible", "inadmissible", "beyond reasonable doubt",
    "presumption of innocence", "burden of proof", "summary judgment",
    "voir dire", "class action", "injunctive relief", "statute of limitations",
    "precedential", "amicus curiae", "habeas corpus", "ex post facto",
    "mens rea", "actus reus", "stare decisis", "ultra vires"
}
MEDICAL_TERMS = {
    "diagnosis", "treatment", "therapy", "symptom", "prescription",
    "anatomy", "pathology", "prognosis", "disease", "infection",
    "immunity", "vaccine", "surgery", "rehabilitation", "pharmacology",
    "antibiotic", "antiviral", "antifungal", "antiseptic", "immunotherapy",
    "radiology", "ultrasound", "biopsy", "chemotherapy", "oncology",
    "cardiology", "neurology", "gastroenterology", "hematology", "orthopedics",
    "dermatology", "psychiatry", "pediatrics", "geriatrics", "nephrology",
    "endocrinology", "gynecology", "obstetrics", "ophthalmology", "urology",
    "pulmonology", "pathogen", "parasite", "virus", "bacteria",
    "fungus", "epidemiology", "pandemic", "outbreak", "quarantine",
    "symptomatology", "prophylaxis", "palliative", "clinical", "acute",
    "chronic", "infectious", "noninfectious", "contagious", "noncontagious",
    "allergy", "inflammation", "rash", "fever", "nausea",
    "vomiting", "diarrhea", "constipation", "fatigue", "pain",
    "headache", "migraine", "dizziness", "shortness of breath", "cough",
    "sore throat", "swelling", "bleeding", "fracture", "dislocation",
    "burn", "laceration", "bruise", "ulcer", "lesion",
    "tumor", "cancer", "carcinoma", "sarcoma", "benign",
    "malignant", "metastasis", "anemia", "diabetes", "hypertension",
    "stroke", "heart attack", "arrhythmia", "hypotension", "cholesterol",
    "arteriosclerosis", "atherosclerosis", "embolism", "thrombosis", "aneurysm",
    "pneumonia", "asthma", "bronchitis", "emphysema", "tuberculosis",
    "allergic rhinitis", "sinusitis", "COPD", "COVID-19", "HIV",
    "AIDS", "measles", "chickenpox", "dengue", "malaria",
    "typhoid", "hepatitis", "liver disease", "kidney disease", "renal failure",
    "dialysis", "urinary tract infection", "bladder", "prostate", "gynecological",
    "pregnancy", "childbirth", "neonatology", "genetics", "mutation",
    "genetic disorder", "hereditary", "chromosome", "DNA", "RNA",
    "protein", "enzymes", "hormones", "endocrine", "metabolism",
    "obesity", "malnutrition", "eating disorders", "mental health", "depression",
    "anxiety", "schizophrenia", "bipolar disorder", "post-traumatic stress disorder", "psychosis",
    "therapy", "psychotherapy", "cognitive behavioral therapy", "physical therapy", "occupational therapy",
    "speech therapy", "palliative care", "home care", "hospice", "first aid",
    "defibrillator", "resuscitation", "emergency", "triage", "ICU",
    "hospital", "clinic", "pharmacy", "pharmacist", "medication",
    "dose", "side effect", "contraindication", "interaction", "placebo",
    "clinical trial", "protocol", "randomized controlled trial", "double-blind", "efficacy",
    "compliance", "adherence", "patient", "doctor", "nurse",
    "technician", "specialist", "primary care", "general practitioner", "consultant"
}
TECHNICAL_TERMS = {
    "algorithm", "data", "network", "protocol", "encryption",
    "authentication", "authorization", "firewall", "debugging", "compiler",
    "interpreter", "virtualization", "containerization", "cloud", "database",
    "query", "index", "schema", "data mining", "data warehousing",
    "machine learning", "deep learning", "artificial intelligence", "neural network", "supervised learning",
    "unsupervised learning", "reinforcement learning", "API", "endpoint", "REST",
    "SOAP", "JSON", "XML", "HTTP", "HTTPS",
    "SSL", "TLS", "tokenization", "hashing", "blockchain",
    "cryptocurrency", "bitcoin", "smart contract", "hash function", "public key",
    "private key", "RSA", "AES", "SHA-256", "digital signature",
    "cybersecurity", "vulnerability", "exploit", "penetration testing", "phishing",
    "ransomware", "malware", "trojan", "virus", "worm",
    "backdoor", "zero-day", "patching", "SOC", "SIEM",
    "intrusion detection", "intrusion prevention", "DNS", "IP", "IPv4",
    "IPv6", "subnetting", "CIDR", "router", "switch",
    "load balancer", "bandwidth", "latency", "throughput", "QoS",
    "VPN", "proxy", "NAT", "firewall rules", "port forwarding",
    "programming", "scripting", "framework", "library", "module",
    "package", "dependency", "version control", "Git", "repository",
    "branch", "merge", "commit", "pull request", "CI/CD",
    "build", "pipeline", "automation", "orchestration", "Kubernetes",
    "Docker", "virtual machine", "hypervisor", "server", "client",
    "peer-to-peer", "distributed systems", "microservices", "monolithic architecture", "scalability",
    "availability", "fault tolerance", "redundancy", "load testing", "stress testing",
    "benchmarking", "deployment", "rollback", "hotfix", "debugger",
    "log", "exception", "stack trace", "memory leak", "garbage collection",
    "thread", "process", "mutex", "semaphore", "deadlock",
    "parallelism", "concurrency", "asynchronous", "synchronous", "event-driven",
    "stateful", "stateless", "cache", "buffer", "stream",
    "serialization", "deserialization", "binary", "hexadecimal", "compiler optimization",
    "refactoring", "code review", "unit testing", "integration testing", "system testing",
    "acceptance testing", "performance testing", "regression testing", "test case", "test suite",
    "debugging tools", "profiling", "code coverage", "mocking", "stubbing",
    "cloud computing", "IaaS", "PaaS", "SaaS", "serverless",
    "edge computing", "IoT", "sensor", "actuator", "big data",
    "Hadoop", "Spark", "data lake", "data pipeline", "ETL",
    "data visualization", "dashboard", "reporting", "business intelligence", "data governance",
    "metadata", "data integrity", "data consistency", "data redundancy", "data normalization",
    "foreign key", "primary key", "NoSQL", "SQL", "relational database",
    "graph database", "document database", "key-value store", "columnar database", "time-series database",
    "distributed ledger", "consensus algorithm", "mining", "staking", "proof of work",
    "proof of stake", "sharding", "replication", "CAP theorem", "event sourcing"
}

def select_file_with_file_manager():
    """Open a file dialog to select strings.xml."""
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(
        title="Select strings.xml file",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def detect_language(word_list):
    """Detect the language of the file based on the words."""
    try:
        sample_text = " ".join(word_list[:50])  # Use the first 50 words for detection
        language = detect(sample_text)
        return language
    except:
        return "unknown"

def classify_words(word_list):
    """Classify words into general and specialized categories."""
    general_words = []
    specialized_words = {"legal": [], "medical": [], "technical": []}
    
    for word in word_list:
        if word in LEGAL_TERMS:
            specialized_words["legal"].append(word)
        elif word in MEDICAL_TERMS:
            specialized_words["medical"].append(word)
        elif word in TECHNICAL_TERMS:
            specialized_words["technical"].append(word)
        else:
            general_words.append(word)
    
    return general_words, specialized_words

def count_words_and_list_in_strings_xml(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        if root.tag != 'resources':
            raise ValueError("Invalid XML file with no 'resources' root element.")
        
        word_list = []
        word_pattern = re.compile(r'\b\w+\b')
        
        for string_element in root.findall('string'):
            if string_element.text:
                words = word_pattern.findall(string_element.text.lower())
                filtered_words = [word for word in words if len(word) > 1]
                word_list.extend(filtered_words)
        
        total_words = len(word_list)
        word_count = Counter(word_list)
        return total_words, word_count, word_list
    except FileNotFoundError:
        print("The file was not found.")
    except ET.ParseError:
        print("The file is not a valid XML file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def display_classified_words(general_words, specialized_words):
    """Display classified words."""
    print("\n=== General Words ===")
    print(", ".join(general_words))
    
    print("\n=== Specialized Words ===")
    for category, words in specialized_words.items():
        print(f"{category.capitalize()} Words: {', '.join(words)}")

if __name__ == "__main__":
    summary_data = []

    while True:
        file_path = select_file_with_file_manager()
        if not file_path:
            print("No file selected.")
            break

        try:
            total_words, word_count, word_list = count_words_and_list_in_strings_xml(file_path)
            language = detect_language(word_list)
            general_words, specialized_words = classify_words(word_list)
            
            print(f"\nDetected Language: {language}")
            display_classified_words(general_words, specialized_words)
            
            table = PrettyTable()
            table.field_names = ["Word", "Count"]
            for word, count in word_count.items():
                table.add_row([word, count])
            print(table)
            
            summary_data.append({
                "file_name": file_path.split("/")[-1],
                "total_words": total_words,
                "general_words": len(general_words),
                "specialized_words": {
                    "legal": len(specialized_words["legal"]),
                    "medical": len(specialized_words["medical"]),
                    "technical": len(specialized_words["technical"]),
                }
            })

            # Display summary
            print("\n=== Summary Data ===")
            summary_table = PrettyTable()
            summary_table.field_names = ["File Name", "Total Words", "General Words", "Legal Words", "Medical Words", "Technical Words"]
            for data in summary_data:
                summary_table.add_row([
                    data["file_name"],
                    data["total_words"],
                    data["general_words"],
                    data["specialized_words"]["legal"],
                    data["specialized_words"]["medical"],
                    data["specialized_words"]["technical"],
                ])
            print(summary_table)

            continue_choice = input("Do you want to process another file? (yes/no): ").strip().lower()
            if continue_choice != "yes":
                print("Goodbye!")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
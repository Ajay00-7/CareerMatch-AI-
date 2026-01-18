import json
import os

# Define the new roles with basic skill mappings
new_roles = {
    # AI / ML
    "AI Engineer": {"required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "NLP"], "weights": {"Python": 2, "TensorFlow": 3, "PyTorch": 3}},
    "Machine Learning Engineer": {"required_skills": ["Python", "Scikit-learn", "Modeling", "Deployment", "SQL", "Statistics"], "weights": {"Scikit-learn": 3, "Modeling": 3}},
    "Deep Learning Engineer": {"required_skills": ["Python", "Neural Networks", "CNN", "RNN", "Keras", "TensorFlow"], "weights": {"Neural Networks": 3, "CNN": 2}},
    "NLP Engineer": {"required_skills": ["Python", "NLTK", "Spacy", "Transformers", "BERT", "Linguistics"], "weights": {"Transformers": 3, "NLP": 3}},
    "Computer Vision Engineer": {"required_skills": ["Python", "OpenCV", "Image Processing", "Deep Learning", "CNN", "YOLO"], "weights": {"OpenCV": 3, "Image Processing": 3}},
    "Speech/Voice AI Engineer": {"required_skills": ["Python", "Signal Processing", "ASR", "TTS", "Audio Processing", "Deep Learning"], "weights": {"Signal Processing": 3, "ASR": 3}},
    "Reinforcement Learning Engineer": {"required_skills": ["Python", "Reinforcement Learning", "OpenAI Gym", "PyTorch", "Algorithms", "Mathematics"], "weights": {"Reinforcement Learning": 3}},
    "Applied Scientist": {"required_skills": ["Python", "Machine Learning", "Statistics", "Research", "Experimentation", "Data Analysis"], "weights": {"Research": 3, "Experimentation": 2}},
    "Research Scientist (AI)": {"required_skills": ["Python", "Research", "Publications", "Deep Learning", "Mathematics", "Algorithms"], "weights": {"Research": 3, "Publications": 2}},
    "Algorithm Engineer": {"required_skills": ["C++", "Python", "Data Structures", "Algorithms", "Optimization", "Mathematics"], "weights": {"Algorithms": 3, "Optimization": 3}},
    "Prompt Engineer": {"required_skills": ["LLMs", "Prompt Engineering", "Python", "Creative Writing", "NLP", "AI Ethics"], "weights": {"Prompt Engineering": 3, "LLMs": 3}},
    "Generative AI Engineer": {"required_skills": ["Python", "Generative AI", "GANs", "Diffusion Models", "Transformers", "PyTorch"], "weights": {"Generative AI": 3, "Diffusion Models": 3}},
    "MLOps Engineer": {"required_skills": ["Python", "Docker", "Kubernetes", "MLflow", "CI/CD", "Model Monitoring"], "weights": {"MLOps": 3, "Kubernetes": 2}},

    # Data
    "Data Scientist": {"required_skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization", "Pandas"], "weights": {"Statistics": 3, "Machine Learning": 3}},
    "Data Analyst": {"required_skills": ["SQL", "Excel", "Data Visualization", "Tableau", "Power BI", "Statistics"], "weights": {"SQL": 3, "Tableau": 2}},
    "Business Analyst": {"required_skills": ["Requirements Gathering", "SQL", "Process Modeling", "Communication", "Data Analysis", "Agile"], "weights": {"Requirements Gathering": 3, "Communication": 2}},
    "Business Intelligence Analyst": {"required_skills": ["SQL", "Power BI", "Tableau", "Data Warehousing", "ETL", "Reporting"], "weights": {"Power BI": 3, "Reporting": 2}},
    "Data Engineer": {"required_skills": ["Python", "SQL", "Spark", "Hadoop", "ETL", "AWS"], "weights": {"Spark": 3, "ETL": 3}},
    "Big Data Engineer": {"required_skills": ["Spark", "Hadoop", "Kafka", "Scala", "NoSQL", "Cloud"], "weights": {"Big Data": 3, "Kafka": 2}},
    "Data Architect": {"required_skills": ["Data Modeling", "Database Design", "SQL", "NoSQL", "Cloud Architecture", "Governance"], "weights": {"Data Modeling": 3, "Database Design": 3}},
    "Data Modeler": {"required_skills": ["Data Modeling", "ER Diagrams", "SQL", "Database Design", "Normalization", "Dimensional Modeling"], "weights": {"Data Modeling": 3}},
    "Statistician": {"required_skills": ["Statistics", "R", "SAS", "Mathematics", "Data Analysis", "Hypothesis Testing"], "weights": {"Statistics": 3, "R": 2}},
    "Quantitative Analyst": {"required_skills": ["Mathematics", "Python", "C++", "Financial Modeling", "Statistics", "Algorithms"], "weights": {"Mathematics": 3, "Financial Modeling": 3}},
    "ETL Developer": {"required_skills": ["ETL", "SQL", "Informatica", "Talend", "Data Warehousing", "SSIS"], "weights": {"ETL": 3, "SQL": 2}},
    "Database Administrator (DBA)": {"required_skills": ["SQL", "Database Management", "Backup/Recovery", "Performance Tuning", "Oracle", "PostgreSQL"], "weights": {"Database Management": 3}},

    # Web
    "Front-End Developer": {"required_skills": ["JavaScript", "HTML", "CSS", "React", "Unknown Framework", "Responsive Design"], "weights": {"JavaScript": 3, "React": 3}},
    "Back-End Developer": {"required_skills": ["Python", "Java", "Node.js", "SQL", "API", "Server"], "weights": {"API": 3, "SQL": 2}},
    "Full-Stack Developer": {"required_skills": ["JavaScript", "Python/Node", "React", "SQL", "HTML/CSS", "Git"], "weights": {"JavaScript": 2, "React": 2}},
    "Web Application Developer": {"required_skills": ["Web Development", "JavaScript", "HTML", "CSS", "Backend", "Database"], "weights": {"Web Development": 3}},
    "JavaScript Developer": {"required_skills": ["JavaScript", "ES6+", "React", "Node.js", "HTML", "CSS"], "weights": {"JavaScript": 3}},
    "UI Developer": {"required_skills": ["HTML", "CSS", "JavaScript", "UI Design", "Responsive Design", "Figma"], "weights": {"UI Design": 3}},
    "React Developer": {"required_skills": ["React", "JavaScript", "Redux", "Hooks", "HTML", "CSS"], "weights": {"React": 3}},
    "Angular Developer": {"required_skills": ["Angular", "TypeScript", "RxJS", "JavaScript", "HTML", "CSS"], "weights": {"Angular": 3}},
    "Vue Developer": {"required_skills": ["Vue.js", "JavaScript", "Vuex", "HTML", "CSS", "Composition API"], "weights": {"Vue.js": 3}},

    # Mobile
    "Android Developer": {"required_skills": ["Kotlin", "Java", "Android Studio", "XML", "Jetpack Compose", "Git"], "weights": {"Kotlin": 3, "Android Studio": 3}},
    "iOS Developer": {"required_skills": ["Swift", "iOS", "Xcode", "UIKit", "SwiftUI", "Git"], "weights": {"Swift": 3, "iOS": 3}},
    "Flutter Developer": {"required_skills": ["Flutter", "Dart", "Mobile App Development", "Widgets", "State Management", "Git"], "weights": {"Flutter": 3, "Dart": 3}},
    "React Native Developer": {"required_skills": ["React Native", "JavaScript", "Mobile App Development", "Redux", "Git", "API"], "weights": {"React Native": 3}},
    "Mobile App Engineer": {"required_skills": ["Mobile Development", "iOS", "Android", "API Integration", "Git", "UI/UX"], "weights": {"Mobile Development": 3}},

    # Software
    "Software Engineer": {"required_skills": ["Programming", "Data Structures", "Algorithms", "System Design", "Git", "Debugging"], "weights": {"Programming": 3, "System Design": 2}},
    "Software Developer": {"required_skills": ["Coding", "Testing", "Debugging", "Agile", "Git", "Problem Solving"], "weights": {"Coding": 3}},
    "Application Developer": {"required_skills": ["App Development", "Programming", "Database", "API", "UI", "Logic"], "weights": {"App Development": 3}},
    "Systems Software Engineer": {"required_skills": ["C/C++", "OS Internals", "Linux", "Kernel", "Multithreading", "Performance"], "weights": {"C/C++": 3, "OS Internals": 3}},
    "Platform Engineer": {"required_skills": ["Kubernetes", "Cloud", "Infrastructure", "Go", "Python", "Linux"], "weights": {"Platform": 3}},
    "Embedded Systems Engineer": {"required_skills": ["C", "C++", "Microcontrollers", "RTOS", "Hardware", "Firmware"], "weights": {"Embedded": 3, "C": 3}},
    "Firmware Engineer": {"required_skills": ["C", "Assembly", "Microcontrollers", "Hardware", "Debugging", "Drivers"], "weights": {"Firmware": 3}},
    "C/C++ Developer": {"required_skills": ["C++", "C", "STL", "Memory Management", "Algorithms", "Linux"], "weights": {"C++": 3}},
    "Java Developer": {"required_skills": ["Java", "Spring Boot", "Hibernate", "SQL", "API", "Microservices"], "weights": {"Java": 3, "Spring Boot": 3}},
    "Python Developer": {"required_skills": ["Python", "Django", "Flask", "SQL", "API", "Scripting"], "weights": {"Python": 3}},
    ".NET Developer": {"required_skills": ["C#", ".NET Core", "ASP.NET", "SQL Server", "MVC", "API"], "weights": {".NET": 3, "C#": 3}},

    # Cloud
    "Cloud Engineer": {"required_skills": ["AWS", "Azure", "Linux", "Terraform", "Python", "Networking"], "weights": {"AWS": 3, "Cloud": 3}},
    "Cloud Solutions Architect": {"required_skills": ["Cloud Architecture", "AWS", "Azure", "Design", "Security", "Migration"], "weights": {"Cloud Architecture": 3}},
    "Cloud Administrator": {"required_skills": ["Cloud Management", "Monitoring", "Linux", "Security", "Scripting", "Backup"], "weights": {"Cloud Management": 3}},
    "Cloud DevOps Engineer": {"required_skills": ["DevOps", "CI/CD", "Kubernetes", "Terraform", "Cloud", "Jenkins"], "weights": {"DevOps": 3}},
    "Cloud Security Engineer": {"required_skills": ["Cloud Security", "IAM", "Compliance", "Network Security", "Encryption", "Python"], "weights": {"Cloud Security": 3}},
    "AWS/GCP/Azure Engineer": {"required_skills": ["AWS", "GCP", "Azure", "Cloud Services", "Infrastructure", "Deployment"], "weights": {"AWS": 2, "Azure": 2}},
    "Cloud Support Engineer": {"required_skills": ["Troubleshooting", "Cloud", "Networking", "Linux", "Customer Service", "Tickets"], "weights": {"Troubleshooting": 3}},
    "Site Reliability Engineer (SRE)": {"required_skills": ["Linux", "Python/Go", "Automation", "Monitoring", "Incident Response", "SLO"], "weights": {"SRE": 3}},
    "Infrastructure Engineer": {"required_skills": ["Infrastructure", "Networking", "Servers", "Virtualization", "Cloud", "Automation"], "weights": {"Infrastructure": 3}},

    # DevOps
    "DevOps Engineer": {"required_skills": ["CI/CD", "Docker", "Kubernetes", "Linux", "Jenkins", "Terraform"], "weights": {"CI/CD": 3, "Docker": 3}},
    "Automation Engineer": {"required_skills": ["Automation", "Scripting", "Python", "Ansible", "Jenkins", "Testing"], "weights": {"Automation": 3}},
    "Release Engineer": {"required_skills": ["Release Management", "CI/CD", "Git", "Versioning", "Build Tools", "Scripting"], "weights": {"Release Management": 3}},
    "CI/CD Engineer": {"required_skills": ["CI/CD", "Jenkins", "GitLab CI", "Pipeline", "Automation", "Docker"], "weights": {"CI/CD": 3}},
    "Kubernetes Engineer": {"required_skills": ["Kubernetes", "Docker", "Container Orchestration", "Helm", "Cloud", "Networking"], "weights": {"Kubernetes": 3}},
    "Container Engineer": {"required_skills": ["Docker", "Containers", "Kubernetes", "Linux", "Microservices", "Security"], "weights": {"Docker": 3}},

    # Cyber
    "Cybersecurity Engineer": {"required_skills": ["Security", "Network Security", "Firewalls", "Linux", "Tools", "Analysis"], "weights": {"Security": 3}},
    "Information Security Analyst": {"required_skills": ["InfoSec", "Risk Assessment", "Compliance", "Security Controls", "Auditing", "Documentation"], "weights": {"InfoSec": 3}},
    "SOC Analyst": {"required_skills": ["SIEM", "Splunk", "Incident Handling", "Monitoring", "Network Traffic", "Forensics"], "weights": {"SOC": 3, "SIEM": 3}},
    "Penetration Tester / Ethical Hacker": {"required_skills": ["Penetration Testing", "Ethical Hacking", "Burp Suite", "Kali Linux", "Exploitation", "Reporting"], "weights": {"Penetration Testing": 3}},
    "Network Security Engineer": {"required_skills": ["Network Security", "Firewalls", "VPN", "IDS/IPS", "Cisco", "Routing"], "weights": {"Network Security": 3}},
    "Security Architect": {"required_skills": ["Security Architecture", "Design", "Threat Modeling", "Compliance", "Cloud Security", "Encryption"], "weights": {"Security Architecture": 3}},
    "Application Security Engineer": {"required_skills": ["AppSec", "OWASP", "Code Review", "SAST/DAST", "DevSecOps", "Secure Coding"], "weights": {"AppSec": 3}},
    "Incident Response Analyst": {"required_skills": ["Incident Response", "Forensics", "Malware Analysis", "Security", "Documentation", "Communication"], "weights": {"Incident Response": 3}},
    "Cloud Security Analyst": {"required_skills": ["Cloud Security", "AWS/Azure", "Compliance", "IAM", "Monitoring", "Risk"], "weights": {"Cloud Security": 3}},

    # IT
    "System Administrator": {"required_skills": ["Linux", "Windows Server", "Active Directory", "Scripting", "Virtualization", "Backup"], "weights": {"Linux": 2, "Windows": 2}},
    "Linux Administrator": {"required_skills": ["Linux", "Bash", "Shell Scripting", "Networking", "Server Management", "Security"], "weights": {"Linux": 3}},
    "Windows Administrator": {"required_skills": ["Windows Server", "Active Directory", "PowerShell", "DNS", "Group Policy", "Azure AD"], "weights": {"Windows Server": 3}},
    "Network Administrator": {"required_skills": ["Networking", "Cisco", "Routing", "Switching", "TCP/IP", "Troubleshooting"], "weights": {"Networking": 3}},
    "IT Support Engineer": {"required_skills": ["Troubleshooting", "Hardware", "Software Help", "Windows/Mac", "Customer Service", "Ticket Systems"], "weights": {"Troubleshooting": 3}},
    "IT Helpdesk Technician": {"required_skills": ["Help Desk", "Technical Support", "Troubleshooting", "Windows", "Office 365", "Hardware"], "weights": {"Help Desk": 3}},
    "Hardware Engineer": {"required_skills": ["Hardware Design", "PCB", "Electronics", "Testing", "Circuit Design", "Soldering"], "weights": {"Hardware Design": 3}},

    # QA
    "QA Engineer": {"required_skills": ["QA", "Testing", "Bug Tracking", "Jira", "Test Cases", "Agile"], "weights": {"QA": 3}},
    "Software Test Engineer": {"required_skills": ["Testing", "Software Quality", "Regression Testing", "Manual Testing", "SQL", "Documentation"], "weights": {"Testing": 3}},
    "Manual Tester": {"required_skills": ["Manual Testing", "Test Cases", "Bug Reporting", "Jira", "UI Testing", "Attention to Detail"], "weights": {"Manual Testing": 3}},
    "Automation Tester (Selenium, Appium)": {"required_skills": ["Selenium", "Appium", "Java/Python", "Test Automation", "Scripting", "Frameworks"], "weights": {"Selenium": 3, "Automation": 3}},
    "Performance Tester": {"required_skills": ["Performance Testing", "JMeter", "LoadRunner", "Load Testing", "Analysis", "Monitoring"], "weights": {"Performance Testing": 3}},
    "Quality Analyst": {"required_skills": ["Quality Assurance", "Process Improvement", "Auditing", "Data Analysis", "Reporting", "Standards"], "weights": {"Quality Assurance": 3}},

    # Design
    "UI Designer": {"required_skills": ["UI Design", "Figma", "Sketch", "Wireframing", "Visual Design", "Prototyping"], "weights": {"UI Design": 3}},
    "UX Designer": {"required_skills": ["UX Design", "User Research", "Wireframing", "Prototyping", "Usability Testing", "Figma"], "weights": {"UX Design": 3}},
    "UX Researcher": {"required_skills": ["User Research", "Interviews", "Usability Testing", "Data Analysis", "Personas", "Reporting"], "weights": {"User Research": 3}},
    "Product Designer": {"required_skills": ["Product Design", "UX/UI", "Problem Solving", "Figma", "Design Systems", "Strategy"], "weights": {"Product Design": 3}},
    "Interaction Designer": {"required_skills": ["Interaction Design", "Motion", "Prototyping", "Figma", "User Flow", "Animation"], "weights": {"Interaction Design": 3}},
    "Graphic Designer": {"required_skills": ["Graphic Design", "Photoshop", "Illustrator", "InDesign", "Typography", "Branding"], "weights": {"Graphic Design": 3}},

    # Product
    "Business Analyst": {"required_skills": ["Business Analysis", "Requirements", "Documentation", "SQL", "Communication", "Process"], "weights": {"Business Analysis": 3}},
    "Product Manager": {"required_skills": ["Product Management", "Roadmap", "Strategy", "Agile", "User Stories", "Stakeholder Mgmt"], "weights": {"Product Management": 3}},
    "Product Owner": {"required_skills": ["Product Ownership", "Backlog", "User Stories", "Scrum", "Agile", "Prioritization"], "weights": {"Product Ownership": 3}},
    "Project Manager": {"required_skills": ["Project Management", "PMP", "Scheduling", "Risk Management", "Budgeting", "Leadership"], "weights": {"Project Management": 3}},
    "Program Manager": {"required_skills": ["Program Management", "Strategy", "Leadership", "Coordination", "Stakeholder Mgmt", "Reporting"], "weights": {"Program Management": 3}},
    "Scrum Master": {"required_skills": ["Scrum", "Agile", "Coaching", "Kanban", "Facilitation", "Jira"], "weights": {"Scrum": 3}},
    "Delivery Manager": {"required_skills": ["Delivery Management", "Agile", "Project Management", "Leadership", "Risk", "Planning"], "weights": {"Delivery Management": 3}},

    # IoT
    "IoT Developer": {"required_skills": ["IoT", "Embedded", "Python", "MQTT", "Sensors", "Cloud"], "weights": {"IoT": 3}},
    "IoT Embedded Engineer": {"required_skills": ["C", "C++", "RTOS", "Microcontrollers", "IoT", "Firmware"], "weights": {"Embedded": 3}},
    "Robotics Engineer": {"required_skills": ["Robotics", "ROS", "Python", "C++", "Control Systems", "Kinematics"], "weights": {"Robotics": 3}},
    "Mechatronics Engineer": {"required_skills": ["Mechatronics", "Electronics", "Mechanical", "Control Systems", "PLCs", "Automation"], "weights": {"Mechatronics": 3}},
    "Hardware Design Engineer": {"required_skills": ["Hardware Design", "PCB", "Schematics", "Testing", "FPGA", "Verilog"], "weights": {"Hardware Design": 3}},

    # Game
    "Game Developer": {"required_skills": ["Game Development", "C#", "C++", "Unity/Unreal", "3D Math", "Physics"], "weights": {"Game Development": 3}},
    "Unity Developer": {"required_skills": ["Unity", "C#", "Game Development", "3D", "Physics", "Scripting"], "weights": {"Unity": 3}},
    "Unreal Engine Developer": {"required_skills": ["Unreal Engine", "C++", "Blueprints", "Game Development", "3D", "Lighting"], "weights": {"Unreal Engine": 3}},
    "AR/VR Developer": {"required_skills": ["AR", "VR", "Unity", "C#", "3D", "Computer Vision"], "weights": {"AR": 3, "VR": 3}},

    # Research
    "Research Engineer": {"required_skills": ["Research", "Python", "Algorithms", "Prototyping", "Technical Writing", "Analysis"], "weights": {"Research": 3}},
    "R&D Engineer": {"required_skills": ["R&D", "Innovation", "Prototyping", "Engineering", "Testing", "Analysis"], "weights": {"R&D": 3}},
    "Research Associate": {"required_skills": ["Research", "Data Collection", "Analysis", "Literature Review", "Writing", "Statistics"], "weights": {"Research": 3}},
    "Applied Researcher": {"required_skills": ["Applied Research", "Machine Learning", "Prototyping", "Experimentation", "Python", "Problem Solving"], "weights": {"Applied Research": 3}},

    # Enterprise
    "ERP Consultant (SAP/Oracle)": {"required_skills": ["ERP", "SAP", "Oracle", "Business Processes", "Configuration", "Consulting"], "weights": {"ERP": 3, "SAP": 2}},
    "CRM Developer (Salesforce, Dynamics)": {"required_skills": ["CRM", "Salesforce", "Dynamics", "Apex", "Customization", "Integration"], "weights": {"CRM": 3}},
    "SAP ABAP Developer": {"required_skills": ["SAP", "ABAP", "ERP", "Reports", "Interfaces", "Fiori"], "weights": {"ABAP": 3, "SAP": 2}},

    # Digital
    "SEO Specialist": {"required_skills": ["SEO", "Google Analytics", "Keyword Research", "Content", "HTML", "Link Building"], "weights": {"SEO": 3}},
    "Digital Marketing Analyst": {"required_skills": ["Digital Marketing", "Analytics", "SEO/SEM", "Data Analysis", "Reporting", "Campaigns"], "weights": {"Digital Marketing": 3}},
    "Growth Engineer": {"required_skills": ["Growth Hacking", "Marketing", "Data Analysis", "Coding", "A/B Testing", "Experiments"], "weights": {"Growth Hacking": 3}},
    "Data Marketing Analyst": {"required_skills": ["Marketing Analytics", "SQL", "Tableau", "Data Analysis", "Statistics", "Python"], "weights": {"Marketing Analytics": 3}},

    # Support
    "Technical Support Engineer": {"required_skills": ["Technical Support", "Troubleshooting", "Customer Service", "Linux/Windows", "Documentation", "Communication"], "weights": {"Technical Support": 3}},
    "Customer Success Engineer": {"required_skills": ["Customer Success", "Technical Support", "Relationship Mgmt", "Product Knowledge", "Communication", "Onboarding"], "weights": {"Customer Success": 3}},
    "Solutions Engineer": {"required_skills": ["Solutions Engineering", "Sales", "Demo", "Technical Presentation", "Product", "Communication"], "weights": {"Solutions Engineering": 3}},
    "Solutions Architect": {"required_skills": ["Architecture", "Design", "Requirements", "Cloud", "Integration", "Leadership"], "weights": {"Architecture": 2}},
    "Technical Consultant": {"required_skills": ["Consulting", "Implementation", "Strategy", "Technical Knowledge", "Client Facing", "Problem Solving"], "weights": {"Consulting": 3}},
}

# Values to apply to all new roles if missing
DEFAULT_DESCRIPTION = "Role created from user request."

def update_roles():
    file_path = "d:/CareerMatch AI/data/job_roles.json"
    
    # Init existing
    existing_roles = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                existing_roles = json.load(f)
        except Exception as e:
            print(f"Error reading existing file: {e}")
            return # Exit if file is corrupt, safer to not overwrite

    # Merge new roles
    print(f"Existing roles: {len(existing_roles)}")
    
    for role, data in new_roles.items():
        if "description" not in data:
            data["description"] = DEFAULT_DESCRIPTION
        
        # We overwrite or add
        existing_roles[role] = data
        
    print(f"Total roles after update: {len(existing_roles)}")

    # Write back
    try:
        with open(file_path, 'w') as f:
            json.dump(existing_roles, f, indent=4)
        print("Successfully updated job_roles.json")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    update_roles()

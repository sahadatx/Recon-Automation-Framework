
<div align="center">

# 🔍 Recon Automation Framework

### A Professional Modular Reconnaissance Framework for Security Assessments & Bug Bounty Hunting

Automate reconnaissance workflows including subdomain enumeration, HTTP probing, technology fingerprinting, vulnerability scanning, and security reporting.

<p>

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)

![Platform](https://img.shields.io/badge/Platform-Kali_Linux-red?style=for-the-badge&logo=kalilinux)

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

![Security](https://img.shields.io/badge/Cybersecurity-Recon_Framework-orange?style=for-the-badge)

</p>

A modular reconnaissance framework designed to automate the information gathering phase of security assessments. The framework integrates multiple open-source tools into a single workflow for asset discovery, infrastructure analysis, web reconnaissance, and vulnerability identification.

</div>

---

# 📖 Overview

**Recon Automation Framework** is a modular cybersecurity project built with **Python** to automate reconnaissance tasks performed during penetration testing, vulnerability assessments, and bug bounty engagements.

The framework combines multiple open-source reconnaissance tools into a unified workflow that performs subdomain enumeration, DNS resolution, HTTP probing, technology fingerprinting, port scanning, content discovery, screenshot capture, and Nuclei-based vulnerability scanning.

Designed with a modular architecture, each reconnaissance stage operates independently while integrating seamlessly into the overall workflow, making the framework scalable, maintainable, and easy to extend.

---

# ✨ Features

| Feature | Status |
|---------|:------:|
| Passive Subdomain Enumeration | ✅ |
| DNS Resolution | ✅ |
| HTTP/HTTPS Probe | ✅ |
| Port Scanning | ✅ |
| Technology Detection | ✅ |
| Screenshot Capture | ✅ |
| URL Discovery | ✅ |
| JavaScript Analysis | ✅ |
| Directory Fuzzing | ✅ |
| Nuclei Vulnerability Scanning | ✅ |
| Result Filtering | ✅ |
| Statistics Generation | ✅ |
| TXT Report Export | ✅ |
| JSON Report Export | ✅ |
| CSV Report Export | ✅ |
| Markdown Report Export | ✅ |
| Modular Architecture | ✅ |
| Multi-threaded Execution | ✅ |
| Error Handling | ✅ |
| Logging System | ✅ |

---

# 📑 Table of Contents

- Overview
- Features
- Screenshots
- Architecture
- Project Structure
- Installation
- Quick Start
- Usage
- Recon Workflow
- Modules
- Generated Reports
- Testing
- Technologies Used
- Skills Demonstrated
- Roadmap
- Contributing
- License
- Author

---

# 📸 Screenshots

The following screenshots demonstrate the framework's architecture, reconnaissance workflow, and generated results.

| Screenshot | Description |
|------------|-------------|
| Project Structure | Overall framework directory layout |
| Passive Enumeration | Subdomain discovery results |
| DNS Resolution | Resolved hosts and IP addresses |
| HTTP Probe | Live host detection |
| Port Scanner | Open port discovery |
| Technology Detection | Web technology fingerprinting |
| URL Discovery | Crawled URLs |
| JavaScript Analysis | JavaScript file extraction |
| Directory Fuzzing | Hidden content discovery |
| Screenshot Capture | Website preview generation |
| Nuclei Scan | Vulnerability detection |
| Generated Reports | TXT, JSON, CSV and Markdown reports |

---

# 🏗️ Architecture

```text
                    Target Domain
                         │
                         ▼
              Passive Enumeration
                         │
                         ▼
                 DNS Resolution
                         │
                         ▼
                  HTTP/HTTPS Probe
                         │
                         ▼
                   Port Scanning
                         │
                         ▼
              Technology Detection
                         │
                         ▼
                 URL Discovery
                         │
                         ▼
             JavaScript Analysis
                         │
                         ▼
              Directory Fuzzing
                         │
                         ▼
              Screenshot Capture
                         │
                         ▼
          Nuclei Vulnerability Scan
                         │
                         ▼
          Statistics & Report Generator
                         │
                         ▼
          TXT • JSON • CSV • Markdown
```

---

# ⚙️ Recon Workflow

```text
Target
   │
   ▼
Passive Enumeration
   │
   ▼
DNS Resolution
   │
   ▼
HTTP Probe
   │
   ▼
Port Scan
   │
   ▼
Technology Detection
   │
   ▼
URL Discovery
   │
   ▼
JavaScript Analysis
   │
   ▼
Directory Fuzzing
   │
   ▼
Screenshot Capture
   │
   ▼
Nuclei Scan
   │
   ▼
Export Reports
```

---

# 📁 Project Structure

```text
Recon-Automation-Framework/
│
├── config/
│   └── config.py
│
├── core/
│   ├── banner.py
│   ├── logger.py
│   └── utils.py
│
├── modules/
│   ├── passive/
│   ├── dns/
│   ├── http/
│   ├── ports/
│   ├── technology/
│   ├── crawler/
│   ├── javascript/
│   ├── fuzzing/
│   ├── screenshot/
│   └── nuclei/
│
├── output/
│   ├── passive/
│   ├── dns/
│   ├── http/
│   ├── ports/
│   ├── technology/
│   ├── crawler/
│   ├── javascript/
│   ├── fuzzing/
│   ├── screenshot/
│   └── nuclei/
│
├── wordlists/
│
├── tests/
│
├── screenshots/
│
├── docs/
│
├── recon.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

# 🧩 Framework Modules

| Module | Purpose |
|---------|---------|
| Passive Enumeration | Discover subdomains using multiple passive sources |
| DNS Resolution | Resolve discovered subdomains to IP addresses |
| HTTP Probe | Identify live HTTP/HTTPS services |
| Port Scanner | Discover open TCP ports |
| Technology Detection | Identify web technologies and frameworks |
| URL Discovery | Extract URLs from target applications |
| JavaScript Analysis | Analyze JavaScript assets and endpoints |
| Directory Fuzzing | Discover hidden files and directories |
| Screenshot Capture | Capture website screenshots |
| Nuclei Scanner | Detect known vulnerabilities using Nuclei templates |
| Report Generator | Export reconnaissance results in multiple formats |


# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/sahadatx/Recon-Automation-Framework.git

cd Recon-Automation-Framework
```

---

## Create a Virtual Environment

### Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## Install Required Reconnaissance Tools

Ensure the following tools are installed and accessible from your system PATH.

| Tool | Purpose |
|------|---------|
| Subfinder | Passive Subdomain Enumeration |
| Assetfinder | Asset Discovery |
| Amass | Subdomain Enumeration |
| httpx | HTTP Probe |
| Naabu | Port Scanning |
| Nuclei | Vulnerability Scanning |
| Katana | URL Crawling |
| FFUF | Directory Fuzzing |
| Gowitness | Screenshot Capture |

Verify the installation:

```bash
subfinder -version

assetfinder --help

amass -version

httpx -version

naabu -version

nuclei -version

katana -version

ffuf -V

gowitness version
```

---

# ⚡ Quick Start

Run a complete reconnaissance scan against a target.

```bash
python recon.py -d example.com
```

---

Scan multiple targets.

```bash
python recon.py -f targets.txt
```

---

Run with verbose logging.

```bash
python recon.py -d example.com --verbose
```

---

# 💻 Usage

## Scan a Single Domain

```bash
python recon.py -d example.com
```

---

## Scan Multiple Targets

```bash
python recon.py -f domains.txt
```

---

## Save Results to a Custom Directory

```bash
python recon.py \
-d example.com \
-o output/example
```

---

# 🔍 Reconnaissance Workflow

The framework automatically performs the following reconnaissance stages.

```text
Target Domain
      │
      ▼
Passive Enumeration
      │
      ▼
DNS Resolution
      │
      ▼
HTTP Probe
      │
      ▼
Port Scanning
      │
      ▼
Technology Detection
      │
      ▼
URL Discovery
      │
      ▼
JavaScript Analysis
      │
      ▼
Directory Fuzzing
      │
      ▼
Screenshot Capture
      │
      ▼
Nuclei Vulnerability Scan
      │
      ▼
Generate Reports
```

---

# 📂 Generated Output

After a successful scan, the framework automatically organizes results into dedicated directories.

```text
output/

├── passive/
├── dns/
├── http/
├── ports/
├── technology/
├── crawler/
├── javascript/
├── fuzzing/
├── screenshot/
└── nuclei/
```

Each module stores its own results independently, making the framework easy to analyze, debug, and extend.

---

# 📊 Generated Reports

The framework automatically exports reconnaissance results in multiple formats.

| Report | Status |
|---------|:------:|
| TXT Report | ✅ |
| JSON Report | ✅ |
| CSV Report | ✅ |
| Markdown Report | ✅ |

Reports include:

- Reconnaissance Summary
- Alive Hosts
- Open Ports
- Detected Technologies
- URLs
- JavaScript Files
- Hidden Directories
- Screenshots
- Nuclei Findings
- Scan Statistics

---

# 🧪 Testing

The framework includes automated and manual validation for each reconnaissance module to ensure reliable results and maintain code quality.

## Validate Installed Tools

```bash
subfinder -version

assetfinder --help

amass -version

httpx -version

naabu -version

nuclei -version

katana -version

ffuf -V

gowitness version
```

---

## Run Unit Tests

```bash
python -m pytest -v
```

Example Output

```text
============================= test session starts =============================

collected 32 items

tests/test_passive.py .......... PASSED

tests/test_dns.py .............. PASSED

tests/test_http.py ............. PASSED

tests/test_ports.py ............ PASSED

tests/test_nuclei.py ........... PASSED

==============================

32 passed in 0.84s
```

---

# 🛠️ Technologies Used

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3 |
| Operating System | Kali Linux |
| Subdomain Enumeration | Subfinder, Assetfinder, Amass |
| HTTP Probing | HTTPX |
| Port Scanning | Naabu |
| Vulnerability Scanning | Nuclei |
| URL Crawling | Katana |
| Directory Fuzzing | FFUF |
| Screenshot Capture | Gowitness |
| Version Control | Git |
| Repository Hosting | GitHub |
| Report Formats | TXT, JSON, CSV, Markdown |

---

# 💡 Skills Demonstrated

This project demonstrates practical cybersecurity and software engineering skills, including:

- Passive Reconnaissance
- Asset Discovery
- DNS Enumeration
- HTTP Service Enumeration
- Network Port Scanning
- Web Technology Fingerprinting
- URL Crawling
- JavaScript Analysis
- Directory Enumeration
- Screenshot Automation
- Vulnerability Assessment
- Multi-threaded Programming
- Python Automation
- JSON Data Processing
- CSV Report Generation
- Markdown Report Generation
- Modular Software Architecture
- Error Handling
- Logging
- Git & GitHub Workflow

---

# 📈 Performance

The framework is designed with scalability and modularity in mind.

Current capabilities include:

- Multi-threaded execution
- Modular architecture
- Independent reconnaissance modules
- Structured output directories
- Automatic report generation
- Reusable helper functions
- Robust error handling
- Easy module integration

---

# 🔒 Security Considerations

This project is intended for:

- Authorized Penetration Testing
- Security Assessments
- Bug Bounty Programs
- Capture The Flag (CTF) Labs
- Educational Purposes
- Internal Security Audits

⚠️ **Use this framework only against systems you own or have explicit permission to test. Unauthorized scanning may violate laws, regulations, or terms of service.**

---

# 🗺️ Project Roadmap

## ✅ Phase 1 — Core Recon

- [x] Passive Enumeration
- [x] DNS Resolution
- [x] HTTP Probe
- [x] Port Scanner
- [x] Technology Detection
- [x] Screenshot Capture

---

## ✅ Phase 2 — Discovery

- [x] URL Discovery
- [x] JavaScript Analysis
- [x] Directory Fuzzing
- [ ] Virtual Host Discovery

---

## 🚧 Phase 3 — Infrastructure

- [ ] TLS Analysis
- [ ] WAF Detection
- [ ] CDN Detection
- [ ] Subdomain Takeover Detection
- [ ] Email Security Analysis

---

## 📋 Phase 4 — Reporting

- [ ] Professional HTML Report
- [ ] Interactive Dashboard

---

## 🚀 Phase 5 — Framework

- [ ] CLI Improvements
- [ ] Performance Optimization
- [ ] Plugin System
- [ ] Distributed Recon

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve this project, please follow the steps below.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Please ensure that:

- Code follows **PEP 8** guidelines.
- New features include appropriate documentation.
- Existing functionality is not broken.
- Pull Requests are clearly described.
- Tests are updated whenever necessary.

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software under the terms of the MIT License.

See the **LICENSE** file for more information.

---

# 👨‍💻 Author

## Sahadat Hossain

**Cybersecurity Enthusiast | Penetration Testing | Reconnaissance | Python Automation**

📧 **Email**

pentester.sahadathossain@gmail.com

💼 **LinkedIn**

https://www.linkedin.com/in/pentester-sahadat-hossain/

🐙 **GitHub**

https://github.com/sahadatx

---

# 📬 Contact

If you have any questions, suggestions, or feedback regarding this project, feel free to reach out.

- Open an Issue
- Submit a Pull Request
- Connect via LinkedIn
- Send an Email

---

# 🌟 Support

If you found this project useful, please consider supporting it.

- ⭐ Star this repository
- 🍴 Fork this project
- 🛠️ Contribute improvements
- 📢 Share it with the cybersecurity community

Your support helps improve the project and encourages future development.

---

# 🙏 Acknowledgements

This project makes use of several outstanding open-source security tools and communities.

Special thanks to:

- ProjectDiscovery
- OWASP
- FFUF
- Katana
- Nuclei
- Naabu
- HTTPX
- Subfinder
- Amass
- Assetfinder
- Gowitness
- Python Community

Their tools and contributions have significantly advanced the cybersecurity ecosystem.

---

# 📌 Disclaimer

This framework is intended **solely for educational purposes, authorized security assessments, and bug bounty programs**.

The author is **not responsible** for any misuse, unauthorized access, or damage caused by the use of this software.

Always obtain **proper authorization** before performing reconnaissance or security testing against any system.

---

<div align="center">

## ⭐ If you found this project useful, please consider giving it a Star!

Made with ❤️ by **Sahadat Hossain**

</div>
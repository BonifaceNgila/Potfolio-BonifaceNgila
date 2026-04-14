"""Seed the database with CV data from Bonface Mutisya Ngila's resume."""

from app import app, db, Profile, Experience, Education, Skill, Project, Certification


def seed():
    with app.app_context():
        db.create_all()

        # ── Profile ──────────────────────────────────────────────────────
        if not Profile.query.first():
            db.session.add(Profile(
                full_name="Bonface Mutisya Ngila",
                tagline="ICT Support Specialist | Web Developer",
                bio=(
                    "Highly versatile IT professional and web developer pursuing an M.Sc. in "
                    "Computer Science. Experienced at the intersection of system administration "
                    "and software engineering, with a proven track record managing secure, "
                    "high-availability infrastructure and Identity & Access Management (IAM) for "
                    "global organizations such as Plan International. Skilled in full-stack "
                    "development (PHP, Python, JavaScript) and experienced integrating AI/LLMs "
                    "into practical tools, including automated code reviewers and data management "
                    "systems. OCI DevOps Professional and Architect Associate certified, with a "
                    "security-first approach to infrastructure monitoring and application development. "
                    "Committed to driving organizational success through automation, strong "
                    "cybersecurity practices, and user-centered technology solutions."
                ),
                email="mutisyaboniface@outlook.com",
                phone="+254792950816",
                address="Kilifi, Kenya",
                linkedin="https://www.linkedin.com/in/bonifacengila254/",
                github="https://github.com/BonifaceNgila",
            ))

        # ── Experience ───────────────────────────────────────────────────
        if not Experience.query.first():
            db.session.add(Experience(
                job_title="IT Officer",
                company="Plan International Kenya, Coastal Hub",
                location="Kenya",
                start_date="March 2024",
                end_date="December 2025",
                description=(
                    "Managed IT infrastructure, servers, and networks to ensure high availability, security, and performance through continuous monitoring and disaster recovery planning.\n"
                    "Configured user access, virtualized environments, and server applications, ensuring strict compliance with organizational security standards and IAM governance.\n"
                    "Provided first- to mid-level helpdesk support, troubleshot complex access issues, and conducted staff training to promote IT best practices and secure authentication.\n"
                    "Maintained accurate documentation and prepared regular IT performance reports.\n"
                    "Facilitated effective service delivery by managing service tickets on ServiceNow, ensuring timely documentation of incidents, resolutions, and procedures.\n"
                    "Participated in onboarding and offboarding processes, coordinating account updates and equipment provisioning according to established SOPs.\n"
                    "Monitored service queues and performed follow-ups on aging tickets to provide users with professional updates on their issues.\n"
                    "Collaborated with senior specialists and infrastructure teams to escalate complex issues, ensuring clear technical context for efficient resolution.\n"
                    "Contributed to service improvements by identifying recurring problems and exploring opportunities for operational automation."
                ),
                sort_order=1,
            ))
            db.session.add(Experience(
                job_title="IT Assistant",
                company="Plan International Kenya, Coastal Hub",
                location="Kenya",
                start_date="November 2022",
                end_date="February 2024",
                description=(
                    "Executed user identity lifecycle activities by configuring user accounts and permissions to secure system access.\n"
                    "Collaborated with IT management on global directory services and email groups to ensure seamless SSO integrations and quality service delivery.\n"
                    "Optimized IT infrastructure for efficiency and supported system upgrades, backups, and secure connectivity.\n"
                    "Delivered Tier 1 support for desktop, network, and infrastructure issues, successfully communicating technical concepts to non-technical users.\n"
                    "Provided support for Microsoft 365 applications, ensuring proper configuration of email accounts and VPN connectivity.\n"
                    "Diagnosed and resolved routine hardware and software problems, maintaining accurate records of all interactions in the ticketing system.\n"
                    "Mentored junior team members, facilitating their technical development and contributing to overall team performance improvements."
                ),
                sort_order=2,
            ))
            db.session.add(Experience(
                job_title="IT Support Intern",
                company="Plan International Kenya, Coastal Hub",
                location="Kenya",
                start_date="November 2021",
                end_date="November 2022",
                description=(
                    "Managed Global Active Directory and OKTA services, troubleshooting authentication errors and supporting access modifications.\n"
                    "Supported technical operations for systems including Exchange Online, SAP, and Office 365, ensuring secure user access and minimal downtime.\n"
                    "Enforced IT policies, developed security guidelines, and provided user training on corporate applications.\n"
                    "Assisted in managing user accounts within Active Directory and Azure AD, ensuring proper access provisioning and permissions management.\n"
                    "Supported endpoint management and troubleshooting of mobile devices and workstations, including installations and configurations.\n"
                    "Collaborated with IT teams to analyze incidents."
                ),
                sort_order=3,
            ))

        # ── Education ────────────────────────────────────────────────────
        if not Education.query.first():
            db.session.add(Education(
                degree="Master of Science in Computer Science",
                institution="UNICAF University",
                year="Ongoing",
                sort_order=1,
            ))
            db.session.add(Education(
                degree="Bachelor of Business Information Technology",
                institution="Taita Taveta University",
                year="November 2019",
                sort_order=2,
            ))

        # ── Skills ───────────────────────────────────────────────────────
        if not Skill.query.first():
            skills_data = [
                ("Front-end", "JavaScript, React.js, HTML5, CSS3 (Bootstrap), Responsive Design", 1),
                ("Web CMS & Back-end", "WordPress, PHP, MySQL", 2),
                ("Back-end Frameworks & Tools", "Python, FastAPI, Streamlit", 3),
                ("Data Visualization", "Chart.js", 4),
                ("Identity & Access Management", "OKTA, Entra ID (Azure AD), OCI IAM, SSO, MFA, Conditional Access", 5),
                ("Cloud & DevOps", "OCI (DevOps Professional, Architect Associate), Azure AD, AWS", 6),
                ("IT Operations & Processes", "ITIL-aligned Incident Management (ServiceNow)", 7),
                ("Networking & Troubleshooting", "TCP/IP, DNS, DHCP, VPN, Hardware/Software Diagnostics", 8),
                ("Data Protection & Compliance", "Data Protection Regulations (CIPIT certified), Privacy and Compliance Controls", 9),
                ("Mobile & Endpoint Management", "iOS and Android Device Optimization and Management", 10),
            ]
            for category, items, order in skills_data:
                db.session.add(Skill(category=category, items=items, sort_order=order))

        # ── Projects ─────────────────────────────────────────────────────
        if not Project.query.first():
            db.session.add(Project(
                title="Asset Management System",
                description="A PHP/MySQL web application for tracking organizational assets and related workflows. Supports multi-role users, scoped access for custodians and verifiers, and full asset lifecycle management, including verification windows, disposals, and reporting.",
                technologies="PHP, MySQL, JavaScript, HTML5, Font Awesome",
                url="https://github.com/BonifaceNgila/Asset_list",
                sort_order=1,
            ))
            db.session.add(Project(
                title="HealthDMS - Health Data Management System",
                description="A full-stack PHP/MySQL web application for managing Sickle Cell Disease (SCD) screening programs. Tracks patients, health facilities, test kits, and screening results across counties, with built-in analytics, reporting, and role-based access control.",
                technologies="PHP 7.4+, MySQL 5.7+, Chart.js 4, XAMPP (Apache + MySQL)",
                url="https://github.com/BonifaceNgila/healthdms",
                sort_order=2,
            ))
            db.session.add(Project(
                title="Code Review Assistant (DeepSeek-Coder)",
                description="Uses the DeepSeek-Coder model via Ollama to analyze code and provide feedback, improvement suggestions, and bug fixes.",
                technologies="DeepSeek-Coder LLM, FastAPI, Streamlit, Ollama",
                url="https://github.com/BonifaceNgila/code-review-deepseek",
                sort_order=3,
            ))
            db.session.add(Project(
                title="Image Caption Generator (LLaVA)",
                description="Uses the LLaVA vision-language model via Ollama to generate descriptive captions for uploaded images.",
                technologies="LLaVA, FastAPI, Streamlit",
                url="https://github.com/BonifaceNgila/Image-Caption-Generator-with-LLaVA",
                sort_order=4,
            ))
            db.session.add(Project(
                title="Sentiment Analyzer (Mistral)",
                description="A simple AI application that uses the Mistral model via Ollama to classify text sentiment as Positive, Negative, or Neutral.",
                technologies="FastAPI, Streamlit, Mistral via Ollama",
                sort_order=5,
            ))

        # ── Certifications ───────────────────────────────────────────────
        if not Certification.query.first():
            certs = [
                ("Oracle Cloud Infrastructure 2025 Certified DevOps Professional", "Oracle", "October 2025", 1),
                ("Oracle Cloud Infrastructure 2025 Certified Architect Associate", "Oracle", "October 2025", 2),
                ("Oracle Cloud Infrastructure 2025 Certified Foundations Associate", "Oracle", "August 2025", 3),
                ("Google IT Support Professional Certification", "Google / Coursera", "July 2022", 4),
                ("IBM Data Analyst Professional Certification", "IBM / Coursera", "October 2022", 5),
                ("CIPIT's Data Protection Course", "Strathmore University", "March 2024", 6),
            ]
            for title, issuer, date, order in certs:
                db.session.add(Certification(title=title, issuer=issuer, date_obtained=date, sort_order=order))

        db.session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed()

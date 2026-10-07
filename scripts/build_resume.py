from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(__file__).resolve().parent / "fonts"
OUTPUT = ROOT / "public" / "felipe-sales-resume.pdf"

pdfmetrics.registerFont(TTFont("Montserrat", FONT_DIR / "Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-SemiBold", FONT_DIR / "Montserrat-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Bold", FONT_DIR / "Montserrat-Bold.ttf"))

BLACK = colors.HexColor("#080808")
GRAY = colors.HexColor("#B7B7B7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ResumeName", fontName="Montserrat-Bold", fontSize=25, leading=30, textColor=BLACK, spaceAfter=3))
styles.add(ParagraphStyle(name="ResumeRole", fontName="Montserrat", fontSize=13.5, leading=18, textColor=BLACK, spaceAfter=12))
styles.add(ParagraphStyle(name="ResumeContact", fontName="Montserrat", fontSize=10.3, leading=14.5, textColor=BLACK, spaceAfter=13))
styles.add(ParagraphStyle(name="ResumeSection", fontName="Montserrat-SemiBold", fontSize=13.5, leading=17, textColor=BLACK, spaceBefore=10, spaceAfter=10))
styles.add(ParagraphStyle(name="ResumeBody", fontName="Montserrat", fontSize=9.8, leading=13.7, textColor=BLACK, spaceAfter=6))
styles.add(ParagraphStyle(name="ResumeJob", fontName="Montserrat-SemiBold", fontSize=10.8, leading=14, textColor=BLACK, spaceBefore=4, spaceAfter=4))
styles.add(ParagraphStyle(name="ResumeMeta", fontName="Montserrat", fontSize=9.6, leading=13, textColor=BLACK, spaceAfter=7))
styles.add(ParagraphStyle(name="ResumeBullet", fontName="Montserrat", fontSize=9.5, leading=13.2, textColor=BLACK, leftIndent=9, firstLineIndent=-9, spaceAfter=2.4))
styles.add(ParagraphStyle(name="ResumeProject", fontName="Montserrat-SemiBold", fontSize=10.2, leading=13.5, textColor=BLACK, spaceBefore=7, spaceAfter=2))
styles.add(ParagraphStyle(name="ResumeCompact", fontName="Montserrat", fontSize=9.4, leading=12.8, textColor=BLACK, spaceAfter=3))


def text(value, style="ResumeBody"):
    return Paragraph(value, styles[style])


def rule(width=0.7, space_before=6, space_after=3):
    return HRFlowable(width="100%", thickness=width, color=GRAY, spaceBefore=space_before, spaceAfter=space_after)


def section(title):
    return Paragraph(title.upper(), styles["ResumeSection"])


def bullet(value):
    return Paragraph(f"- {value}", styles["ResumeBullet"])


def job(title, company, period, location, summary, items):
    blocks = [
        text(title, "ResumeJob"),
        text(f"{company} | {period} | {location}", "ResumeMeta"),
        text(summary),
    ]
    blocks.extend(bullet(item) for item in items)
    blocks.append(Spacer(1, 4))
    return blocks


def project(title, status, stack, description):
    return [
        text(f"> {title} [{status}]", "ResumeProject"),
        text(f"Tech Stack: {stack}", "ResumeCompact"),
        text(description, "ResumeBody"),
    ]


def build():
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=18 * mm,
        bottomMargin=17 * mm,
        title="Felipe Sales de Oliveira - Cloud, DevOps & SRE Consultant",
        author="Felipe Sales de Oliveira",
        subject="Professional resume",
    )

    story = [
        text("Felipe Sales de Oliveira", "ResumeName"),
        text("Cloud, DevOps & SRE Consultant | AWS, Kubernetes, Terraform and Observability", "ResumeRole"),
        HRFlowable(width=68, thickness=1.5, color=BLACK, spaceBefore=0, spaceAfter=10, hAlign="LEFT"),
        text(
            "Florianopolis - SC | +55 48 99629-7388 | fesales.oliveira@gmail.com<br/>"
            "linkedin.com/in/felipesalesdeoliveira | github.com/felipesalesdeoliveira",
            "ResumeContact",
        ),
        rule(),
        section("Professional Summary"),
        text(
            "Cloud, DevOps and Site Reliability Engineering consultant with more than three years of hands-on experience building, operating and improving production environments. Experience with AWS architecture, Terraform, Kubernetes, CI/CD, GitOps and observability, including infrastructure provisioning, containerized application delivery, incident investigation and collaboration with development teams. Engineering background that supports a structured approach to planning, risk, cost and problem-solving."
        ),
        rule(space_before=7),
        section("Technical Skills"),
        bullet("Cloud & Infrastructure as Code: AWS, Terraform, Infrastructure as Code, Linux and networking"),
        bullet("Containers & Orchestration: Docker, Kubernetes, Amazon EKS and Helm"),
        bullet("CI/CD & GitOps: GitHub Actions, Jenkins, Argo CD, Git and delivery pipelines"),
        bullet("Observability: Prometheus, Grafana, Loki, Elastic Stack, Kibana and OpenTelemetry"),
        bullet("SRE & Operations: troubleshooting, synthetic monitoring, incident investigation, availability and reliability"),
        rule(space_before=8),
        section("Professional Experience"),
    ]

    story.extend(job(
        "Cloud, DevOps & SRE Consultant",
        "FSO Cloud Consulting",
        "Jan 2025 - Present",
        "Florianopolis, SC, Brazil | Remote",
        "Independent consulting focused on AWS architecture, infrastructure automation, CI/CD, observability and cloud-native operations.",
        [
            "Design and evolve AWS architectures considering availability, scalability, security, networking and cost.",
            "Automate infrastructure provisioning with Terraform and Infrastructure as Code practices.",
            "Build and operate containerized environments with Kubernetes, Amazon EKS, Docker and Helm.",
            "Implement CI/CD, GitOps, synthetic monitoring, dashboards and actionable alerts.",
            "Investigate failures using metrics, logs, APIs and availability data to support incident resolution.",
        ],
    ))

    story.append(PageBreak())
    story.extend(job(
        "DevOps Engineer",
        "FCamara",
        "Jan 2023 - Dec 2024",
        "Florianopolis, SC, Brazil | Remote",
        "Worked on the automation, operation and evolution of cloud infrastructure and Kubernetes environments supporting production applications.",
        [
            "Automated AWS infrastructure provisioning with Terraform, including VPC, IAM, EC2, RDS, S3 and Amazon EKS.",
            "Designed and standardized CI/CD pipelines with GitHub Actions, improving build and deployment consistency.",
            "Deployed and maintained containerized applications on Kubernetes using Helm for release management.",
            "Implemented and enhanced observability with Prometheus, Grafana, Loki and the Elastic Stack.",
            "Supported production environments through troubleshooting, incident investigation and failure analysis.",
        ],
    ))
    story.extend(job(
        "Civil Engineer",
        "Cymaco Engenharia",
        "Feb 2020 - Jan 2023",
        "Florianopolis, SC, Brazil",
        "Planned and monitored construction projects with responsibility for budgets, financial analysis, schedules, resources and decision support.",
        ["Developed systems thinking, organization, risk analysis and structured problem-solving."],
    ))
    story.extend([rule(space_before=8), section("Technical Projects")])
    story.extend(project(
        "Secure Frontend Delivery on AWS",
        "Completed",
        "React, Amazon S3, CloudFront, ACM, Route 53 and OAC",
        "Delivered a React SPA from a private S3 origin through CloudFront. Validated HTTPS redirection, SPA routing, private-origin access controls and cache behavior.",
    ))
    story.extend(project(
        "Serverless Marketplace with Identity and Events",
        "In Progress",
        "Cognito, API Gateway, Lambda, DynamoDB, Amazon S3 and SQS",
        "Evolving the published SPA into an architecture with authentication, protected APIs, persistence and asynchronous order processing with a dead-letter queue.",
    ))
    story.extend(project(
        "End-to-End DevOps Platform on AWS",
        "Lab",
        "AWS, Terraform, Jenkins, Kubernetes, Argo CD, Prometheus and Grafana",
        "Provisioned AWS infrastructure and connected CI/CD, Kubernetes deployment, GitOps and observability in one delivery workflow.",
    ))
    story.extend(project(
        "Multi-Cluster Kubernetes Observability",
        "Lab",
        "AWS, EKS, Terraform, Prometheus, Grafana, Loki and Fluent Bit",
        "Separated application and observability clusters while centralizing metrics and logs and automating infrastructure and networking.",
    ))

    story.append(PageBreak())
    story.extend([rule(space_before=0, space_after=4), section("Additional Technical Projects")])
    story.extend(project(
        "Kubernetes 360-degree Observability",
        "Lab",
        "Kubernetes, Prometheus, Grafana, Loki, OpenTelemetry and Tempo",
        "Correlated metrics, logs and distributed traces and applied SLIs, SLOs and error-budget concepts.",
    ))
    story.extend(project(
        "FinOps & AWS Cost Optimization",
        "Lab",
        "AWS Cost Explorer, AWS Budgets, Compute Optimizer and Lambda",
        "Implemented cost monitoring, budget alerts, rightsizing analysis and automation for idle resources.",
    ))
    story.extend([
        rule(space_before=8),
        section("Education"),
        text("<b>Bachelor's Degree in Computer Science - In Progress</b>"),
        text("Universidade do Sul de Santa Catarina - Unisul | 2026 - 2030"),
        Spacer(1, 4),
        text("<b>Bachelor's Degree in Civil Engineering</b>"),
        text("Universidade do Sul de Santa Catarina - Unisul | 2012 - 2017"),
        Spacer(1, 4),
        text("<b>Technical Degree in Building Construction</b>"),
        text("Instituto Federal de Santa Catarina - IFSC | 2010 - 2011"),
        rule(space_before=9),
        section("Certifications & Courses"),
        bullet("AWS Certified Cloud Practitioner"),
        bullet("Linux Essentials - Linux Professional Institute"),
        bullet("IBM DevOps and Software Engineering Professional Certificate - IBM / Coursera - In Progress"),
        bullet("Terraform - From Basic to Advanced"),
        bullet("SRE DevOps: End-to-End Journey"),
        bullet("Databricks Fundamentals - Databricks Academy"),
        rule(space_before=9),
        section("Languages"),
        bullet("Portuguese: Native"),
        bullet("English: Professional Working Proficiency"),
        bullet("French: Elementary"),
        rule(space_before=9),
        section("Professional Links"),
        text("Technical Portfolio: felipesalesdeoliveira.github.io/felipe-sales-technical-portfolio/", "ResumeCompact"),
        text("FSO Cloud Consulting: felipesalesdeoliveira.github.io/fso-cloud-consulting/", "ResumeCompact"),
    ])

    document.build(story)


if __name__ == "__main__":
    build()

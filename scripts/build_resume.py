from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "felipe-sales-resume.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 16 * mm

DARK = colors.HexColor("#172326")
MUTED = colors.HexColor("#526064")
ACCENT = colors.HexColor("#148a68")
LIGHT = colors.HexColor("#e5efec")
PANEL = colors.HexColor("#f4f8f7")


def register_fonts():
    candidates = [
        ("Inter", "/System/Library/Fonts/Supplemental/Arial.ttf"),
        ("Inter-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ]
    for name, path in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))


register_fonts()
FONT = "Inter" if "Inter" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
FONT_BOLD = "Inter-Bold" if "Inter-Bold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="Name",
    fontName=FONT_BOLD,
    fontSize=24,
    leading=28,
    textColor=DARK,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Role",
    fontName=FONT,
    fontSize=11.5,
    leading=15,
    textColor=ACCENT,
))
styles.add(ParagraphStyle(
    name="Contact",
    fontName=FONT,
    fontSize=8.5,
    leading=12,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="Section",
    fontName=FONT_BOLD,
    fontSize=11.5,
    leading=14,
    textColor=DARK,
    spaceBefore=9,
    spaceAfter=6,
    borderColor=ACCENT,
    borderWidth=0,
    borderPadding=0,
))
styles.add(ParagraphStyle(
    name="BodyResume",
    fontName=FONT,
    fontSize=8.8,
    leading=12.5,
    textColor=DARK,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="JobTitle",
    fontName=FONT_BOLD,
    fontSize=10.2,
    leading=13,
    textColor=DARK,
    spaceAfter=1,
))
styles.add(ParagraphStyle(
    name="JobMeta",
    fontName=FONT,
    fontSize=8.4,
    leading=11,
    textColor=ACCENT,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="BulletResume",
    fontName=FONT,
    fontSize=8.6,
    leading=12,
    textColor=DARK,
    leftIndent=8,
    firstLineIndent=-8,
    spaceAfter=2.5,
))
styles.add(ParagraphStyle(
    name="Small",
    fontName=FONT,
    fontSize=8,
    leading=11,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="ProjectTitle",
    fontName=FONT_BOLD,
    fontSize=9.3,
    leading=12,
    textColor=DARK,
    spaceAfter=2,
))


def p(text, style="BodyResume"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"- {text}", styles["BulletResume"])


def section(title):
    label = Table([[Paragraph(title.upper(), styles["Section"])]], colWidths=[PAGE_WIDTH - 2 * MARGIN_X])
    label.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.7, LIGHT),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return label


def job(title, company, period, location, summary, bullets):
    content = [
        p(title, "JobTitle"),
        p(f"{company} | {period} | {location}", "JobMeta"),
        p(summary),
    ]
    content.extend(bullet(item) for item in bullets)
    content.append(Spacer(1, 4))
    return KeepTogether(content)


def project(title, status, description, stack):
    return KeepTogether([
        p(f"{title} <font color='#148a68'>[{status}]</font>", "ProjectTitle"),
        p(description, "BodyResume"),
        p(f"Stack: {stack}", "Small"),
        Spacer(1, 5),
    ])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.line(MARGIN_X, 11 * mm, PAGE_WIDTH - MARGIN_X, 11 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT, 7.5)
    canvas.drawString(MARGIN_X, 7 * mm, "Felipe Sales de Oliveira - Cloud, DevOps & SRE Consultant")
    canvas.drawRightString(PAGE_WIDTH - MARGIN_X, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Felipe Sales de Oliveira - Cloud, DevOps & SRE Consultant",
        author="Felipe Sales de Oliveira",
        subject="Professional resume",
    )
    frame = Frame(
        MARGIN_X,
        MARGIN_BOTTOM,
        PAGE_WIDTH - 2 * MARGIN_X,
        PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=5 * mm,
    )
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=footer)])

    story = []
    header = Table([
        [
            [p("Felipe Sales de Oliveira", "Name"), p("Cloud, DevOps & SRE Consultant", "Role")],
            p(
                "Florianopolis, SC, Brazil<br/>"
                "+55 48 99629-7388 | fesales.oliveira@gmail.com<br/>"
                "linkedin.com/in/felipesalesdeoliveira<br/>"
                "github.com/felipesalesdeoliveira",
                "Contact",
            ),
        ]
    ], colWidths=[112 * mm, 64 * mm])
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([header, section("Professional profile")])
    story.append(p(
        "Cloud, DevOps and Site Reliability Engineering consultant with more than three years of hands-on experience building, operating and improving production environments. Experience across AWS architecture, Terraform, Kubernetes, CI/CD, GitOps, observability, incident investigation and cloud-native operations. Engineering background that supports a structured approach to planning, risk, cost and problem-solving."
    ))

    story.append(section("Core expertise"))
    expertise = [
        [p("<b>AWS Cloud Architecture</b><br/>VPC, IAM, EC2, RDS, S3, CloudFront, EKS, Lambda", "Small"), p("<b>Infrastructure as Code</b><br/>Terraform, repeatable environments, automation", "Small")],
        [p("<b>Kubernetes & Platforms</b><br/>Kubernetes, EKS, Docker, Helm, Argo CD", "Small"), p("<b>CI/CD & GitOps</b><br/>GitHub Actions, Jenkins, delivery automation", "Small")],
        [p("<b>Observability & SRE</b><br/>Prometheus, Grafana, Loki, Elastic, OpenTelemetry", "Small"), p("<b>Operations</b><br/>Troubleshooting, incidents, synthetic monitoring, Linux", "Small")],
    ]
    expertise_table = Table(expertise, colWidths=[88 * mm, 88 * mm], hAlign="LEFT")
    expertise_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL),
        ("BOX", (0, 0), (-1, -1), 0.4, LIGHT),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(expertise_table)

    story.append(section("Professional experience"))
    story.append(job(
        "Cloud, DevOps & SRE Consultant",
        "FSO Cloud Consulting",
        "Jan 2025 - Present",
        "Florianopolis, SC, Brazil",
        "Independent consulting focused on AWS architecture, infrastructure automation, CI/CD, observability and cloud-native operations.",
        [
            "Design and evolve AWS architectures considering availability, scalability, security, networking and cost.",
            "Automate infrastructure provisioning with Terraform and Infrastructure as Code practices.",
            "Build and operate containerized environments with Kubernetes, Amazon EKS, Docker and Helm.",
            "Implement CI/CD, GitOps, synthetic monitoring, dashboards and actionable alerts.",
            "Investigate failures using metrics, logs, APIs and availability data to support incident resolution.",
        ],
    ))
    story.append(job(
        "DevOps Engineer",
        "FCamara",
        "Jan 2023 - Dec 2024",
        "Florianopolis, SC, Brazil",
        "Worked on automation, operation and evolution of cloud infrastructure and Kubernetes environments supporting production applications.",
        [
            "Provisioned AWS infrastructure with Terraform, including VPC, IAM, EC2, RDS, S3 and Amazon EKS.",
            "Standardized CI/CD pipelines with GitHub Actions and managed Kubernetes releases with Helm.",
            "Implemented and evolved observability with Prometheus, Grafana, Loki and Elastic Stack.",
            "Supported production environments through troubleshooting, incident investigation and failure analysis.",
        ],
    ))
    story.append(job(
        "Civil Engineer",
        "Cymaco Engenharia",
        "Feb 2020 - Jan 2023",
        "Florianopolis, SC, Brazil",
        "Planned and monitored construction projects with responsibility for budgets, financial analysis, schedules, resources and decision support.",
        ["Developed systems thinking, organization, risk analysis and structured problem-solving."],
    ))

    story.append(section("Selected technical projects"))
    story.append(project(
        "Secure Frontend Delivery on AWS",
        "Completed",
        "Delivered a React SPA from a private S3 origin through CloudFront with OAC, ACM and Route 53. Validated HTTPS redirection, SPA routing, private-origin access controls and cache behavior.",
        "React, Amazon S3, CloudFront, ACM, Route 53, OAC",
    ))
    story.append(project(
        "Serverless Marketplace with Identity and Events",
        "In progress",
        "Evolving the published SPA into an architecture with Cognito authentication, protected APIs, DynamoDB persistence, private product images and asynchronous order processing with SQS and a DLQ.",
        "Cognito, API Gateway, Lambda, DynamoDB, S3, SQS",
    ))
    story.append(project(
        "End-to-End DevOps Platform on AWS",
        "Lab",
        "Provisioned AWS infrastructure and connected CI/CD, Kubernetes deployment, GitOps and observability in one delivery workflow.",
        "AWS, Terraform, Jenkins, Kubernetes, Argo CD, Prometheus, Grafana",
    ))
    story.append(project(
        "Kubernetes Observability Projects",
        "Lab",
        "Built multi-cluster and 360-degree observability architectures covering centralized metrics, logs, distributed traces, SLIs, SLOs and error budgets.",
        "EKS, Prometheus, Grafana, Loki, Fluent Bit, OpenTelemetry, Tempo",
    ))
    story.append(project(
        "FinOps and AWS Cost Optimization",
        "Lab",
        "Developed cost monitoring, budget alerts, rightsizing analysis and automation for idle resources.",
        "AWS Cost Explorer, AWS Budgets, Compute Optimizer, Lambda",
    ))

    story.append(section("Education"))
    story.append(p("<b>Bachelor's Degree in Computer Science</b> - Universidade do Sul de Santa Catarina (Unisul) | 2026 - 2030 | In progress"))
    story.append(p("<b>Bachelor's Degree in Civil Engineering</b> - Universidade do Sul de Santa Catarina (Unisul) | 2012 - 2017"))
    story.append(p("<b>Technical Degree in Building Construction</b> - Instituto Federal de Santa Catarina (IFSC) | 2010 - 2011"))

    story.append(section("Certifications and professional development"))
    story.append(p("AWS Certified Cloud Practitioner | Linux Essentials | Databricks Fundamentals | Terraform - From Basic to Advanced | SRE DevOps - End-to-End Journey"))
    story.append(p("IBM DevOps and Software Engineering Professional Certificate - Coursera | 2026 | In progress"))

    story.append(section("Languages"))
    story.append(p("Portuguese - Native | English - Professional working proficiency | French - Elementary"))

    doc.build(story)


if __name__ == "__main__":
    build()

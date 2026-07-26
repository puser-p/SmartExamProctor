import os
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from reportlab.platypus import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


class ReportGenerator:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

    def generate(
            self,
            student_name,
            roll_no,
            duration,
            violations
    ):

        filename = f"Report_{roll_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        filepath = os.path.join("reports", filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=(8.27 * inch, 11.69 * inch),
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=30
        )

        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_style.alignment = TA_CENTER
        title_style.textColor = colors.darkblue

        heading_style = styles["Heading2"]
        heading_style.textColor = colors.darkred

        normal = styles["BodyText"]

        elements = []
        logo_path = os.path.join("assets", "logo.png")

        if os.path.exists(logo_path):

            logo = Image(
                logo_path,
                width=90,
                height=90
            )

            logo.hAlign = "CENTER"

            elements.append(logo)

            elements.append(Spacer(1,10))
        elements.append(
            Paragraph(
                "<b>SMART EXAM PROCTORING SYSTEM</b>",
                title_style
            )
        )

        elements.append(
            Paragraph(
                "Artificial Intelligence Based Examination Monitoring",
                title_style
            )
        )

        elements.append(Spacer(1, 20))

        elements.append(
            Paragraph(
                "<b>EXAM REPORT</b>",
                heading_style
            )
        )


        elements.append(
            Paragraph(
                f"<b>Generated On :</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                normal
            )
        )

        elements.append(Spacer(1, 12))
        elements.append(
            Paragraph(
                "<b>Student Information</b>",
                heading_style
            )
        )

        elements.append(Spacer(1,10))

        student_table = Table(

            [

                ["Student Name", student_name],

                ["Roll Number", roll_no],

                ["Exam Duration", duration],

                ["Exam Date", datetime.now().strftime("%d-%m-%Y")],

                ["Exam Time", datetime.now().strftime("%I:%M:%S %p")]

            ],

            colWidths=[160,300]

        )

        student_table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE")

            ])

        )

        elements.append(student_table)

        elements.append(Spacer(1,12))
        elements.append(
            Paragraph(
                "<b>AI Monitoring Summary</b>",
                heading_style
            )
        )

        elements.append(Spacer(1,10))

        summary_table = Table(

            [

                ["Face Recognition","Successful"],

                ["Student Verification","Verified"],

                ["Phone Detection","Checked"],

                ["Unknown Person Detection","Enabled"],

                ["Multiple Person Detection","Enabled"]

            ],

            colWidths=[220,240]

        )

        summary_table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.lightblue),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        elements.append(summary_table)

        elements.append(Spacer(1,12))
        elements.append(
            Paragraph(
                "<b>Violation Log</b>",
                heading_style
            )
        )

        elements.append(Spacer(1, 10))
        violation_data = [["S.No","Violation"]]

        if len(violations)==0:

            violation_data.append(["-","No Violations"])

        else:

            for i,v in enumerate(violations,1):

                violation_data.append([str(i),v])

        violation_table = Table(

            violation_data,

            colWidths=[60,400]

        )

        violation_table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        elements.append(violation_table)
        elements.append(Spacer(1,12))
        total = len(violations)

        if total <= 2:

            risk = "LOW"

        elif total <= 5:

            risk = "MEDIUM"

        else:

            risk = "HIGH"
        if total > 10:
            status = "FAILED"
        else:
            status = "PASSED"

        risk_table = Table(

            [

                ["Total Violations",str(total)],

                ["Risk Level",risk],

                ["Exam Status", status]

            ],

            colWidths=[180,200]

        )

        risk_table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        elements.append(risk_table)
        elements.append(Spacer(1,12))

        elements.append(
            Paragraph(
                "<b>Violation Statistics</b>",
                heading_style
            )
        )

        stats = {}

        for v in violations:

            stats[v] = stats.get(v,0)+1

        data = [["Violation","Count"]]

        for k,v in stats.items():

            data.append([k,str(v)])

        table = Table(
            data,
            colWidths=[300,100]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black)

            ])

        )

        elements.append(table)
        elements.append(Spacer(1,40))
        signature = Table(

            [

                ["____________________","____________________"],

                ["Examiner Signature","Student Signature"]

            ],

            colWidths=[230,230]

        )

        signature.setStyle(

            TableStyle([

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("TOPPADDING",(0,0),(-1,-1),20)

            ])

        )

        elements.append(signature)
        doc.build(
            elements,
            onFirstPage=add_header_footer,
            onLaterPages=add_header_footer
        )

        return filepath
from reportlab.pdfgen import canvas
def add_header_footer(canvas, doc):

    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 10)

    canvas.setFont(
        "Helvetica",
        9
    )

    canvas.drawString(
        40,
        20,
        "Generated Automatically by Smart Exam Proctoring System"
    )

    canvas.drawRightString(
        550,
        20,
        f"Page {doc.page}"
    )

    canvas.restoreState()
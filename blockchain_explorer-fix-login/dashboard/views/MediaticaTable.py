from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
 
#----------------------------------------------------------------------

def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = "Page %s" % page_num
    canvas.drawRightString(285*mm, 2*mm, text)
 
#----------------------------------------------------------------------
def createMultiPage():
    """
    Create a multi-page document
    """
    doc = SimpleDocTemplate("doc_page_num.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    Story = []
    
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
    full_name = "Marvin Jones"
    address_parts = ["411 State St.", "Reno, NV 80158"]
    
    for page in range(5):
        # Create return address
        ptext = '<font size="12">%s</font>' % full_name
        Story.append(Paragraph(ptext, styles["Normal"]))      
        for part in address_parts:
            ptext = '<font size="12">%s</font>' % part.strip()
            Story.append(Paragraph(ptext, styles["Normal"]))
            
        Story.append(Spacer(1, 12))
        ptext = '<font size="12">Dear %s:</font>' % full_name.split()[0].strip()
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        ptext = """<font size="12">We would like to welcome you to our subscriber base
        for %s Magazine! You will receive %s issues at the excellent introductory
        price of $%s. Please respond by %s to start receiving your subscription
        and get the following free gift: %s.</font>"""
        ptext = ptext % (magName, issueNum, subPrice, limitedDate, freeGift)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        
        
        ptext = '<font size="12">Thank you very much and we look forward to serving you.</font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        ptext = '<font size="12">Sincerely,</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 48))
        ptext = '<font size="12">Ima Sucker</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(PageBreak())
        
    doc.build(Story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    createMultiPage()
# from fpdf import FPDF
# import io

# class MeetingReport(FPDF):
#     def header(self):
#         self.set_font("helvetica", "B", 15)
#         self.cell(0, 10, "Executive Meeting Intelligence Report", border=False, ln=True, align="C")
#         self.ln(5)

#     def chapter_title(self, title):
#         self.set_font("helvetica", "B", 12)
#         self.set_fill_color(200, 220, 255)
#         self.cell(0, 10, title, ln=True, fill=True)
#         self.ln(4)

# def generate_meeting_pdf(data: dict):
#     pdf = MeetingReport()
#     pdf.add_page()
    
#     # Section 1: Summary
#     pdf.chapter_title("Executive Summary")
#     pdf.set_font("helvetica", "", 11)
#     pdf.multi_cell(0, 8, data.get("analysis", {}).get("summary", "No summary provided."))
#     pdf.ln(5)
    
#     # Section 2: Action Items
#     pdf.chapter_title("Action Items")
#     action_items = data.get("analysis", {}).get("action_items", [])
#     for item in action_items:
#         task = item.get('task', 'N/A')
#         owner = item.get('owner', 'N/A')
#         pdf.set_font("helvetica", "B", 10)
#         pdf.cell(0, 8, f"• Task: {task}", ln=True)
#         pdf.set_font("helvetica", "I", 10)
#         pdf.cell(0, 8, f"  Owner: {owner} | Deadline: {item.get('deadline', 'N/A')}", ln=True)
#     pdf.ln(5)

#     # Section 3: Full Transcript
#     pdf.add_page()
#     pdf.chapter_title("Full Meeting Transcript")
#     pdf.set_font("helvetica", "", 9)
#     pdf.multi_cell(0, 6, data.get("transcript", "No transcript available."))
    
#     # Return as bytes
#     return bytes(pdf.output())





from fpdf import FPDF
import io

class MeetingReport(FPDF):
    def header(self):
        # Using a standard font, but we will set up Unicode support below
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Executive Meeting Intelligence Report", border=False, ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, ln=True, fill=True)
        self.ln(4)

def generate_meeting_pdf(data: dict):
    # USE 'UTF-8' friendly core fonts or a specific Unicode font
    # Most modern fpdf2 versions support 'Arial' as a core font with latin-1 
    # but for true UTF-8, we use 'helvetica' or 'times' and replace unsupported chars.
    
    pdf = MeetingReport()
    pdf.add_page()
    
    # 1. CLEAN THE TEXT: This is the safest way to fix 'latin-1' errors 
    # It replaces special characters like the bullet point with a simple '-'
    def clean_text(text):
        if not text: return ""
        return (text.replace("•", "-")
                    .replace("\u2022", "-")
                    .replace("\u201c", '"')
                    .replace("\u201d", '"')
                    .replace("\u2019", "'"))

    # Section 1: Summary
    pdf.chapter_title("Executive Summary")
    pdf.set_font("Arial", "", 11)
    summary_text = clean_text(data.get("analysis", {}).get("summary", "No summary provided."))
    pdf.multi_cell(0, 8, summary_text)
    pdf.ln(5)
    
    # Section 2: Action Items
    pdf.chapter_title("Action Items")
    action_items = data.get("analysis", {}).get("action_items", [])
    for item in action_items:
        task = clean_text(item.get('task', 'N/A'))
        owner = clean_text(item.get('owner', 'N/A'))
        pdf.set_font("Arial", "B", 10)
        # Use a simple hyphen instead of the bullet point character
        pdf.cell(0, 8, f"- Task: {task}", ln=True)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 8, f"  Owner: {owner} | Deadline: {item.get('deadline', 'N/A')}", ln=True)
    pdf.ln(5)

    # Section 3: Full Transcript
    pdf.add_page()
    pdf.chapter_title("Full Meeting Transcript")
    pdf.set_font("Arial", "", 9)
    transcript_text = clean_text(data.get("transcript", "No transcript available."))
    pdf.multi_cell(0, 6, transcript_text)
    
    # Final fix for the output call
    # return bytes(pdf.output())
    # return pdf.output()
    return pdf.output(dest="S").encode("latin-1")

from PIL import Image, ImageFont
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

# Paths to assets
logo_path = '/home/buzzadmin/Downloads/idfc.png'  # First logo path
BUZZWORKS_LOGO_PATH = '/home/buzzadmin/Downloads/buzz.jpg'  # Buzzworks logo path
photo_path = '/home/buzzadmin/Downloads/image.jpg'  # User photo path

class Hdfc_Idcreation:
    def __init__(self, user_data):
        self.user_data = user_data
        self.width, self.height = 2000, 3175  # Card dimensions in pixels (16.88 cm x 26.80 cm at 300 DPI)
        # Font paths
        self.font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        self.font_normal_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        # Fonts used in the card
        self.font_bold = ImageFont.truetype(self.font_bold_path, size=80)
        self.font_normal = ImageFont.truetype(self.font_normal_path, size=46)
        self.font_small_bold = ImageFont.truetype(self.font_bold_path, size=50)

    def generate_id_card(self, pdf):
        # Set up the first page for ID card
        pdf.add_page()
        pdf.set_auto_page_break(auto=False, margin=0)  # Disable auto page break
        pdf.set_fill_color(255, 255, 0)  # Yellow color
        photo_height =  79 # Photo height
        photo_top = 90  # Top position of the photo

        # Add yellow rectangle covering the area behind the photo
        pdf.rect(0, photo_top, self.width, photo_height, 'F')  # Yellow rectangle just behind the photo
        # Adding user photo
        try:
            photo = Image.open(self.user_data['Photo_path'])
            photo = photo.resize((90, 100))
            border_size = 2
            bordered_photo = Image.new('RGB', (photo.width + border_size * 2, photo.height + border_size * 2), color='black')
            bordered_photo.paste(photo, (border_size, border_size))
            bordered_photo.save("/tmp/user_photo.jpg")
            pdf.image("/tmp/user_photo.jpg", (210 - bordered_photo.width * 0.75) / 2, 90, bordered_photo.width * 0.75)
        except Exception as e:
            print(f"Could not load photo: {e}")

        # Adding the title "ACCESS CARD" in red color
        pdf.set_font("Helvetica", 'B', 30)  # Font size 50 for title
        pdf.set_text_color(255, 0, 0)  # Red color for title
        pdf.ln(5)  # Move below the photo
        pdf.cell(pdf.w - 2 * pdf.l_margin, 12, "ACCESS CARD", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        # Adding subtitle "For Service Provider"
        pdf.set_font("Helvetica", 'B', 30)  # Font size 30 for subtitle
        pdf.set_text_color(0, 0, 0)  # Reset to black for the subtitle
        pdf.ln(5)  # Add space below title
        pdf.cell(pdf.w - 2 * pdf.l_margin, 12, 'For Service Provider', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        # Adding the user name
        pdf.set_font("Helvetica", 'B', 30)  # Font size 30 for name
        pdf.ln(130)  # Move below the subtitle
        pdf.cell(pdf.w - 2 * pdf.l_margin, 12, self.user_data['Name'], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        # Adding the employee ID, Designation, DOJ, Location, Vendor, etc.
        pdf.set_font("Helvetica", 'B', 24)  # Font size for other fields
        line_height = 4 # Height between lines
        padding = 9  # Space between text and fields
        
        # Label and value width calculation based on ID card width
        label_width = self.width * 0.30  # 35% of the total card width for labels
        value_width = self.width * 0.52 # 55% of the total card width for values

        # Employee ID at a fixed position (label and value alignment)
        pdf.ln(padding)  # Space below the name
        pdf.cell(value_width, line_height, f"               Emp ID       : {self.user_data['Employee_id']}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")  # Value aligned right

        # Designation at a fixed position (label and value alignment)
        pdf.ln(line_height + padding)  # Space between fields
        pdf.cell(value_width, line_height, f"               Design       : {self.user_data['Designation']}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")  # Value aligned right

        # DOJ (Date of Joining) at a fixed position (label and value alignment)
        pdf.ln(line_height + padding)  # Space between fields
        pdf.cell(value_width, line_height, f"               D.O.J          : {self.user_data['DOJ']}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")  # Value aligned right

        # Location at a fixed position (label and value alignment)
        pdf.ln(line_height + padding)  # Space between fields
        pdf.cell(value_width, line_height, f"               Location    : {self.user_data['Location']}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")  # Value aligned right

       
        # Adding horizontal line before Vendor
        pdf.set_line_width(0.2)
        pdf.line(12, pdf.get_y() + 10, pdf.w - 30, pdf.get_y() + 10)  # Draw line across the width

        # Adding subtitle "For Service Provider"
        pdf.set_font("Helvetica", 'B', 25)  # Font size 30 for subtitle
        pdf.set_text_color(0, 0, 0)  # Reset to black for the subtitle
        pdf.ln(20)  # Add space below title
        pdf.cell(pdf.w - 2 * pdf.l_margin, 12, 'Vendor:', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        
        # Adding first logo (IDFC logo)
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((120, 40))
            border_size = 0
            bordered_logo = Image.new('RGB', (logo.width + border_size * 3, logo.height + border_size * 3), color='black')
            bordered_logo.paste(logo, (border_size, border_size))
            bordered_logo.save("/tmp/user_logo.jpg")
            pdf.image("/tmp/user_logo.jpg", (210 - bordered_logo.width * 0.75) / 2, 50, bordered_logo.width * 0.75)
        except Exception as e:
            print(f"Could not load logo: {e}")
    

    
    def generate_second_page(self, pdf):
        # Set up the second page for company details
        pdf.add_page()

        # Add the "Conditions of Use" heading centered
        pdf.set_font("Helvetica", 'B', 24)
        pdf.cell(0, 34, "Conditions of Use:", new_x=XPos.CENTER, new_y=YPos.NEXT, align="C")
        pdf.ln(1)  # Line break

        # Conditions Text, center aligned
        pdf.set_font("Helvetica", size=21)
        conditions = [
            "This card remains the property of",
            "Buzzworks Business Services Pvt Ltd.",
            "and is non-transferable. The bearer of ",
            "this ID card is not authorized to collect ",
            " cash. This card must be surrendered ",
            "when employment with Buzzworks ",
            "Business Services Pvt Ltd. ceases.",
            "Loss must be reported to the issuing ",
            "authority."
        ]
        for line in conditions:
            pdf.cell(0, 10, line, new_x=XPos.CENTER, new_y=YPos.NEXT, align="C")
            pdf.ln(3)  # Line break between conditions

        # Empty line for spacing
        pdf.ln(10)

        # Add the "If found kindly return to" prompt, centered
        pdf.set_font("Helvetica", size=20)
        pdf.cell(0, 15, "If found kindly return to:", new_x=XPos.CENTER, new_y=YPos.NEXT, align="C")
        pdf.ln(6)  # Line break

        # Address Information, center aligned with reduced line spacing
        pdf.set_font("Helvetica", 'B', 20)  # Bold font for the first line
        pdf.cell(0, 10, "Buzzworks Business Services Pvt Ltd.", new_x=XPos.CENTER, new_y=YPos.NEXT, align="C")
        pdf.ln(3)  # Reduced line spacing for the next line

        pdf.set_font("Helvetica", size=20)
        address_lines = [
            "Door No.84, 3rd Floor,Murugesa Naicker Building,Thousand Lights",
            "Greams Road, Chennai - 600 006, Tamil Nadu."
        ]
        for line in address_lines:
            pdf.cell(0, 10, line, new_x=XPos.CENTER, new_y=YPos.NEXT, align="C")
            pdf.ln(3)  # Reduced line spacing for the next address lines

     


    def generate_pdf(self):
        # Create PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=False, margin=15)

        # Generate the first page and second page (only two pages now)
        self.generate_id_card(pdf)
        self.generate_second_page(pdf)

        # Save the PDF at the end
        pdf_output_path = f"{self.user_data['Name']}_id_card.pdf"
        pdf.output(pdf_output_path)
        print(f"ID card PDF generated and saved at: {pdf_output_path}")



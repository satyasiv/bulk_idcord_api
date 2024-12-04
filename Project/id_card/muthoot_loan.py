from PIL import Image, ImageFont
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

# Paths to assets
logo_path = '/home/buzzadmin/Downloads/muthot.jpg'  
BUZZWORKS_LOGO_PATH = '/home/buzzadmin/Downloads/buzz.jpg'  
photo_path = '/home/buzzadmin/Downloads/image.jpg' 

class Muthoot_Idcreation:
    def __init__(self, user_data):
        print(user_data,"userdata111111")
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
        # Set up page for ID card
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)        
        try:
            photo = Image.open(self.user_data['Photo_path'])
            photo = photo.resize((90, 100))
            border_size = 1
            bordered_photo = Image.new('RGB', (photo.width + border_size * 2, photo.height + border_size * 2), color='black')
            bordered_photo.paste(photo, (border_size, border_size))
            bordered_photo.save("/tmp/user_photo.jpg")
            pdf.image("/tmp/user_photo.jpg", (210 - bordered_photo.width * 0.75) / 2, 66, bordered_photo.width * 0.75)
        except Exception as e:
            print(f"Could not load photo: {e}")

        # Adding the name
        pdf.set_font("Helvetica", 'B', 30)  # Font size 20 for name
        pdf.ln(135)  # Move below the photo
        pdf.cell(pdf.w - 2 * pdf.l_margin, 19, self.user_data['Name'], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        # Adding the designation (centered)
        pdf.set_font("Helvetica", 'B', 24)  # Font size 20 for designation
        pdf.cell(pdf.w - 2 * pdf.l_margin, 14, self.user_data['Designation'], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        # Adding the employee ID (centered)
        pdf.set_font("Helvetica", 'B', 30)  # Font size increased to 24
        pdf.cell(pdf.w - 2 * pdf.l_margin, 14, f"Employee Code : {self.user_data['Employee_id']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        # Adding the location (centered)
        pdf.set_font("Helvetica", 'B', 30)  # Font size increased to 24
        pdf.cell(pdf.w - 2 * pdf.l_margin, 14, self.user_data['Location'], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

       # Adding the location (centered)
        pdf.set_font("Helvetica", 'B', 20)  # Font size increased to 24
        pdf.cell(pdf.w - 13 * pdf.l_margin, 70, "Auth. signature", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Full width for centering

        
        try:
            photo = Image.open('/home/buzzadmin/Downloads/signature.jpg')
            photo = photo.resize((70, 50))
            border_size = 0
            bordered_photo = Image.new('RGB', (photo.width + border_size * 2, photo.height + border_size * 2), color='black')
            bordered_photo.paste(photo, (border_size, border_size))
            bordered_photo.save("/tmp/user_sign.jpg")
            pdf.image("/tmp/user_sign.jpg", (100 - bordered_photo.width * 0.75) / 2, 200, bordered_photo.width * 0.75)
        except Exception as e:
            print(f"Could not load photo: {e}")



        # Adding the first logo (Muthoot logo)
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((200, 60))
            border_size = 0
            bordered_logo = Image.new('RGB', (logo.width + border_size * 3, logo.height + border_size * 3), color='black')
            bordered_logo.paste(logo, (border_size, border_size))
            bordered_logo.save("/tmp/user_logo.jpg")
            pdf.image("/tmp/user_logo.jpg", (210 - bordered_logo.width * 0.75) / 2, 10, bordered_logo.width * 0.75)
        except Exception as e:
            print(f"Could not load logo: {e}")
        
    
        # Draw a red line
        pdf.set_draw_color(255, 0, 0)  # Red color
        pdf.set_line_width(30)  # Line width
        pdf.line(5, pdf.h - 15, pdf.w - 10, pdf.h - 15)  # Draw the red line near the bottom

        # Set the font for the text (increase the font size)
        pdf.set_font("Helvetica", 'B', 24)  # Example: Set font size to 24 (you can change this size as needed)

        # Set the color to white for the text "Muthoot Family - 800 Years of Business Legacy"
        pdf.set_text_color(255, 255, 255)  # White color for the text

        # Position for the text and adding the text
        pdf.text(10, pdf.h - 12, 'Muthoot Family - 800 Years of Business Legacy')

        # Restore the text color to black (or any other color you need) for subsequent text
        pdf.set_text_color(0, 0, 0)  
                

    def generate_second_page(self, pdf):
        # Set up the second page for additional details
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 20)
        
        # Adding the associate info section
        pdf.ln(30)  # Ensure some space from top
        pdf.cell(200, 10, "Associate on the role of:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        pdf.ln(110)  # Line break after this section
    
        # Adding the address info
        pdf.set_font("Helvetica", 'B', 23)
        pdf.cell(200, 13, "Buzzworks Business Services Pvt. Ltd.", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(0)  # Space after company name

        pdf.set_font("Helvetica", size=15)
        address_lines = [
            "Door No.84, 3rd Floor, Murugesa Naicker Building,",
            "Thousand Lights, Greams Road, Chennai - 600 006.",
            "Ph : +91.44.4978 1504",
            "www.buzzworks.com"
        ]

      # Add address information line by line
        for line in address_lines:
            pdf.cell(200, 10, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            pdf.ln(6)  # Small line break between address lines
        # Adding the second logo (Buzzworks logo)
        try:
            buzzworks_logo = Image.open(BUZZWORKS_LOGO_PATH)
            buzzworks_logo = buzzworks_logo.resize((200, 60))
            border_size = 0
            bordered_buzzworks_logo = Image.new('RGB', (buzzworks_logo.width + border_size * 3, buzzworks_logo.height + border_size * 3), color='black')
            bordered_buzzworks_logo.paste(buzzworks_logo, (border_size, border_size))
            bordered_buzzworks_logo.save("/tmp/buzzworks_logo.jpg")
            # Placing the logo with a bit more space (increased from 100 to 130)
            pdf.image("/tmp/buzzworks_logo.jpg", (210 - bordered_buzzworks_logo.width * 0.75) / 2, 80, bordered_buzzworks_logo.width * 0.75)
        except Exception as e:
            print(f"Could not load Buzzworks logo: {e}")






    def generate_pdf(self):
        # Create PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        # Generate the first and second pages
        self.generate_id_card(pdf)
        self.generate_second_page(pdf)
        print(self.user_data['Name'],"user_name")
        # Save the PDF at the end
        pdf_output_path = f"{self.user_data['Name']}_id_card.pdf"
        pdf.output(pdf_output_path)
        print(f"ID card PDF generated and saved at: {pdf_output_path}")
        return pdf_output_path







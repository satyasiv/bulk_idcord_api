import os
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
# from Project.id_card.muthoot_loan import  Muthoot_Idcreation
from id_card.muthoot_loan import  Muthoot_Idcreation
from id_card.muthoot_id import  Muthoot_creation

from id_card.hdfc_id import  Hdfc_Idcreation
from rest_framework import status

class Id_Creation(APIView):
    def post(self, request):
        user_data = {
            'Name': request.data.get('name'),
            'Employee_id': request.data.get('employee_id'),
            'Designation': request.data.get('designation'),
            'Contact_No.': request.data.get('contact_no', 'N/A'),
            'Blood_Group': request.data.get('Blood_Group', 'N/A'),
            'DOJ': request.data.get('DOJ'),
            'Department': request.data.get('department'),
            'Location': request.data.get('location'),
            'Photo_path': request.data.get('photo_path'),
            'Legal_entity': request.data.get('legal_entity', '').lower()
        }
        print(user_data,"userdata")
        print(user_data['Legal_entity'])
        if user_data['Legal_entity'] == 'muthoot_loan':
            data = Muthoot_Idcreation(user_data)
            data.generate_pdf()
            print(data,"return_status")
            return Response({"message": "Muthoot Loan card generated successfully"}, status=status.HTTP_200_OK)
        elif  user_data['Legal_entity'] == 'idfc': 
            data = Hdfc_Idcreation(user_data)
            data.generate_pdf()
            return Response({"message": "idfc generated successfully"}, status=status.HTTP_200_OK)
        elif  user_data['Legal_entity'] == 'muthoot': 
            data = Muthoot_creation(user_data)
            data.generate_pdf()
            return Response({"message": "Muthoot generated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid Legal Entity"}, status=status.HTTP_200_OK)
        








#1.mouthot
#2.hdfc -- idfc 
#3.muthoot loan at home 
















# # DIRECT PDF
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .id_card_gen import IDCardGenerator  # Correct import for IDCardGenerator
# from .idfc_id import id_fc  # Assuming this is the IDFC-specific function
# from django.http import HttpResponse
# import os
# from datetime import datetime
# from fpdf import FPDF  # Importing FPDF here to create a PDF object

# class GenerateIDCard(APIView):
#     def post(self, request):
#         user_data = {
#             'name': request.data.get('name'),
#             'employee_id': request.data.get('employee_id'),
#             'designation': request.data.get('designation'),
#             'Emergency_Contact_No.': request.data.get('Emergency_Contact_No.', 'N/A'),
#             'Blood_Group': request.data.get('Blood_Group', 'N/A'),
#             'DOJ': request.data.get('DOJ'),
#             'department': request.data.get('department'),
#             'location': request.data.get('location'),
#             'photo_path': request.data.get('photo_path'),
#             'idfc_logo': request.data.get('idfc_logo', ''),  # Optional for IDFC
#             'buzzworks_logo': request.data.get('buzzworks_logo', '')  # Optional for all cases
#         }

#         print("=== User Data:", user_data)

#         # Ensure that required fields are provided
#         required_fields = ['name', 'employee_id', 'designation', 'DOJ', 'department', 'location', 'photo_path']
#         missing_fields = [field for field in required_fields if not user_data.get(field)]

#         if missing_fields:
#             return Response({
#                 'error': f'Missing fields: {", ".join(missing_fields)}'
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         # Check emergency contact validation
#         emergency_contact = user_data.get('Emergency_Contact_No.')
#         if emergency_contact != 'N/A' and (not emergency_contact.isdigit() or len(emergency_contact) != 10):
#             return Response({
#                 'error': "Emergency contact number must be a 10-digit number."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Validate the legal entity
#         legal_entity = request.data.get('legal_entity')
#         if legal_entity not in ["Muthoot", "IDFC"]:
#             return Response({
#                 'error': "Invalid legal entity. Please use either 'Muthoot' or 'IDFC'."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Generate a timestamp for the file name
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#             # Create the PDF object (necessary for generating the ID card and second page)
#             pdf = FPDF()
#             pdf.set_auto_page_break(auto=True, margin=15)

#             # Process ID card generation based on the legal entity
#             if legal_entity == "Muthoot":
#                 # Instantiate the IDCardGenerator for Muthoot
#                 id_card_generator = IDCardGenerator(user_data)

#                 # Generate the ID card and second page for Muthoot
#                 id_card_generator.generate_id_card(pdf)  # Pass the PDF object to generate the ID card
#                 id_card_generator.generate_second_page(pdf)  # Generate the second page using the same PDF object

#                 # Save the PDF to the desired path
#                 pdf_path = id_card_generator.generate_pdf()  # This will save the file and return its path

#             elif legal_entity == "IDFC":
#                 # Call the IDFC-specific ID card generation function (assuming it exists)
#                 id_card_generator = id_fc(user_data)

#                 # Generate the ID card and second page for IDFC
#                 id_card_generator.generate_id_card(pdf)  # Pass the PDF object to generate the ID card
#                 id_card_generator.generate_second_page(pdf)  # Generate the second page using the same PDF object

#                 # Save the PDF to the desired path
#                 pdf_path = id_card_generator.generate_pdf()  # This will save the file and return its path

#             # Add timestamp to the file name
#             pdf_path_with_timestamp = pdf_path.replace(".pdf", f"_{timestamp}.pdf")

#             # Rename the file with the timestamp
#             os.rename(pdf_path, pdf_path_with_timestamp)

#             # Return the path of the generated PDF
#             return Response({
#                 "message": "ID Card PDF generated successfully.",
#                 "pdf_path": pdf_path_with_timestamp  # Returning the path of the generated PDF with timestamp
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             # Handle error during generation
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)









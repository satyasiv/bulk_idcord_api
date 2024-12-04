import os
import subprocess
import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response

class Bulkprocess(APIView):
    def post(self, request):
        # Get the uploaded text file from the request
        text_file = request.FILES.get('text_file')  # 'text_file' is the key used in the form-data
        print(text_file, "text_file")

        if not text_file:
            return Response({"error": "No file uploaded"}, status=400)
        
        # Log the uploaded file name for debugging
        print(f"Uploaded File: {text_file.name}")

        # Create a dynamic output directory based on the uploaded file name (without extension)
        output_directory = f"/home/buzzadmin/Desktop/id_card_api/Project/id_card/{text_file.name.split('.')[0]}/"        
        os.makedirs(output_directory, exist_ok=True)        
        file_path = os.path.join(output_directory, text_file.name)        
        with open(file_path, 'wb') as f:
            for chunk in text_file.chunks():  # Efficient way to handle large files
                f.write(chunk)
        print(f"File saved at: {file_path}")
        robot_path = "/home/buzzadmin/Desktop/id_card_api/Project/id_card/bulk.robot"
        
        try:
            # Command to run Robot Framework test with the file path
            command = [
                'robot',
                '--variable', f'bulk_file:{file_path}',  # Pass the file path to Robot Framework as a variable
                '--outputdir', output_directory,
                '--log', f'{output_directory}/log.html',
                '--report', f'{output_directory}/report.html',
                '--output', f'{output_directory}/output.xml',
                robot_path
            ]
            
            # Run the Robot Framework command and capture the output data
            result = subprocess.run(command, capture_output=True)
            
            # Log the output of the Robot Framework execution for debugging
            print('Result:', result)
            print('stdout:', result.stdout.decode())
            print('stderr:', result.stderr.decode())

            # If Robot Framework returned output data directly, capture it
            output_data = result.stdout.decode().strip()

            # Use regex to extract the relevant 'output_data' part
            match = re.search(r"{'output_data':.*?}", output_data)
            if match:
                output_data = match.group(0)  # Extract matched part
            else:
                output_data = "No output_data found."

        except Exception as e:
            print("An error occurred during the execution:", str(e))
            return Response({"error": "An error occurred during execution"}, status=500)
        
        # Return a success response with the file path and only the relevant output_data
        return Response({"Remarks": output_data}, status=200)

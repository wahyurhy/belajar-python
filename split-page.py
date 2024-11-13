# pip install PyPDF2

import os
from datetime import datetime
import PyPDF2

def split_pdf(input_pdf_path, participant_names):
    # Get the current date and time to create a unique folder name
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = f"Sertifikat_{current_datetime}"
    
    # Create the output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the PDF file
    with open(input_pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page_count = len(pdf_reader.pages)
        
        print(f"Total pages in PDF: {page_count}")
        
        # Check if the number of names matches the number of pages
        if len(participant_names) != page_count:
            print("Error: The number of names does not match the number of pages.")
            print(f"Please provide exactly {page_count} participant names.")
            return
        
        # Process each page and save it with the participant's name
        for i, name in enumerate(participant_names):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[i])
            
            # Sanitize name to avoid invalid characters in filenames
            sanitized_name = "".join(c if c.isalnum() or c.isspace() else "_" for c in name).replace(" ", "_")
            output_pdf_path = os.path.join(output_folder, f"{sanitized_name}.pdf")
            
            # Write the single-page PDF
            with open(output_pdf_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
            
            print(f"Saved page {i + 1} as {output_pdf_path}")

# List of participant names (replace with actual names, ensuring it matches the page count)
participant_names = [
    f"Participant Name {i+1}" for i in range(37)  # Replace with actual names as needed
]

# Path to the input PDF file
input_pdf_path = "D:\\sert.pdf"

# Run the split function
split_pdf(input_pdf_path, participant_names)

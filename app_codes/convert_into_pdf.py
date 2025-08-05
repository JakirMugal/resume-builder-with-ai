from xhtml2pdf import pisa
from io import BytesIO
import json
import pandas as pd
import os

def create_pdf_via_html(base_path):
    resume_html_path = rf"{base_path}\job_resume_html.json"
    resume_folder_path = rf"{base_path}\Resumes"
    job_resume_combined_path = rf"{base_path}\job_resume_combined.csv"
    os.makedirs(resume_folder_path, exist_ok=True)
    with open(resume_html_path,"r") as file:
        jobs = json.loads(file.read())
    meta=[]
    for job,data in jobs.items():
        print(f"Processing Job: {job}")
        filename = job.replace(".html",".pdf")
        
        full_path = os.path.join(resume_folder_path, filename)
        meta.append(
            {
                'Company':data['company'],
                'Location':data['location'],
                'Position':data['position'],
                'Link':data['link'],
                "Resume Path":full_path
            }
        )
        if os.path.exists(full_path):
            print(f"{filename} already present.....")
            continue
        reply = data['resume_html']
        pdf_buffer = BytesIO()
        pisa.CreatePDF(reply, dest=pdf_buffer)
        pdf_buffer.seek(0)

        # Save to file
        with open(full_path, "wb") as f:
            f.write(pdf_buffer.getbuffer())

        print(f"PDF saved as {filename}")


    df=pd.DataFrame(meta)
    df.to_csv(job_resume_combined_path,index=False)



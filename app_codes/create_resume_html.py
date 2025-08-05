import json
from groq import Groq
import os

def create_html_by_ai(base_path,profile_name='profile',api_key=None):
    job_description_summary = rf"{base_path}\job_description_summary.json"
    personal_details = rf"{base_path}\{profile_name}.txt"
    job_resume_html = rf"{base_path}\job_resume_html.json"
    with open(job_description_summary,"r") as file:
        jobs = json.loads(file.read())
    with open(personal_details, "r", encoding="utf-8") as file:
        user_resume = file.read().replace('–','-')
    if os.path.exists(job_resume_html):
        with open(job_resume_html, "r", encoding="utf-8") as file:
            already_processed_data = json.load(file)
    else:
        already_processed_data = {}


    client = Groq(api_key=api_key)
    description_prompt = """
    You are an expert resume formatter. Generate a **clean and ATS-friendly HTML resume** using the information I will provide.

    🎯 Follow this structure:

    1. Center the candidate’s **name** at the top in large, colored text.
    2. Below the name, add personal information (smaller font, inline, pointer-separated):
    - ➤ Email (as a clickable hyperlink where link word should be Email)
    - ➤ Phone : number
    - ➤ LinkedIn (as a clickable hyperlink where link word should be LinkedIn)
    - ➤ GitHub (as a clickable hyperlink where link word should be GitHub)
    - ➤ Education : text
    In this Email Phone linkedIn and Git present in a single line and Education in next line and please use  ➤ with every pointer. And do not make too much new lines between these.
    3. Add these **sections with headings in 14px colored font**:
        - **Professional Summary**
        - **Skills**
        - **Work Experience**
        - **Projects**
        - **Certifications**
        - **Achievements**

    📌 Important Instructions:
    - Always include **Projects** and **Work Experience** in the output.
    - **Order the Projects based on relevance to the job description.**
    - Bold all **company names** in Work Experience and Projects.
    - Use a clean, modern font like Segoe UI or Arial.
    - Font sizes: 
        - `h1`: 18px
        - `h2`: 14px
        - list items and content: 11px
    - Color scheme: use `#1e3a8a` for headings and `#2563eb` for links.
    - ✅ Do **not** insert extra line breaks between bullet points — keep spacing minimal to reduce page size.

    🎨 Add this CSS in a `<style>` tag inside the HTML head:

    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
            margin: 40px;
            color: #222;
            background-color: #f9f9f9;
        }
        h1 {
            font-size: 18px;
            text-align: center;
            color: #1e3a8a;
            margin-bottom: 5px;
        }
        .personal-info {
            text-align: center;
            font-size: 11px;
            color: #444;
            margin-bottom: 20px;
        }
        .personal-info span {
            display: inline-block;
            margin: 0 10px;
        }
        h2 {
            font-size: 14px;
            color: #1e3a8a;
            margin-bottom: 6px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 2px;
        }
        ul {
            padding-left: 16px;
            margin-top: 0;
            margin-bottom: 4px;
        }
        ul li {
            font-size: 11px;
            margin-bottom: 2px;
        }
        b {
            color: #000;
        }
        a {
            color: #2563eb;
            text-decoration: none;
        }
    </style>

    📥 Now, take the user resume data and output a full valid HTML document — compact, styled, and optimized."""
    meta={}
    for job,data in jobs.items():
        print(f"Processing Job: {job}")
        if job in already_processed_data:
            print(f"{job} is already proccesed")
            meta[job]=already_processed_data[job]
            meta[job]['company']=data['company']
            meta[job]['position']=data['position']
            meta[job]['location']=data['location']
            continue
        job_description=data['description_summary'].strip()
        information = f"""
        ----------------------
        ### USER PROFESSIONAL SUMMARY
        {user_resume}

        ----------------------
        ### JOB DESCRIPTION
        {job_description}
        ----------------------

        Please return only the final HTML resume code.
        📥 Now, take the user resume data and output a full valid HTML document.
        """
        user_prompt = f"{description_prompt}\n{information}"
        response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {"role": "user", "content": user_prompt}
                        ],
                    temperature=0.2,
                    max_tokens=1024*8,
                )
        reply = response.choices[0].message.content
        data['resume_html']=reply
        meta[job] = data
        already_processed_data[job]=data
    with open(job_resume_html,'w') as file:
        file.write(json.dumps(meta))







import os
import shutil
import streamlit as st
from scrape_jobs import scrape_and_upload
from get_job_details import get_details_from_html
from create_job_description_summary import create_summary
from create_resume_html import create_html_by_ai
from convert_into_pdf import create_pdf_via_html

# Default values
default_url = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&f_E=3&f_TPR=&f_WT=2&position=1&pageNum=0"
default_profile_name = "profile"

# Page config
st.set_page_config(page_title="Create Customized Resume with AI & LinkedIn", layout="centered")
st.title("📝 Create Customized Resume with AI & LinkedIn")

# Instructions for non-technical users
st.markdown("""
Paste a LinkedIn filtered jobs URL and let the app automatically collect jobs, process details, summarize descriptions, 
and generate customized resumes for each job posting.  

**Steps:**
1. Paste your LinkedIn search URL with filters applied.  
2. Enter your profile `.txt` filename (without extension) stored in the app folder.  
3. Set the number of jobs to collect.  
4. Click **Start** and wait for the process to complete.  

⚠ Keep LinkedIn open in your browser for best results.
""")

# Inputs
url = st.text_input("🔗 LinkedIn filtered URL:", value=default_url)
number_of_jobs = st.number_input("📊 Number of jobs to collect:", min_value=1, value=2, step=1)
profile_name = st.text_input("👤 Profile text file name (without .txt):", value=default_profile_name)

# Fixed base_path
base_path = os.path.join(os.getcwd(), "data")
os.makedirs(base_path, exist_ok=True)

# Run pipeline
if st.button("🚀 Start"):
    steps = [
        (f"📥 Collecting {number_of_jobs} jobs from LinkedIn...", lambda: scrape_and_upload(base_path, url, number_of_jobs=number_of_jobs)),
        ("🔍 Processing job details...", lambda: get_details_from_html(base_path)),
        ("📝 Summarizing job descriptions...", lambda: create_summary(base_path)),
        ("🎨 Creating resumes...", lambda: create_html_by_ai(base_path, profile_name=profile_name)),
        ("📄 Converting resumes to PDF and CSV...", lambda: create_pdf_via_html(base_path)),
    ]

    try:
        for step_msg, step_func in steps:
            with st.spinner(step_msg):
                step_func()
            st.success(f"✅ {step_msg.replace('...', '')} Done.")

        # Show folder path
        st.success(f"📂 All files saved in: `{base_path}`")

        # Create and offer ZIP download
        zip_path = f"{base_path}.zip"
        shutil.make_archive(base_path, 'zip', base_path)
        with open(zip_path, "rb") as zip_file:
            st.download_button(
                label="⬇️ Download All Files as ZIP",
                data=zip_file,
                file_name="data.zip",
                mime="application/zip"
            )

    except FileNotFoundError:
        st.error(f"❌ Profile file not found.\nPlease put your `.txt` file in this location: `{base_path}`")
    except Exception as e:
        st.error(f"❌ Error: {e}")

import os
import streamlit as st
from scrape_jobs import scrape_and_upload
from get_job_details import get_details_from_html
from create_job_description_summary import create_summary
from create_resume_html import create_html_by_ai
from convert_into_pdf import create_pdf_via_html

# Default values
default_url = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&f_E=3&f_TPR=&f_WT=2&position=1&pageNum=0"
default_folder_name = "data"  # Fixed default folder name
default_profile_name = "profile"  # without extension

# App title
st.set_page_config(page_title="Create Customized Resume with AI & LinkedIn", layout="centered")
st.title("📝 Create Customized Resume with AI & LinkedIn")

# Simple instructions
st.markdown("""
This tool will help you collect jobs from LinkedIn and prepare resumes for them automatically.  

**Steps:**
1. Paste a LinkedIn search URL with your filters applied.  
2. Enter the base directory path where files will be saved.  
3. Enter a folder name (default is `"data"`).  
4. Type the name of your profile text file (without `.txt`).  
5. Choose how many jobs you want to collect.  
6. Click **Start** and wait until it finishes.  

⚠ Keep your LinkedIn page open in the background to avoid login issues.
""")

# User inputs
url = st.text_input("🔗 Please paste a LinkedIn filtered URL:", value=default_url)
base_directory = st.text_input("📂 Enter the base directory path:", value=os.getcwd())
folder_name = st.text_input("📁 Folder name to save data:", value=default_folder_name)
number_of_jobs = st.number_input("📊 Number of jobs to collect:", min_value=1, value=2, step=1)
profile_name = st.text_input("👤 Your profile text file name (without .txt):", value=default_profile_name)

# Run pipeline
if st.button("🚀 Start"):
    base_path = os.path.join(base_directory, folder_name)
    os.makedirs(base_path, exist_ok=True)

    try:
        with st.spinner(f"📥 Collecting {number_of_jobs} jobs from LinkedIn..."):
            dict_of_folders = scrape_and_upload(base_path, url, number_of_jobs=number_of_jobs)
        st.success("✅ Job collection complete.")
        st.markdown(f"Job HTML Folder Path : {dict_of_folders['html_path']}\nJson Folder Path: {dict_of_folders['json_path']}")

        with st.spinner("🔍 Processing job details..."):
            get_details_from_html(base_path)
        st.success("✅ Job details processed.")

        with st.spinner("📝 Summarizing job descriptions..."):
            create_summary(base_path)
        st.success("✅ Summaries ready.")

        with st.spinner("🎨 Creating resumes..."):
            try:
                create_html_by_ai(base_path, profile_name=profile_name)
                st.success("✅ HTML resumes created.")
            except FileNotFoundError:
                st.error(f"❌ Profile file not found.\nPlease put your `.txt` file in this location: `{base_path}`")
                st.stop()

        with st.spinner("📄 Converting resumes to PDF and CSV..."):
            create_pdf_via_html(base_path)
        st.success("✅ PDF and CSV files created.")

        st.markdown(f"📂 **All files saved in:** `{base_path}`")

    except Exception as e:
        st.error(f"❌ Error: {e}")

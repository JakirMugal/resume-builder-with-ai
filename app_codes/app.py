import os
import shutil
import streamlit as st
from scrape_jobs import scrape_and_upload
from get_job_details import get_details_from_html
from create_job_description_summary import create_summary
from create_resume_html import create_html_by_ai
from convert_into_pdf import create_pdf_via_html

# Default LinkedIn jobs URL
default_url = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&f_E=3&f_TPR=&f_WT=2&position=1&pageNum=0"

# Streamlit page setup
st.set_page_config(page_title="Create Customized Resume with AI & LinkedIn", layout="centered")
st.title("📝 Create Customized Resume with AI & LinkedIn")

# Instructions
st.markdown("""
Paste a LinkedIn filtered jobs URL and let the app automatically collect jobs, process details, summarize descriptions, 
and generate customized resumes for each job posting.  

**Steps:**
1. Paste your LinkedIn search URL with filters applied.  
2. Upload your profile `.txt` file (contains your resume details).  
3. Set the number of jobs to collect.  
4. Click **Start** and wait for the process to complete.  

⚠ Keep LinkedIn open in your browser for best results.
""")

# Inputs
url = st.text_input("🔗 LinkedIn filtered URL:", value=default_url)
number_of_jobs = st.number_input("📊 Number of jobs to collect:", min_value=1, value=2, step=1)

# Fixed base path
base_path = os.path.join(os.getcwd(), "data")
os.makedirs(base_path, exist_ok=True)

# Upload profile.txt
uploaded_file = st.file_uploader("📤 Upload your profile .txt file", type=["txt"])
profile_name = "profile"  # fixed name used by create_html_by_ai

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode("utf-8")
        profile_path = os.path.join(base_path, f"{profile_name}.txt")
        with open(profile_path, "w", encoding="utf-8") as f:
            f.write(content)
        st.success(f"✅ Profile file uploaded successfully and saved as 'profile.txt' on {profile_path}")
    except Exception as e:
        st.error(f"❌ Error reading uploaded file: {e}")

# Run pipeline
if st.button("🚀 Start"):
    profile_path = os.path.join(base_path, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        st.error("❌ Please upload your profile `.txt` file before starting.")
    else:
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

            # Show full folder path
            full_path = os.path.abspath(base_path)
            st.success(f"📂 All files saved in: `{full_path}`")

            # Create and offer ZIP download
            zip_path = f"{full_path}.zip"
            shutil.make_archive(full_path, 'zip', full_path)
            with open(zip_path, "rb") as zip_file:
                st.download_button(
                    label="⬇️ Download All Files as ZIP",
                    data=zip_file,
                    file_name="data.zip",
                    mime="application/zip"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")

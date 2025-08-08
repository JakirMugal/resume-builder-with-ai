import os
import json
import streamlit as st
import shutil
import base64

from scrape_jobs import scrape_and_upload
from get_job_details import get_details_from_html
from create_job_description_summary import create_summary
from create_resume_html import create_html_by_ai
from convert_into_pdf import create_pdf_via_html


# ========== Helper Functions ==========

def make_download_button(file_path, label):
    """Creates a Streamlit download link for a file."""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/zip;base64,{b64}" download="{os.path.basename(file_path)}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def prepare_downloads(base_path):
    """Create zips for all data and for Resumes + CSV only."""
    resume_folder_path = os.path.join(base_path, "Resumes")
    csv_path = os.path.join(base_path, "job_resume_combined.csv")

    # ZIP for All Data
    all_data_zip = os.path.join(base_path, "All_Data.zip")
    shutil.make_archive(all_data_zip.replace(".zip", ""), 'zip', base_path)

    # ZIP for Resumes + CSV
    resume_zip = os.path.join(base_path, "Resumes_and_CSV.zip")
    temp_dir = os.path.join(base_path, "temp_download")
    os.makedirs(temp_dir, exist_ok=True)

    if os.path.exists(resume_folder_path):
        shutil.copytree(resume_folder_path, os.path.join(temp_dir, "Resumes"))
    if os.path.exists(csv_path):
        shutil.copy(csv_path, os.path.join(temp_dir, "job_resume_combined.csv"))

    shutil.make_archive(resume_zip.replace(".zip", ""), 'zip', temp_dir)
    shutil.rmtree(temp_dir)

    return all_data_zip, resume_zip

def delete_all_data(base_path):
    """Delete all files and folders inside the base path."""
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
        os.makedirs(base_path, exist_ok=True)


# ========== Streamlit App ==========

st.title("🔧 AI Resume Builder App")
st.markdown("""
### 📋 Instructions:
1. Go to [LinkedIn Jobs](https://www.linkedin.com/jobs/) and filter jobs based on your preferences (e.g., location, experience, remote, etc.).
2. Copy the filtered **LinkedIn Jobs URL** that lists many jobs.
3. Create a `.txt` file (you can copy from your long detailed CV) and **upload it** as your user profile.
4. Enter how many resumes you want to generate.
5. Hit **🚀 Start Resume Creation**. After a few seconds, download your results.
""")

# Default values
default_url = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&f_E=3&f_TPR=&f_WT=2&position=1&pageNum=0"
default_folder = "data"

# Inputs
url = st.text_input("LinkedIn Jobs URL", value=default_url)
num_jobs = st.number_input("Number of Jobs to Scrape", min_value=1, max_value=50, value=2, step=1)
uploaded_file = st.file_uploader("Upload your profile (.txt)", type=["txt"])
profile_name = "profile"

# Ensure base path exists
base_path = os.path.join(os.getcwd(), default_folder)
os.makedirs(base_path, exist_ok=True)

if uploaded_file is not None:
    profile_path = os.path.join(base_path, f"{profile_name}.txt")
    with open(profile_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Profile file saved at: {profile_path}")

if st.button("🚀 Start Resume Creation"):
    # Check profile exists
    profile_path = os.path.join(base_path, f"{profile_name}.txt")
    if not os.path.exists(profile_path):
        st.error(f"❌ Profile file not found at {profile_path}. Please upload it above.")
        st.stop()

    with st.spinner("🔍 Gathering Job Data..."):
        scrape_and_upload(base_path, url, number_of_jobs=num_jobs)
    st.success("✅ Job data gathering complete.")

    with st.spinner("📄 Extracting Job Details..."):
        get_details_from_html(base_path)
    st.success("✅ Job details extraction done.")

    with st.spinner("📝 Summarizing Job Descriptions..."):
        create_summary(base_path)
    st.success("✅ Job description summaries created.")

    with st.spinner("🎨 Creating HTML Resumes via AI..."):
        create_html_by_ai(base_path, profile_name=profile_name)
    st.success("✅ HTML resumes created.")

    with st.spinner("📄 Converting HTML to PDF..."):
        create_pdf_via_html(base_path)
    st.success("✅ PDF resumes generated.")

    # Prepare download zips
    all_data_zip, resume_zip = prepare_downloads(base_path)

    st.subheader("📥 Download Your Files")
    make_download_button(all_data_zip, "⬇️ Download All Data (ZIP)")
    make_download_button(resume_zip, "⬇️ Download Resumes + CSV (ZIP)")

    # Clean up
    delete_all_data(base_path)
    st.info("🧹 All temporary data has been cleaned after download.")

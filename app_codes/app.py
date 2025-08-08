import streamlit as st
import os
import shutil
from scrape_jobs import scrape_and_upload
from get_job_details import get_details_from_html
from create_job_description_summary import create_summary
from create_resume_html import create_html_by_ai
from convert_into_pdf import create_pdf_via_html
from zipfile import ZipFile
from pathlib import Path
import tempfile

# ---------------- INSTRUCTIONS ----------------
st.title("🔧 AI Resume Builder App")

st.markdown("""
### 📋 Instructions:
1. Go to [LinkedIn Jobs](https://www.linkedin.com/jobs/) and filter jobs based on your preferences (e.g., location, experience, remote, etc.).
2. Copy the filtered **LinkedIn Jobs URL** that lists many jobs.
3. Create a `.txt` file (you can copy from your long detailed CV) and **upload it** as your user profile.
4. Enter how many resumes you want to generate.
5. Hit **Process**. After a few seconds, download your results.
""")

# ---------------- INPUT SECTION ----------------
# LinkedIn job URL
url = st.text_input("🔗 Enter filtered LinkedIn Jobs URL:")

# Upload profile.txt
uploaded_file = st.file_uploader("📄 Upload your profile.txt file (a long text version of your resume)", type="txt")

# Number of resumes
num_resumes = st.number_input("📌 Number of resumes to generate:", min_value=1, step=1)

# Submit button
if st.button("🚀 Process"):
    if not uploaded_file or not url:
        st.warning("Please upload profile.txt and paste a valid LinkedIn jobs URL.")
    else:
        # Step 1: Set base data folder
        base_path = Path(__file__).resolve().parent / "data"
        base_path.mkdir(parents=True, exist_ok=True)

        # Step 2: Save profile.txt
        profile_path = base_path / "profile.txt"
        with open(profile_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ Profile uploaded successfully.")

        # Step 3: Scrape and save jobs
        st.info("🔍 Scraping jobs...")
        scrape_and_upload(base_path, url)
        st.success("✅ Job scraping complete.")

        # Step 4: Extract job details
        st.info("📄 Extracting job details...")
        get_details_from_html(base_path)
        st.success("✅ Job details extracted.")

        # Step 5: Create summaries
        st.info("🧠 Creating job description summaries...")
        create_summary(base_path)
        st.success("✅ Job description summaries done.")

        # Step 6: Create HTMLs using AI
        st.info("🤖 Generating HTML resumes using AI...")
        create_html_by_ai(base_path, num_resumes)
        st.success("✅ HTML generation done.")

        # Step 7: Convert HTML to PDF resumes
        st.info("📝 Creating final resume PDFs...")
        create_pdf_via_html(base_path)
        st.success("✅ Resume creation complete!")

        st.success("🎉 All tasks completed! You can now download your data.")

        # Store generated path for download buttons
        st.session_state["base_path"] = base_path

# ---------------- DOWNLOAD SECTION ----------------
if "base_path" in st.session_state:
    base_path = st.session_state["base_path"]

    def zip_folder_and_download(source_paths, zip_name):
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, zip_name)

        with ZipFile(zip_path, 'w') as zipf:
            for path in source_paths:
                path = Path(path)
                if path.is_file():
                    zipf.write(path, arcname=path.name)
                elif path.is_dir():
                    for root, _, files in os.walk(path):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(base_path)
                            zipf.write(file_path, arcname=arcname)

        return zip_path

    st.subheader("📦 Download Results")

    # Download all data
    if st.button("⬇️ Download ALL data"):
        zip_file_path = zip_folder_and_download([base_path], "all_data.zip")
        with open(zip_file_path, "rb") as f:
            st.download_button("📁 Download All Data (ZIP)", f, file_name="all_data.zip")

    # Download only CSV and resumes
    if st.button("⬇️ Download CSV + Resumes only"):
        csv_path = base_path / "job_resume_combined.csv"
        resume_folder = base_path / "Resumes"
        zip_file_path = zip_folder_and_download([csv_path, resume_folder], "resumes_and_csv.zip")
        with open(zip_file_path, "rb") as f:
            st.download_button("📁 Download CSV + Resumes (ZIP)", f, file_name="resumes_and_csv.zip")

# ---------------- CLEANUP OPTION ----------------
    st.markdown("🗑️ *Data is stored temporarily in the app and will be cleared on next run.*")


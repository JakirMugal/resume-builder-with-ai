# 🚀 RESUME-BUILDER-WITH-AI

This project is an intelligent, automated resume generator that scrapes LinkedIn job postings and generates **customized, job-specific resumes** using **Large Language Models (LLMs)**. Ideal for job seekers aiming to tailor their resumes to specific job descriptions in seconds.

---

## 📁 Folder Structure

```
RESUME-BUILDER-WITH-AI/
│
├── common_lib/                  # Reusable scripts and modules
├── job_data/                    # Contains scraped HTML job pages
├── Resumes/                     # Stores generated resume PDFs
├── venv/                        # Virtual environment
│
├── convert_into_pdf.ipynb       # Converts HTML resumes into PDFs
├── create_job_description_summary.ipynb  # Summarizes job descriptions using LLM
├── create_resume_html.ipynb     # Generates customized HTML resumes using LLM
├── get_job_details.ipynb        # Extracts job info using Scrapy
├── scrape_jobs.ipynb            # Scrapes LinkedIn job listings using Selenium
│
├── job_description.json         # Raw extracted job details
├── job_description_summary.json # Summarized job descriptions
├── job_resume_html.json         # LLM-generated HTML resumes
├── job_resume_combined.csv      # Metadata of all generated resumes
├── link_path_data.json          # Maps job file names to LinkedIn URLs
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
```

---

## ⚙️ Project Workflow

### 1. **Scrape LinkedIn Jobs** (`scrape_jobs.ipynb`)
- Uses **Selenium** to open a LinkedIn search URL with multiple job listings.
- Scrapes individual job HTML pages.
- Saves:
  - Raw HTML files in `job_data/`
  - Mapping in `link_path_data.json`:
    ```json
    {
      "job-file-name.html": {
        "path": "absolute_path_to_html_file",
        "link": "original_linkedin_job_url"
      }
    }
    ```

---

### 2. **Extract Job Details** (`get_job_details.ipynb`)
- Parses HTML using `scrapy.Selector`.
- Extracts:
  - Position
  - Company
  - Location
  - Full job description
- Saves to `job_description.json`.

---

### 3. **Summarize Job Descriptions** (`create_job_description_summary.ipynb`)
- Uses **GROQ + LLM** to create a concise, structured summary of each job description.
- Output stored in `job_description_summary.json`.

---

### 4. **Generate Custom HTML Resume** (`create_resume_html.ipynb`)
- Takes:
  - User’s profile info
  - Summarized job description
- Uses **GROQ + LLM** to generate a **customized HTML resume**.
- Saves to `job_resume_html.json`.

---

### 5. **Convert to PDF** (`convert_into_pdf.ipynb`)
- Converts the HTML resumes into **PDF format** using `xhtml2pdf`.
- Stores PDFs in `Resumes/`
- Also generates a CSV: `job_resume_combined.csv` with:
  - Resume path
  - Company
  - Position
  - Location
  - Job link

---

## 📦 Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## 💡 Tech Stack

- **Selenium** – Job scraping  
- **Scrapy Selectors** – HTML parsing  
- **GROQ (LLM)** – Job summary & resume generation  
- **xhtml2pdf** – HTML to PDF conversion  
- **Jupyter Notebooks** – Modular development

---

## 🔚 Output Example

Generated PDF resumes are saved in the `Resumes/` folder with metadata tracked in `job_resume_combined.csv`.

---

## 📬 Contact

For any questions, feel free to connect:  
📧 jakirmugal7867@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/thejakirhusain) | [GitHub](https://github.com/JakirM)

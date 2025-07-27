# 💼 AI Resume Builder

A smart resume generator that builds customized resumes based on LinkedIn job descriptions and your experience using AI.

---

## 📌 Overview

AI Resume Builder allows you to:

1. Enter job filters via a user-friendly Streamlit interface.
2. Scrape LinkedIn to find jobs matching your filters.
3. Upload your knowledge document (skills, experience, achievements).
4. Use AI to tailor a resume specifically for the selected job.
5. Save the resume locally in `.docx` or `.pdf` format.

---

## 🚀 Features

- 🌐 Streamlit-based UI
- 🔍 LinkedIn job scraping based on filters
- 📄 Upload personal experience document
- 🧠 AI-powered resume generation using job descriptions
- 💾 Export resume to local file system

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python, OpenAI API (or any LLM)
- **Scraping:** BeautifulSoup, Requests, (optional: Selenium)
- **File Export:** `python-docx`, `fpdf`, or `reportlab`

---

## 📂 Project Structure

```
ai-resume-builder/
│
├── app.py                  # Main Streamlit application
├── scraper.py              # LinkedIn scraping logic
├── resume_generator.py     # AI resume generation logic
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/ai-resume-builder.git
cd ai-resume-builder
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set API Key**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Or directly set it in your environment variables.

---

## ▶️ Usage

1. Run the application:

```bash
streamlit run app.py
```

2. Enter job filters (title, location, etc.)
3. Upload your knowledge/experience document
4. Select a job from the scraped LinkedIn results
5. Let the AI generate a resume tailored to that job
6. Download the resume to your device

---

## 📎 Example Knowledge Document

Your knowledge document can include:

```
- Work Experience
- Skills
- Projects
- Certifications
- Tools/Technologies
```

It should be a `.txt`, `.docx`, or `.pdf` file with all relevant professional info.

---

## ⚠️ Legal Notice

This project is for personal and educational purposes only.

> **Note:** Scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement). Use this tool responsibly.

---

## 🚧 Future Improvements

- Support other job boards (Indeed, Glassdoor)
- Resume design templates
- Interactive resume editing
- Auto-update via GitHub/portfolio links
- Cloud storage integration

---

## 👤 Author

Made with ❤️ by [Jakir Husain](https://github.com/JakirMugal?tab=repositories)


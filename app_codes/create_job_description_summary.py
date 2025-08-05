import json
import os
from groq import Groq
def create_summary(base_path,api_key=None):
    job_description = rf"{base_path}\job_description.json"
    job_description_summary = rf"{base_path}\job_description_summary.json"
    client = Groq(api_key=api_key)
    user_prompt ="""
                You are a professional resume and job-fit analyst.

                Given the following job description, summarize who is eligible to apply for this role. Focus on both required and preferred qualifications and skills.

                Only include what is clearly stated or strongly implied. Avoid generic language unless explicitly mentioned.

                Present the output as a clean and concise bullet list with no extra commentary.

                ### Job Description:
                {job_description}
                """
    with open(job_description,"r") as file:
        jobs = json.loads(file.read())
    if os.path.exists(job_description_summary):
        with open(job_description_summary, "r", encoding="utf-8") as file:
            already_processed_data = json.load(file)
    else:
        already_processed_data = {}
    meta={}
    for job,data in jobs.items():
        print(f"Processing Job: {job}")
        if job in already_processed_data:
            print(f"{job} is already proccesed")
            meta[job]=already_processed_data[job]
            continue
        job_description=data['description'].strip()
        response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {"role": "user", "content": user_prompt.format(job_description=job_description)}
                        ],
                    temperature=0.3,
                    max_tokens=1024*8,
                )
        reply = response.choices[0].message.content
        data['description_summary'] = reply
        meta[job]=data

    with open(job_description_summary,'w') as file:
        file.write(json.dumps(meta))




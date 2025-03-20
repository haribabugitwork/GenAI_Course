from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import pymupdf  # PyMuPDF for PDF extraction
import ollama
import json

@CrewBase
class MyMedicalCrew():
    """Crew for processing blood test reports"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def blood_report_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['blood_report_analyzer'],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    @task
    def extract_blood_report(self) -> Task:
        return Task(
            config=self.tasks_config['extract_blood_report'],
            run=self.process_blood_report
        )

    @task
    def generate_medical_summary(self) -> Task:
        return Task(
            config=self.tasks_config['generate_medical_summary'],
            run=self.generate_summary
        )

    def process_blood_report(self):
        """Extracts text from the PDF and processes it into structured JSON using LLaMA."""
        extracted_text = self.extract_text_from_pdf()

        # Define LLaMA prompt
        prompt = f"""
        You are an expert in medical document analysis. Convert the following blood test report into structured JSON.
        
        **Report Text:**
        {extracted_text}

        **Expected JSON Format:**
        {{
          "Patient Information": {{
            "Name": "John Doe",
            "Sex": "Male",
            "Age": "35",
            "DOB": "01-Feb-1982",
            "Report Date": "20-Feb-2023"
          }},
          "Test Results": {{
            "Hemoglobin (g/dL)": 14.5,
            "WBC Count (/cmm)": 10570,
            "RBC Count (million/cmm)": 4.79,
            "Platelet Count (/cmm)": 150000,
            "MCV (fL)": 90.3,
            "MCH (pg)": 30.2
          }},
          "Doctor's Remarks": "Normal blood report."
        }}

        **Return only the JSON output, no additional text.**
        """

        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        structured_json = response["message"]["content"]

        # Save JSON output
        json_path = "parsed_blood_report.json"
        with open(json_path, "w") as json_file:
            json.dump(json.loads(structured_json), json_file, indent=4)

        print(f"Blood report successfully parsed and saved to {json_path}")
        return structured_json

    def generate_summary(self):
        """Takes structured JSON data and converts it into a human-readable summary."""
        with open("parsed_blood_report.json", "r") as json_file:
            blood_report_data = json.load(json_file)

        # Prompt LLaMA to generate a medical summary
        prompt = f"""
        You are a medical reporting AI. Based on the following structured JSON blood report data,
        generate a readable medical report highlighting key findings, normal values, and abnormalities.

        **Blood Report Data:**
        {json.dumps(blood_report_data, indent=2)}

        **Expected Output:**
        - Patient Details
        - Test Results Summary
        - Any Abnormalities Detected
        - Recommendations (if any)

        Format the report in **Markdown (MD)** format.
        """

        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        medical_summary = response["message"]["content"]

        # Save Markdown output
        with open("medical_report.md", "w") as report_file:
            report_file.write(medical_summary)

        print(f"📄 Medical report saved to medical_report.md")

    def extract_text_from_pdf(self):
        """Extract text from a medical report PDF."""
        doc = pymupdf.open("Medical_Report.pdf")
        text = "\n".join(page.get_text("text") for page in doc if page.get_text("text"))
        return text

    @crew
    def crew(self) -> Crew:
        """Creates the MyMedicalCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

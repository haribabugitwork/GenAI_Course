#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from my_medical_crew.crew import MyMedicalCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the crew."""
    inputs = {
        'topic': 'Medical AI',
        'current_year': str(datetime.now().year)
    }
    
    try:
        MyMedicalCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()

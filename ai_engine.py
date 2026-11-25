
import os
import json

from dotenv import load_dotenv
from google import genai


# Load API key from .env file
load_dotenv()


def generate_ai_recommendations(student, career_matches):

    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key not found!")

    # Connect to Gemini
    client = genai.Client(api_key=api_key)

    # Prepare student information without personal identifiers
    student_profile = {
        "education": student["education"],
        "year": student["year"],
        "interests": student["interests"],
        "subjects": student["subjects"],
        "skills": student["skills"],
        "career_preference": student["career"]
    }

    # Prepare career matching results
    matching_results = career_matches[:5]

    # Create AI prompt
    prompt = f"""
    You are an expert career guidance counsellor for Indian students.

    Analyse the following student profile and career matching results.

    STUDENT PROFILE:
    {json.dumps(student_profile, indent=2)}

    PYTHON CAREER MATCHING RESULTS:
    {json.dumps(matching_results, indent=2)}

    YOUR TASK:

    1. Recommend the most suitable career options.
    2. Explain why each career may suit the student.
    3. Identify the student's existing strengths.
    4. Explain which skills the student needs to develop.
    5. Consider interests, subjects, education and career preference.
    6. Suggest practical projects for developing skills.
    7. Create a simple learning roadmap.

    IMPORTANT RULES:

    - Do not invent student skills.
    - Do not invent career requirements.
    - Do not treat matching percentages as guaranteed career suitability.
    - Explain when information is insufficient.
    - Use simple English.
    - Give practical and realistic advice for students in India.

    Format your response with clear headings and bullet points.
    """

    # Ask Gemini to analyse the profile
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    # Return AI-generated recommendations
    return response.text

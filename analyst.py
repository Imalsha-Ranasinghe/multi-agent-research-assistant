
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import get_secret

# load_dotenv()

api_key = get_secret("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)


def analyze_research(research_findings: str) -> str:
    """Analyze research findings and extract evidence-based insights."""

    prompt = f"""
    Analyze the following research findings.

    Your tasks:
    1. Identify the most important insights.
    2. Compare the main ideas and identify relationships.
    3. Identify contradictions or disagreements between sources.
    4. Highlight limitations and missing information.
    5. Suggest useful conclusions based only on the evidence provided.

    Do not invent facts, statistics, or sources.
    If the evidence is insufficient, clearly say so.
    Preserve source URLs when they are provided.

    RESEARCH FINDINGS:
    {research_findings}
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=800,
            system_instruction=(
                "You are an analytical research agent. "
                "Evaluate evidence critically and distinguish "
                "supported conclusions from assumptions."
            ),
        ),
    )

    return response.text or "The Analyst returned no text."


if __name__ == "__main__":
    print("Analyst Agent")
    print("Paste your research findings below.")
    print("When finished, enter a line containing only END.")

    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    findings = "\n".join(lines).strip()

    if findings:
        try:
            analysis = analyze_research(findings)
            print("\n--- ANALYSIS RESULTS ---\n")
            print(analysis)
        except Exception as error:
            print(f"Analysis failed: {error}")
    else:
        print("No research findings were provided.")

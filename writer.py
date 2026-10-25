
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


def write_report(
    research_findings: str,
    analysis: str,
) -> str:
    """Generate a structured report from research and analysis."""

    prompt = f"""
    Create a professional research report using the material below.

    Use this structure:

    # Research Report
    ## 1. Executive Summary
    ## 2. Introduction
    ## 3. Key Findings
    ## 4. Analysis and Discussion
    ## 5. Limitations
    ## 6. Conclusion
    ## 7. References

    Requirements:
    - Write clearly and avoid unnecessary repetition.
    - Base claims on the supplied research and analysis.
    - Preserve source titles and URLs where available.
    - Do not invent references, facts, or statistics.
    - Distinguish established findings from uncertain conclusions.
    - If references are missing, state that they need verification.

    RESEARCH FINDINGS:
    {research_findings}

    ANALYST'S REPORT:
    {analysis}
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1500,
            system_instruction=(
                "You are a professional research report writer. "
                "Produce well-organized, evidence-based reports. "
                "Never fabricate citations or research findings."
            ),
        ),
    )

    return response.text or "The Writer returned no text."


if __name__ == "__main__":
    print("Report Writer Agent")
    print("Paste the research findings. Enter END on a separate line.")

    research_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        research_lines.append(line)

    print("\nNow paste the analyst's output. Enter END when finished.")

    analysis_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        analysis_lines.append(line)

    research = "\n".join(research_lines).strip()
    analysis = "\n".join(analysis_lines).strip()

    if not research or not analysis:
        print("Both research findings and analysis are required.")
    else:
        try:
            report = write_report(research, analysis)

            with open("research_report.md", "w", encoding="utf-8") as file:
                file.write(report)

            print("\nReport saved to research_report.md")
            print("\n" + report)

        except Exception as error:
            print(f"Report generation failed: {error}")

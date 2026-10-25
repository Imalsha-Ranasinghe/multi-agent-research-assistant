
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


def review_report(report: str) -> str:
    """Review a research report and return a structured verdict."""

    prompt = f"""
    Review this research report critically.

    Check:
    1. Does it follow a clear structure?
    2. Are its claims supported by the supplied material?
    3. Are citations and source URLs preserved?
    4. Does it acknowledge limitations?
    5. Does it avoid unsupported claims?

    Return your response in this exact format:

    VERDICT: APPROVE or REVISE

    FEEDBACK:
    Explain the most important issues. If revision is needed,
    give specific, actionable instructions to improve the report.

    A report with minor stylistic issues may be approved.
    Never claim you independently verified a source unless you did.

    REPORT:
    {report}
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=600,
            system_instruction=(
                "You are a critical research report reviewer. "
                "Be evidence-focused, fair, and specific."
            ),
        ),
    )

    return response.text or "VERDICT: REVISE\nFEEDBACK: No review returned."


if __name__ == "__main__":
    print("Paste the report to review. Enter END on a separate line.")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    report = "\n".join(lines).strip()

    if report:
        try:
            print("\n--- REVIEW ---\n")
            print(review_report(report))
        except Exception as error:
            print(f"Review failed: {error}")
    else:
        print("No report was provided.")

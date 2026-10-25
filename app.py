import streamlit as st
from pathlib import Path
from datetime import datetime

from workflow import workflow

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research Assistant")
st.write(
    "Research a topic using web search, analyze the findings, "
    "generate a report, and review its quality."
)

question = st.text_area(
    "What would you like to research?",
    placeholder="Example: How are AI agents being used in healthcare?",
    height=120,
)

with st.expander("How it works"):
    st.markdown(
        """
        1. **Researcher:** Searches the web for relevant information.
        2. **Analyst:** Evaluates the findings and identifies insights.
        3. **Writer:** Generates a structured report.
        4. **Reviewer:** Checks the report and can request revisions.
        """
    )

if st.button("Generate Research Report", type="primary"):
    if not question.strip():
        st.warning("Please enter a research question.")
    else:
        initial_state = {
            "question": question.strip(),
            "revision_count": 0,
            "review_feedback": "",
            "status": "",
        }

        try:
            with st.spinner(
                "Agents are researching, analyzing, writing, and reviewing..."
            ):
                result = workflow.invoke(initial_state)

            report = result.get("report", "")

            if not report:
                st.error("The workflow finished without producing a report.")
            else:
                output_dir = Path("reports")
                output_dir.mkdir(exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_path = output_dir / f"research_report_{timestamp}.md"

                report_path.write_text(report, encoding="utf-8")

                st.success("Research report generated!")
                st.caption(f"Review status: {result.get('status', 'unknown')}")

                st.markdown(report)

                st.download_button(
                    label="Download report (.md)",
                    data=report,
                    file_name=report_path.name,
                    mime="text/markdown",
                )

                with st.expander("View research findings"):
                    st.text(result.get("research_findings", ""))

                with st.expander("View analyst's evaluation"):
                    st.text(result.get("analysis", ""))

                with st.expander("View reviewer feedback"):
                    st.text(result.get("review_feedback", ""))

        except Exception as error:
            st.error(f"Research workflow failed: {error}")
            st.info(
                "Check your Gemini quota, API configuration, "
                "and Tavily API key before trying again."
            )


from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from researcher import research_topic
from analyst import analyze_research
from writer import write_report
from reviewer import review_report
import re

class ResearchState(TypedDict, total=False):
    question: str
    research_findings: str
    analysis: str
    report: str
    review_feedback: str
    revision_count: int
    status: str


def researcher_node(state: ResearchState) -> dict:
    print("\n[Researcher] Collecting findings...")
    return {
        "research_findings": research_topic(state["question"])
    }


def analyst_node(state: ResearchState) -> dict:
    print("\n[Analyst] Analyzing findings...")
    return {
        "analysis": analyze_research(state["research_findings"])
    }


def writer_node(state: ResearchState) -> dict:
    print("\n[Writer] Creating or revising report...")

    feedback = state.get("review_feedback", "")

    analysis = state["analysis"]

    if feedback:
        analysis += (
            "\n\nREVIEWER FEEDBACK — address these issues:\n"
            + feedback
        )

    report = write_report(
        research_findings=state["research_findings"],
        analysis=analysis,
    )

    return {"report": report}


def parse_review_verdict(review: str) -> str:
    """Accept only an exact APPROVE or REVISE verdict line."""

    match = re.search(
        r"^\s*VERDICT:\s*(APPROVE|REVISE)\s*$",
        review,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    if not match:
        return "REVISE"

    return match.group(1).upper()



def reviewer_node(state: ResearchState) -> dict:
    print("\n[Reviewer] Checking report quality...")

    review = review_report(state["report"])
    verdict = parse_review_verdict(review)

    if verdict == "APPROVE":
        return {
            "review_feedback": review,
            "status": "approved",
        }

    return {
        "review_feedback": review,
        "status": "revise",
        "revision_count": state.get("revision_count", 0) + 1,
    }



def review_decision(state: ResearchState) -> str:
    if state.get("status") == "approved":
        return "finish"

    if state.get("revision_count", 0) >= 2:
        return "finish"

    return "revise"


builder = StateGraph(ResearchState)

builder.add_node("researcher", researcher_node)
builder.add_node("analyst", analyst_node)
builder.add_node("writer", writer_node)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "researcher")
builder.add_edge("researcher", "analyst")
builder.add_edge("analyst", "writer")
builder.add_edge("writer", "reviewer")

builder.add_conditional_edges(
    "reviewer",
    review_decision,
    {
        "finish": END,
        "revise": "writer",
    },
)

workflow = builder.compile()


if __name__ == "__main__":
    print("Multi-Agent Research Workflow")
    print("Graph compiled successfully!\n")
    print(workflow.get_graph().draw_mermaid())

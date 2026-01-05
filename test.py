import os
import json
from typing import TypedDict, Optional, List, Dict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


# ----------------------------
# 1) Define Agent State
# ----------------------------
class RecruiterState(TypedDict):
    first_name: str
    meeting_booked: Optional[bool]
    permission_given: Optional[bool]
    messages: List[Dict[str, str]]
    log: List[str]


# ----------------------------
# 2) Setup DeepInfra LLM (OpenAI-compatible)
# ----------------------------
llm = ChatOpenAI(
    model="openai/gpt-oss-120b",  
    api_key=os.getenv("DEEPINFRA_API_KEY"),
    base_url="https://api.deepinfra.com/v1/openai",
    temperature=0.2
)


# ----------------------------
# 3) Pydantic schema for intent extraction
# ----------------------------
class YesNoIntent(BaseModel):
    answer: Optional[bool]  # true/false/null
    confidence: float
    reasoning: str


def llm_yes_no(user_text: str) -> Optional[bool]:
    """
    Uses LLM to classify yes/no/unclear.
    Returns: True / False / None
    """

    prompt = f"""
You are a classifier. The user responded to a yes/no question.

Return ONLY JSON in this schema:
{{
  "answer": true/false/null,
  "confidence": 0.0-1.0,
  "reasoning": "short explanation"
}}

User response: "{user_text}"
"""

    res = llm.invoke(prompt)
    data = json.loads(res.content)
    parsed = YesNoIntent(**data)

    # Optional: only accept when confidence is high enough
    if parsed.confidence < 0.65:
        return None
    return parsed.answer


# ----------------------------
# 4) Step 1: Welcome + Meeting Question
# ----------------------------
def welcome_and_meeting_question(state: RecruiterState):
    msg = (
        f"Thank you {state['first_name']} for your application via the Linkrsmarokko website. "
        "Have you been able to book a meeting via the website with one of our recruiters?"
    )
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Sent welcome + meeting question")
    return state


# ----------------------------
# 5) Router for meeting answer
# ----------------------------
def meeting_router(state: RecruiterState):
    last_user_msg = state["messages"][-1]["content"]

    answer = llm_yes_no(last_user_msg)

    if answer is None:
        return "meeting_unclear"

    state["meeting_booked"] = answer
    if answer:
        return "permission_question"
    else:
        return "send_booking_link"


# ----------------------------
# 6) Meeting unclear
# ----------------------------
def meeting_unclear(state: RecruiterState):
    msg = "Sorry, I didn’t fully catch that — have you already booked a meeting? (yes/no)"
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Meeting unclear → asked again")
    return state


# ----------------------------
# 7) Send booking link if not booked
# ----------------------------
def send_booking_link(state: RecruiterState):
    booking_link = "https://linkrsmarokko.com/book-meeting"
    msg = (
        "No problem! Please book a meeting using this link:\n"
        f"{booking_link}\n\n"
        "After booking, I’ll ask you a couple of quick questions to prepare for the meeting."
    )
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Meeting not booked → sent link")
    return state


# ----------------------------
# 8) Permission question
# ----------------------------
def permission_question(state: RecruiterState):
    msg = "Is it okay if we ask you a couple of questions to prepare ourselves for the upcoming meeting?"
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked permission")
    return state


# ----------------------------
# 9) Permission router
# ----------------------------
def permission_router(state: RecruiterState):
    last_user_msg = state["messages"][-1]["content"]
    answer = llm_yes_no(last_user_msg)

    if answer is None:
        return "permission_unclear"

    state["permission_given"] = answer
    if answer:
        return "end_success"
    else:
        return "persuasion_then_end"


# ----------------------------
# 10) Permission unclear + persuasion
# ----------------------------
def permission_unclear(state: RecruiterState):
    msg = "Just to confirm — is it okay if we ask you a few questions? (yes/no)"
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Permission unclear → asked again")
    return state


def persuasion_then_end(state: RecruiterState):
    msg = (
        "No worries — these questions help our recruiter prepare and make the meeting more effective. "
        "It takes only about 2 minutes."
    )
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Permission denied → persuasion sent")
    return state


def end_success(state: RecruiterState):
    msg = "Perfect ✅ Thank you! We’ll continue with the first question shortly."
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Permission granted")
    return state


# ----------------------------
# 11) Build LangGraph
# ----------------------------
builder = StateGraph(RecruiterState)

builder.add_node("welcome_and_meeting_question", welcome_and_meeting_question)
builder.add_node("meeting_unclear", meeting_unclear)
builder.add_node("send_booking_link", send_booking_link)
builder.add_node("permission_question", permission_question)
builder.add_node("permission_unclear", permission_unclear)
builder.add_node("persuasion_then_end", persuasion_then_end)
builder.add_node("end_success", end_success)

builder.set_entry_point("welcome_and_meeting_question")

graph = builder.compile()


# ----------------------------
# 12) CLI Runner
# ----------------------------
def run_cli():
    state: RecruiterState = {
        "first_name": "John",
        "meeting_booked": None,
        "permission_given": None,
        "messages": [],
        "log": []
    }

    # Start
    state = graph.invoke(state)
    print("\nAI:", state["messages"][-1]["content"])

    # Meeting step loop
    while state["meeting_booked"] is None:
        user_input = input("\nYou: ")
        state["messages"].append({"role": "user", "content": user_input})

        route = meeting_router(state)
        if route == "meeting_unclear":
            state = meeting_unclear(state)
        elif route == "send_booking_link":
            state = send_booking_link(state)
            state = permission_question(state)
        elif route == "permission_question":
            state = permission_question(state)

        print("\nAI:", state["messages"][-1]["content"])

    # Permission step loop
    while state["permission_given"] is None:
        user_input = input("\nYou: ")
        state["messages"].append({"role": "user", "content": user_input})

        route = permission_router(state)
        if route == "permission_unclear":
            state = permission_unclear(state)
        elif route == "persuasion_then_end":
            state = persuasion_then_end(state)
            break
        elif route == "end_success":
            state = end_success(state)
            break

        print("\nAI:", state["messages"][-1]["content"])

    print("\n✅ FINAL STATE:")
    print(state)

    print("\n✅ LOG:")
    for item in state["log"]:
        print("-", item)


if __name__ == "__main__":
    run_cli()

"""
CLI runner for the Recruiter Assistant.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import RecruiterAssistant
from config.settings import settings


def run_cli():
    """Run the conversational assistant in CLI mode."""
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        return
    
    print("=" * 60)
    print("🤖 Recruiter Assistant CLI")
    print("=" * 60)
    
    # Get user's first name
    first_name = input("\nEnter your first name: ").strip() or "John"
    
    # Initialize assistant
    assistant = RecruiterAssistant(first_name)
    assistant.start()
    
    print(f"\n🤖 AI: {assistant.get_last_message()}")
    
    # Main conversation loop
    while not assistant.is_completed():
        user_input = input("\n👤 You: ").strip()
        
        if not user_input:
            print("⚠️  Please provide a response.")
            continue
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        # Process input and get all new messages
        new_messages = assistant.process_user_input(user_input)
        
        # Display all new assistant messages
        for message in new_messages:
            print(f"\n🤖 AI: {message}")
    
    # Display final results
    state = assistant.get_state()
    collected_data = assistant.get_collected_data()
    
    print("\n" + "=" * 60)
    print("✅ CONVERSATION COMPLETED")
    print("=" * 60)
    
    print(f"\n📊 Collected Information:")
    print(f"  👤 Name: {collected_data['first_name']}")
    print(f"  📅 Meeting Booked: {collected_data['meeting_booked']}")
    print(f"  ✓ Permission Given: {collected_data['permission_given']}")
    print(f"\n  🌍 Location:")
    print(f"     - In Morocco: {collected_data['in_morocco']}")
    if collected_data['current_city']:
        print(f"     - Current City: {collected_data['current_city']}")
    if collected_data['plan_to_move']:
        print(f"     - Plan to Move: {collected_data['plan_to_move']}")
    print(f"     - Preferred Cities: {collected_data['preferred_cities']}")
    
    print(f"\n  💼 Experience:")
    print(f"     - Has Call Center Experience: {collected_data['has_call_center_experience']}")
    if collected_data['experience_details']:
        print(f"     - Experience Details: {collected_data['experience_details']}")
    if collected_data['why_call_center']:
        print(f"     - Why Call Center: {collected_data['why_call_center']}")
    
    print(f"\n  💰 Compensation:")
    print(f"     - Salary Expectation: {collected_data['salary_expectation']}")
    
    print(f"\n  📋 Other:")
    print(f"     - Previous Applications: {collected_data['previous_applications']}")
    
    print(f"\n📝 Conversation Log:")
    for item in state["log"]:
        print(f"  - {item}")
    
    print("\n" + "=" * 60)

    print(state)


if __name__ == "__main__":
    run_cli()
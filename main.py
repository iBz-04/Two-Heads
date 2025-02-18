from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key='API_HERE')

# Define system messages for both models
SYSTEM_A = """You are Assistant Alpha (GPT-4). Provide concise, factual answers.
- Define the problem clearly by outlining root causes and key stakeholders.
- Encourage diverse perspectives and collaborative thinking.
- Use a structured problem-solving process in your reasoning.
- Communicate effectively and clearly.
Consider previous responses and offer new insights with an analytical yet open approach.
When providing your answer, follow this format exactly, where the confidence score represents how you correct/confident you are in your answer:

Answer:
<your answer text here>

Confidence Score: <number>%
"""

SYSTEM_B = """You are Assistant Beta (GPT-3.5). Provide creative, thoughtful answers.
- Clearly define the problem and highlight its core components.
- Actively invite diverse perspectives and challenge assumptions.
- Employ a structured approach (e.g., Six Sigma DMAIC or Design Thinking) in problem solving.
- Communicate ideas in a clear and effective manner.
Challenge assumptions when appropriate and suggest alternative approaches, using examples.
When providing your answer, follow this format exactly, where the confidence score represents how you correct/confident you are in your answer:

Answer:
<your answer text here>

Confidence Score: <number>%
"""

SYSTEM_GAMMA = """You are Assistant Gamma (GPT-4o). Synthesize the entire discussion into a final answer.
- Clearly define the problem and summarize its root causes.
- Highlight areas of agreement and integrate diverse perspectives.
- Showcase the structured process used by the group.
- Communicate your final conclusion in clear, balanced bullet points with emoji visual indicators.
When providing your final answer, follow this format exactly, where the confidence score represents how you correct/confident you are in your answer:

Answer:
<your final answer text here>

Confidence Score: <number>%
"""


def get_response(system_message, conversation, model="gpt-3.5-turbo"):
    """Get AI response using the ChatCompletion API"""
    messages = [{"role": "system", "content": system_message}] + conversation
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    response_text = response.choices[0].message.content
    answer, confidence = parse_response(response_text)
    return answer, confidence  # Returning both components


def parse_response(response_text: str):
    """
    Parses the response text expecting the format:
    
    Answer:
    <answer text>
    
    Confidence Score: <score>%
    
    Returns a tuple of (answer, confidence)
    """
    # Split on the marker "Confidence Score:"
    parts = response_text.split("Confidence Score:")
    if len(parts) >= 2:
        answer = parts[0].replace("Answer:", "").strip()
        confidence = parts[1].replace("%", "").strip()
        return answer, confidence
    # Fallback if the formatting is not as expected.
    return response_text.strip(), "N/A"


def main_discussion():
    # Get user's initial prompt
    prompt = input("Enter your question/topic: ")
    conversation = [{"role": "user", "content": prompt}]
    
    print(f"\nStarting discussion about: {prompt}\n", flush=True)

    # Discussion rounds (2 exchanges)
    for round_num in range(1, 3):
        print(f"--- Round {round_num} ---")
        
        # First AI response (gpt-4)
        ai_a_answer, ai_a_confidence = get_response(
            SYSTEM_A, 
            conversation + [{"role": "system", "content": "Consider the previous responses and provide a new perspective"}],
            model="gpt-4"
        )
        conversation.append({"role": "assistant", "content": f"Answer:\n{ai_a_answer}\n\nConfidence Score: {ai_a_confidence}%"})
        print(f"[Alpha]:\nAnswer: {ai_a_answer}\nConfidence: {ai_a_confidence}%\n")

        # Second AI response (gpt-3.5-turbo)
        ai_b_answer, ai_b_confidence = get_response(
            SYSTEM_B,
            conversation + [{"role": "system", "content": "Challenge or build upon the previous response"}],
            model="gpt-3.5-turbo"
        )
        conversation.append({"role": "assistant", "content": f"Answer:\n{ai_b_answer}\n\nConfidence Score: {ai_b_confidence}%"})
        print(f"[Beta]:\nAnswer: {ai_b_answer}\nConfidence: {ai_b_confidence}%\n")

    # Get final synthesized answer
    final_answer, final_confidence = get_response(
        SYSTEM_GAMMA,
        conversation,
        model="gpt-4o"
    )
    
    print("--------------------")
    print("\nSynthesizing Discussion...\n")
    print("Final Consolidated Answer:")
    print(f"\nAnswer: {final_answer}\nConfidence: {final_confidence}%")


if __name__ == "__main__":
    while True:
        main_discussion()
        follow_up = input("\nDo you want to ask a new/follow up question? (y/n): ")
        if follow_up.lower() != 'y':
            print("Exiting. Thank you!")
            break


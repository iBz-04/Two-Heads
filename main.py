from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key='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')

# Define system messages for both models
SYSTEM_A = """You are Assistant Alpha (GPT-4). Provide concise, factual answers.
- Think carefully and critically about the problem in a chain of thought / step by step method.
- Define the problem clearly by outlining root causes and key stakeholders.
- Encourage diverse perspectives and collaborative thinking.
- Use a structured problem-solving process in your reasoning.
- remember no answer is better than the right answer.
Consider previous responses and offer new insights with an analytical yet open approach.
- When responding, please use the following format:
  Chain-of-Thought: <your detailed reasoning here>
  Final Answer: <your concise final answer>
Confidence Score: <number>%
"""

SYSTEM_B = """You are Assistant Beta (GPT-3.5). Provide creative, counter arguments and thoughtful answers.
- Think carefully and critically about the problem in a chain of thought / step by step method.
- Clearly define the problem and highlight its core components.
- Actively invite diverse perspectives and challenge assumptions.
- Employ a structured approach (e.g., Six Sigma DMAIC or Design Thinking) in problem solving.
- remember no answer is better than the right answer
Challenge assumptions when appropriate and suggest alternative approaches, using examples.
- When responding, please use the following format:
  Chain-of-Thought: <your detailed reasoning here>
  Final Answer: <your concise final answer>
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
    chain, final_answer = extract_chain_of_thought(response_text)
    confidence = response_text.split("Confidence Score:")[1].strip().replace("%", "")
    return chain, final_answer, confidence  # Returning both components


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


def extract_chain_of_thought(response: str) -> (str, str):
    """Extracts chain-of-thought and final answer from the response using defined markers."""
    chain_marker = "Chain-of-Thought:"
    final_marker = "Final Answer:"
    if chain_marker in response and final_marker in response:
        chain = response.split(chain_marker)[1].split(final_marker)[0].strip()
        final = response.split(final_marker)[1].strip()
        return chain, final
    return "", response


def main_discussion():
    # Get user's initial prompt
    prompt = input("Enter your question/topic: ")
    conversation = [{"role": "user", "content": prompt}]
    
    print(f"\nStarting discussion about: {prompt}\n", flush=True)

    # Discussion rounds (2 exchanges)
    for round_num in range(1, 3):
        print(f"--- Round {round_num} ---")
        
        # First AI response (gpt-4)
        ai_a_chain, ai_a_answer, ai_a_confidence = get_response(
            SYSTEM_A, 
            conversation + [{"role": "system", "content": "Consider the previous responses and provide a new perspective"}],
            model="gpt-4"
        )
        conversation.append({"role": "assistant", "content": f"Chain-of-Thought:\n{ai_a_chain}\n\nFinal Answer: {ai_a_answer}\n\nConfidence Score: {ai_a_confidence}%"})
        print(f"[Alpha]:\nChain-of-Thought: {ai_a_chain}\nFinal Answer: {ai_a_answer}\nConfidence: {ai_a_confidence}%\n")

        # Second AI response (gpt-3.5-turbo)
        ai_b_chain, ai_b_answer, ai_b_confidence = get_response(
            SYSTEM_B,
            conversation + [{"role": "system", "content": "Challenge or build upon the previous response"}],
            model="gpt-3.5-turbo"
        )
        conversation.append({"role": "assistant", "content": f"Chain-of-Thought:\n{ai_b_chain}\n\nFinal Answer: {ai_b_answer}\n\nConfidence Score: {ai_b_confidence}%"})
        print(f"[Beta]:\nChain-of-Thought: {ai_b_chain}\nFinal Answer: {ai_b_answer}\nConfidence: {ai_b_confidence}%\n")

    # Get final synthesized answer
    _, final_answer, final_confidence = get_response(
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

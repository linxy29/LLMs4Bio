import pandas as pd
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer

# Function to mock ChatGPT response (since we can't interact with OpenAI API here)
def mock_chatgpt_response(question):
    # Mock responses for demonstration purposes
    mock_responses = {
        "What is the official gene symbol of LMP10?": "PSMB10",
        "What is the official gene symbol of SNAT6?": "SLC38A6",
        # Add more mock responses as needed
    }
    return mock_responses.get(question, "Unknown")

client = OpenAI()
def get_chatgpt_response(question):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message
    except Exception as e:
        return f"Error: {str(e)}"

# Replace 'model_name' with the appropriate model available on Hugging Face
model_name = "facebook/llama"  # Example placeholder, replace with actual model if available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize the pipeline
from transformers import pipeline
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Function to get response from Hugging Face model
def get_huggingface_response(question):
    response = generator(question, max_length=50, num_return_sequences=1)
    return response[0]['generated_text'].strip()



# Read the CSV file
file_path = "/home/linxy29/data/GeneRAG/GeneTurining_partial.csv"  # Change this to your actual file path
df = pd.read_csv(file_path)

# Select rows based on 'Module'
selected_rows = df[df['Module'] == 'Gene alias']

# Initialize a list to store results
results = []

# Iterate over selected rows and get responses
for index, row in selected_rows[:10].iterrows():
    question = row['Question']
    goldstandard = row['Goldstandard']
    # Get ChatGPT response (using mock function here)
    #response = mock_chatgpt_response(question)
    response = get_chatgpt_response(question)
    # Compare with Goldstandard
    is_correct = response == goldstandard
    # Calculate score
    score = 1 if is_correct else 0
    # Store the result
    results.append({
        "Question": question,
        "Goldstandard": goldstandard,
        "Response": response,
        "IsCorrect": is_correct,
        "Score": score
    })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Display the results
print(results_df)


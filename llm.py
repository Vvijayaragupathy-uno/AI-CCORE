# llm.py

from huggingface_hub import InferenceApi

# Hugging Face API setup
API_TOKEN = "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"  # Replace with your Hugging Face API token
MODEL_NAME = "deepseek-ai/DeepSeek-R1"  # Replace with your desired Hugging Face model

# Initialize Hugging Face Inference API
api = InferenceApi(repo_id=MODEL_NAME, token=API_TOKEN)

# Function to get a response from the LLM
def get_llm_response(prompt):
    try:
        # Call the Hugging Face Inference API with the prompt
        response = api(inputs=prompt, raw_response=True)  # Enable raw_response to handle JSON
        
        # Parse the raw response
        if response.status_code == 200:  # Check if the request was successful
            response_json = response.json()
            
            # Extract the generated text from the response
            if isinstance(response_json, list) and len(response_json) > 0:
                return response_json[0]["generated_text"]  # Adjust based on the actual response structure
            else:
                return "No response from the model."
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
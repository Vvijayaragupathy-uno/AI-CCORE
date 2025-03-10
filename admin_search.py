from typing import Generator, Union
from together import Together
import os

DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
API_TOKEN =  DEEPSEEK_API_KEY 
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"  

client = Together(api_key=API_TOKEN)
def get_llm_response(
    prompt: str,
    max_tokens: int = 1500,
    stream: bool = False
):

    try:
    
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            stream=stream,  
        )
        
        if stream: 
            def generate():
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return generate()
        else:
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "No response from the model."
    except Exception as e:
        return f"Error: {str(e)}"
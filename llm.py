from typing import Generator, Union
from together import Together
import os

API_TOKEN =  "4a8e6e227750fba44f0713c1f4c7831548950b0ba3d12533cf670864f6c3901e"  
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"  

client = Together(api_key=API_TOKEN)

def get_llm_response(
    prompt: str,
    max_tokens: int = 500,
    stream: bool = False
) -> Union[str, Generator[str, None, None]]:

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

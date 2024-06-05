

import requests
import json
import re
import asyncio
import edge_tts
import pygame
import os
import time


pygame.init()

# Initialize pygame mixer
pygame.mixer.init()

# Replace with your actual KoboldAI API base URL
base_url = "http://localhost:5001/api/v1"

# Function to send a prompt and receive a response

def delete_text_between_asterisks(text):
    pattern = r'\*(.*?)\*'  # Regular expression pattern to match text between asterisks
    deleted_text = re.sub(pattern, '', text)  # Replace the matched pattern with an empty string
    return deleted_text



def remove_incomplete_sentence(paragraph):
    # Split the paragraph into sentences using regular expressions
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)

    # Check if the last sentence is incomplete or lacks a full stop
    # if sentences and (not sentences[-1] or not sentences[-1][-1] in ['.', '!', '?']):
    #     # Remove the last sentence
    #     sentences.pop()

    # Join the remaining sentences back into a paragraph
    cleaned_par = ' '.join(sentences)
    return cleaned_par


def generate_response(prompt):
     
    global incomp_sen
    endpoint = "/generate"
    url = base_url + endpoint

    headers = {
        "Content-Type": "application/json",
    }
    data = {
        
        "max_context_length": 2048,
        "max_length": 80,
        "rep_pen": 1.15,
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 100,
        "top_a": 0,
        "typical": 1,
        "tfs": 1,
        "rep_pen_range": 2048,
        "rep_pen_slope": 3.4,
        "sampler_order": [6,5,0,2,3,1,4],
        "prompt": prompt + "\nzara:" ,

        "stop_sequence": ["You:", "\nYou "]

    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Check for HTTP errors
        if response.status_code == 200:
            response_data = response.json()
            choices = response_data.get("results")
            if choices:
                generated_text = choices[0].get("text")
                if generated_text:
                          split_text1 = generated_text.split('\n', 1)[0]
                          split_text2 = split_text1.split('\n\n', 1)[0]
                          final_text = delete_text_between_asterisks(split_text2)
                          incomp_sen = remove_incomplete_sentence(final_text)
                
                          
  
                        


            
            else:
                return "Chatbot: Error generating response."
        else:
            return f"Chatbot: API error - {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Chatbot: Request Exception - {e}"






# Chatbot interaction loop
if __name__ == "__main__":
    print("Chatbot: Hello! I'm your friendly chatbot. Type 'exit' to end the conversation.")
    input_prompt = 
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        # Append user input to the conversation prompt
        input_prompt += "You: " + user_input + "\n"

        # Send the updated conversation prompt to KoboldAI API and get response
        sent_to_api = generate_response(input_prompt)

        # Print and play the response using pygame
        
        print("zara:", incomp_sen)

        
        TEXT = incomp_sen
        VOICE = "en-IE-EmilyNeural"
        OUTPUT_FILE = "test.mp3"

        async def amain() -> None:
            """Main function"""
            communicate = edge_tts.Communicate(TEXT, VOICE)
            await communicate.save(OUTPUT_FILE)

        if __name__ == "__main__":
            asyncio.run(amain())

        # Generate a new MP3 file

        # Initialize the mixer and load the newly generated MP3 file
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        # Close the pygame mixer after the music has finished playing
        pygame.mixer.quit()

        # Remove the file after closing the mixer
        # if os.path.exists(OUTPUT_FILE):
        #     try:
        #         os.remove(OUTPUT_FILE)
        #     except Exception as e:
        #         print(f"Error removing file: {e}")
        # else:
        #     print(f"File {OUTPUT_FILE} does not exist.")

        # # Append tiff's response to the conversation prompt
        input_prompt += incomp_sen

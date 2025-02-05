from __future__ import annotations
import os 
from openai import OpenAI
import time 
from time import localtime, strftime
from datetime import datetime as PyDateTime
from models import Video, Summary
import google.generativeai as genai 
import json

WORDS_PER_CHUNK = 50000 #800

class VideoSummarizer:
    PATH = os.getcwd()
    notes_path = PATH + "\\test videos\\output\\notes"
    model_name ="gemini-pro"
    client = genai.GenerativeModel(model_name)
    user_prompt = """
    Please Present this transcript in a more readable manner using lists, bullet points etc.
    Highlight any any actionable advice, references to research, examples, or specific techniques mentioned.
    Please use the exact sentences creator uses in the video. Use the language creator uses in their video. 
    Avoid phrases like "this video summarises", "creator says" just present the information in the video from a third person point of view.  
    Please present the information in the same order as the creator of the video. 
    Do not miss any point or information. 
    Do not leave out information such as definitions, explanations, interesting facts or words that are out of the ordinary, key concepts, main points, and valuable insights presented. 

    Title:
    \"""{title}\"""
    Script:
    \"""{transcript}\"""
    """

    def __init__(self, video: Video):
        self.video = video
        self.api_key = ""

    def start(self):
        self.set_api_key()
        s = self.summarize(self.video)
        return s
    
    def set_api_key(self):
        with open('gemini-api-key.txt', 'r') as f:
            api_key = f.read().strip()
            self.api_key = api_key
            genai.configure(api_key=api_key)
        
    def split_text_by_words(self, text, words_per_chunk):
        words = text.split()
        chunks = [" ".join(words[i:i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)]
        return chunks

    def get_summary(self, video, transcript_part):
        prompt = f"Please summarize the following text:\n\n{transcript_part}\n\nSummary:"
        response = self.client.generate_content(prompt)
        summary = self.set_summary(video, response)
        print(f"Summary-----------------------\n")
        print(summary)
        return summary

    def set_summary(self, video, response):
        summary = ""
        try:
            if hasattr(response, 'text') and response.text is not None:
                summary = response.text
                print(f"Summary for {video.title}: {summary}")
            else:
                finish_reason = getattr(response, 'finish_reason', 'Unknown')
                print(f"No valid summary returned for {video.title}. Reason: {finish_reason}")
                summary = f"No valid summary returned for {video.title}. Reason: {finish_reason}"
        except ValueError as e:
            summary = f"ValueError encountered for {video.title}: {e}"
            print(f"ValueError encountered for {video.title}: {e}")
        except Exception as e:
            summary = f"Unexpected error for {video.title}: {e}"
            print(f"Unexpected error for {video.title}: {e}")
        print(response.usage_metadata)
        return summary 

    def summarize(self, video: Video):
        start_time = time.time()
        print("#######################################")
        prompt = self.user_prompt.format(title=video.title, transcript=video.transcript)
        word, char, token = self.get_text_information(prompt)
        video.transcript_word_count = word # video.prompt_word_count? 
        video.transcript_character_count = char 
        video.transcript_token_count = token
        # TODO: The maximum number of api calls for a minute is 15. So i need to make sure  transcript word count / words_per_chunk < 15 

        if video.transcript_word_count < WORDS_PER_CHUNK:
            response = self.client.generate_content(prompt)
            summary = self.set_summary(video, response)
        else:
            transcript_chunks = self.split_text_by_words(video.transcript, WORDS_PER_CHUNK) # split the transcript into chunks!   
            for chunk in transcript_chunks: 
                print(chunk[:100])
                print("\n")
            video.transcript_chunks = transcript_chunks
            summaries = [self.get_summary(video, chunk) for chunk in transcript_chunks] # get summary of each chunk! 
            final_summary = " ".join(summaries)
            summary = final_summary

        end_time = time.time()
        summary_time = end_time - start_time 
        note_filename = self.notes_path + "\\" + video.title + ".txt" 
        self.save_summary(summary, note_filename)
            
        s = Summary(title=video.title, summary_text=summary)
        s.summary_time = summary_time 
        s.gpt_model_name = self.model_name
        gpt_info = genai.get_model(f"models/{self.model_name}") 
        s.gpt_information = json.dumps(gpt_info.__dict__)
        s.gpt_input_token_count = gpt_info.input_token_limit # not that necessary?
        s.gpt_output_token_count = gpt_info.output_token_limit
        word, char, token = self.get_text_information(summary)
        s.summary_word_count = word 
        s.summary_char_count = char
        s.summary_token_count = token 

        start_time_str = strftime('%Y-%m-%d %H:%M:%S', localtime(start_time))
        s.summary_start_date = PyDateTime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time_str = strftime('%Y-%m-%d %H:%M:%S', localtime(end_time))
        s.summary_end_date = PyDateTime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        s.summary_path = note_filename
        video.summaries.append(s)
        video.is_summarized = True
        video.status = "Done."
        return s

    def get_text_information(self, text):
        word_count = len(text.split())
        char_count = len(text)
        ct = self.client.count_tokens(text)
        token_count = ct.total_tokens
        return word_count, char_count, token_count

    def save_summary(self, summary_text, note_filename):
        with open(note_filename, "w", encoding="utf-8") as file: 
            file.write(summary_text) 

        print(f"Note saved to {note_filename}")

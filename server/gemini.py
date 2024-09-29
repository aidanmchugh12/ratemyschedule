import os
import google.generativeai as genai

genai.configure(api_key='AIzaSyA7zDuJi_5LlvqSsTCzqv-Sj3-Jl1gyixM')
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="You must answer politely")

response = model.generate_content("question")
print(response.text)
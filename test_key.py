import os
try:
    from groq import Groq
except ImportError:
    print("❌ ERROR: Groq library not found. Run: pip install groq")
    exit()

# 1. PASTE YOUR GROQ KEY HERE (starts with gsk_...)
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

print("--- TESTING GROQ CONNECTION ---")

try:
    # 2. SEND A SIMPLE REQUEST
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say 'Groq is ready!'",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    
    print("✅ SUCCESS!")
    print("Response:", chat_completion.choices[0].message.content)

except Exception as e:
    print("❌ FAILED!")
    print(f"Error details: {e}")
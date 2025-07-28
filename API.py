import google.generativeai as genai
genai.configure(api_key="AIzaSyAsdanUxNneTgN2K34CpHXuP5LWtZ3taYM")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Kể truyện ma")
print(response.text)


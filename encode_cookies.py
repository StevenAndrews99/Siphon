import base64

with open("cookies/cookies.txt", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

with open("cookies_b64.txt", "w") as f:
    f.write(encoded)

print("✅ cookies_b64.txt created successfully.")

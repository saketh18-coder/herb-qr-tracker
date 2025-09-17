import pandas as pd
import qrcode
import os
from flask import Flask, render_template_string
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ------------------------
# 1. Select Excel File
# ------------------------
Tk().withdraw()  # hide tkinter window
file_path = askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx")])

if not file_path:
    raise FileNotFoundError("❌ No Excel file selected. Please run again and choose a file.")

df = pd.read_excel(file_path)

# ------------------------
# 2. Flask App Setup
# ------------------------
app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Herb Journey</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 20px;">
    <h2>🌿 Herb Journey for Batch {{ batch_id }}</h2>
    <ul>
        <li><b>Herb:</b> {{ herb_name }}</li>
        <li><b>Farm Location:</b> {{ farm_location }}</li>
        <li><b>Harvest Stage:</b> {{ harvest }}</li>
        <li><b>Purity:</b> {{ purity }}</li>
        <li><b>Certified:</b> {{ certified }}</li>
        <li><b>Notes:</b> {{ notes }}</li>
    </ul>
    <p><i>Data updated from Excel.</i></p>
</body>
</html>
"""

# ------------------------
# 3. Route to show batch journey
# ------------------------
@app.route("/batch/<batch_id>")
def show_batch(batch_id):
    row = df[df["batch_id"] == batch_id]
    if row.empty:
        return f"<h2>No data found for batch {batch_id}</h2>"

    record = row.iloc[0].to_dict()
    return render_template_string(HTML_TEMPLATE, **record)

# ------------------------
# 4. Generate QR codes
# ------------------------
def generate_qr_codes():
    os.makedirs("qrcodes", exist_ok=True)
    for batch_id in df["batch_id"]:
        url = f"http://127.0.0.1:5000/batch/{batch_id}"
        qr = qrcode.make(url)
        qr.save(f"qrcodes/{batch_id}.png")
    print("✅ QR Codes generated in 'qrcodes' folder.")

if __name__ == "__main__":
    generate_qr_codes()
    print("🚀 Starting Flask server... Open http://127.0.0.1:5000/batch/B001")
    app.run(debug=True)

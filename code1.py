import pandas as pd

# Load your existing Excel file (replace with your file path)
df = pd.read_excel("herb_batches.xlsx")

# Suppose you have uploaded herb images to Google Drive
# and prepared a dictionary that maps herb_name -> Google Drive FILE_ID
# Example (replace with your own FILE_IDs):
image_links = {
    "ashwagandha": "1x2y3zAshwagandhaID",
    "brahmi": "1a2b3cBrahmiID",
    "turmeric": "1t2u3rTurmericID",
    "neem": "1n2e3eNeemID",
    "tulsi": "1t2u3lTulsiID",
    # add all other herbs...
}

# Generate clickable links
def make_hyperlink(herb):
    if herb in image_links:
        file_id = image_links[herb]
        url = f"https://drive.google.com/uc?id={file_id}"
        return f'=HYPERLINK("{url}", "View Image")'
    else:
        return ""

# Add new column
df["image_url"] = df["herb_name"].apply(make_hyperlink)

# Save back to Excel (with formulas preserved)
output_file = "herb_batches_with_clickable_images.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"✅ Excel file created: {output_file}")

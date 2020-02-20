import os

def fix_house_text(text):
    return fix_both_text(text)

def fix_senate_text(text):
    return fix_both_text(text)

def fix_both_text(text):
    return text.replace("™™",'"' ).replace("™","'").replace("Š", "–").replace("‚‚", '"').replace("‚", "'").replace("Œ", " to ").replace("\n", "")
    


directory = r'transcripts-txt/'
for filename in os.listdir(directory):
    text = ""
    with open(f"transcripts-txt/{filename}") as file:
        text = file.read()
    if "house" in filename:
        pass
        open(f"transcripts-txt/{filename}","w").write(fix_house_text(text))
    else:
        open(f"transcripts-txt/{filename}","w").write(fix_senate_text(text))
    print(f"Fixed {filename}.")


pip install -r requirements.txt
mkdir transcripts-pdf
mkdir transcripts-txt
python DownloadTranscripts.py && python ConvertToText.py && python FixCharacters.py && python UnhypenizeWords.py
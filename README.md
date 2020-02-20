# US-Congress-Corpora-Builder
A set of Python tools to download the Senate and House transcripts and convert them to usable text.

# Usage
```bash
sh setup.sh
sh build-corpera.sh
```
The text transcripts will be in transcripts-txt/ and will be named by chamber of congress and date.
# Roadmap

 - [x] Downloading PDFs by date range
 - [x] Converting them into usable text
 - [ ] Seperating the text by speaker and eliminating non-spoken text (See SeperateSpeeches.py)

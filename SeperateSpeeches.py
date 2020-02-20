import os
import re
import textwrap

US_STATES = "(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming)"

MEMBER_NAME = f"M[rs]{{1,2}}\\.( Manager| Counsel)? (?!Speaker)[A-Z'-´]*?(( [A-Z]+)?( [A-Z]\\.)? [A-Z]*?)?(( )?of {US_STATES}( )?)?"

START_REGEXES = [
    "The Acting CHAIR( \\(during the vote\\))?",
    "The VICE PRESIDENT",
    "The SPEAKER( pro tempore)?( \\(during the vote\\))?",
    "The PRESIDING OFFICER",
    "The CHIEF JUSTICE",
    "The CHAIR",
    "The SPEAKER",
    "The ACTING PRESIDENT( pro tem(-)?pore)?",
    "Secretary General",
    MEMBER_NAME
]

SPEECH_START = re.compile(f"[^a-z,:] ({ '|'.join(START_REGEXES)})( \\({MEMBER_NAME}\\))?(?=\.)", re.MULTILINE)

print(f"[^a-z,:] ({ '|'.join(START_REGEXES)})( \\({MEMBER_NAME}\\))?(?=\.)")

MIDDLE_REGEXES = [
    "\\(Text of (v|V)ideotape presentation(:|\\.)\\)",
    "\\[Text of Videotape presentation:\\]",
    "\\(Videotape presentation\\.\\)"
]

SPEECH_MIDDLE=re.compile("|".join(MIDDLE_REGEXES))

END_REGEXES = [
    "(?<=(\\.| ))f ",
    "The ((senior )?assistant )?(|legislative |bill )(c|C)lerk (?!will)",
    "(The|M[rs]\\.)[A-Za-z ]*led the Pledge of Allegiance as follows",
    "[A-Z ']*INTHEHOUSEOFREPRESENTATIVES",
    "There (being|was) no objection",
    "Thereupon, the Senate proceeded",
    "Thereupon, the committee was",
    "The result was announced",
    "The vote was taken",
    "The yeas and nays resulted",
    "b[0-9]{4}",
    "PERSONAL( )?EXPLANATION",
    "MOTIONTORECOMMIT",
    "GENERALLEAVE",
    "OFFICEOFTHEPRESSSECRETARY",
    f"([A-Z ]*)?\\({MEMBER_NAME} asked and was given permission to",
    "[A-Z0-9 \\.]{10,}$",
    "h FOREIGN TRAVEL FINANCIAL REPORTS",
    "EXPLANATORYSTATEMENTTOACCOMPANY",
    "\\(The remarks of ",
    "UNANIMOUSCONSENTREQUEST",
    "RECESS",
    "(?<=I yield back\\.)",
    "(?<=reserve the balance of my time\\.)",
    "Thereupon, the Senate,",
    "There being no objection, the Senate",
    "\\(Applause, (the )?(Members|Senators) rising\\.\\)$",
    " The ( concurrent)?(amendment|motion) was agreed to",
    "S\\.J\\. RES\\. [0-9]{1,4}",
    "AMENDMENTNO\\. [0-9]{1,4}",
    "The bill\\(S\\. [0-9]{1,4}",
    "H\\.R\\. [0-9]{1-4}",
    "\\(The resolution, with its preamble, is printed in today's",
    "\\(For conference report and statement,",
    "The nomination was confirmed",
    "\\(For veto message",
    "\\(For text of the report",
    "The material previously referred to",
    "\\(The amendment is printed",
    "The amendment(\\(No\\. [0-9]{1-3}\\))?(, as modified,)? was",
    "Accordingly \\(at (1)?[0-9] o'clock and ([1-5])?([0-9])? minutes (a|p).m. \\)",
    "The question was taken",
    "The text of the amendment is as follows",
    "The nominations were confirmed",
    "The yeas and nays were ordered\\.",
    f"By {MEMBER_NAME} \\(for (him|her)self",
    "The committee-reported amendments",
    "\\(The foregoing tally has been changed to reflect the above order\\.\\)",
    f"\\({MEMBER_NAME} assumed the Chair\\.\\)",
    f"\\(At the request of {MEMBER_NAME}, ",
    "\\(Applause\\.\\)$",
    "The (concurrent )?resolution \\((H|S)\\.( Con\\.)? Res\\. [0-9]{1,4}\\) was agreed to\\.",
    "The (concurrent )?resolutions \\((H|S)\\.( Con\\.)? Res\\. [0-9]{1,4} and (H|S)\\.( Con\\.)? Res\\. [0-9]{1,4}\\) were agreed to\\.",
    "\\(English translation of the statement",
    "\\(Disturbance in the( Visitors') Galleries\\.\\)$",
    "((?<=(\\. |\\.\"|[a-z]\\.))([A-Z 0-9,;&'\"\\.–-]| to ){3,}($|HON\\.| The))",
    "(?<=RECORD).*[A-Z ]{10}",
    "The Assistant to the Sergeant at Arms announced ",
]

SPEECH_END=re.compile("|".join(END_REGEXES))

print(MEMBER_NAME)

def print_speech(speech):
    if len(speech) > 3*160:
        print(textwrap.fill(speech[2:3*80],80))
        print("...")
        print(textwrap.fill(speech[len(speech)-3*80:],80))
        
    else:
        print(textwrap.fill(speech[2:],80))
    print("======================================================")

def convert_to_speeches(text):
    matches = list(re.finditer(SPEECH_START, text))
    try:
        for i in range(len(matches)):
            last_index = len(matches) - 1

            if i < len(matches)-1:
                last_index = matches[i + 1].start(0) + 2

            speaker = matches[i].group(0)[2:]
            speech = text[matches[i].end(0):last_index]
            if re.search(SPEECH_MIDDLE, speech):
                print(speaker)
                i += 1
                last_index = len(text) - 1
                if i < len(matches)-1:
                    last_index = matches[i + 1].start(0) + 2
                temp_speaker = matches[i].group(0)[2:]
                temp_speech = text[matches[i].end(0):last_index]
                while i < len(matches) - 1:
                    if temp_speaker == speaker:
                        break
                    try:
                        last_index = list(re.finditer(SPEECH_END, speech))[0].start(0)
                        speech = speech[: last_index]
                        break
                    except:
                        pass
                    speech += temp_speech
                    i += 1
                    last_index = len(text) - 1
                    if i < len(matches)-1:
                        last_index = matches[i + 1].start(0) + 2
                    temp_speaker = matches[i].group(0)[2:]
                    temp_speech = text[matches[i].end(0):last_index]

            speech = speech.rstrip()
            speech +="\n"
            last_index = len(speech) - 1
            try:
                last_index = list(re.finditer(SPEECH_END, speech))[0].start(0)
            except:
                pass
            speech = speech[: last_index]
            yield speaker, speech
    except Exception as e:
        pass

def main():
    directory = r'transcripts-txt/'
    for filename in os.listdir(directory):
        text = ""
        with open(f"transcripts-txt/{filename}", "r") as file:
            text = file.read()
            for speaker, speech in convert_to_speeches(text):
                text+=speech
        with open(f"{filename}", "w") as file:
            file.write(text)

if __name__ == "__main__":
    main()
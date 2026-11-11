import re
from pathlib import Path

# re is Python's regex module — it lets you search text for patterns instead of exact strings (e.g. "any two digits, a dot, any two digits" instead of literally typing every timestamp). 
# Path is the modern way to point at a file and read/write it.


FILLER_PATTERN = re.compile(r"\(\s*(?:eeh|uuh|uhm)\s*\)", re.IGNORECASE)
UTTERANCE_PATTERN = re.compile(r"(.*?)\[(\d{2}\.\d{2})\]\s*([.!?]?)", re.DOTALL)

# re.compile pre-builds a pattern so you can reuse it instead of re-parsing the regex string every time. Breaking down FILLER_PATTERN: \( and \) match a literal ( and ) (escaped because parentheses are special in regex). \s* means "zero or more spaces." (?:eeh|uuh|uhm) is a non-capturing group meaning "one of these three words." So the whole thing matches (eeh), ( uhm ), (UUH), etc. — anything filler-shaped, case-insensitive.
# UTTERANCE_PATTERN is the one doing the heavy lifting. (.*?) is a capturing group — parentheses in regex (unlike in your transcript text) mean "remember this chunk of matched text so I can grab it later." The ? makes it non-greedy, meaning "match as little as possible" — without it, it would gobble up text all the way to the last timestamp in the whole transcript instead of stopping at the next one. \[(\d{2}\.\d{2})\] matches a 
# literal [, then two digits, a literal dot, two digits, a literal ] — that's your [00.10] shape — and captures the digits part too. re.DOTALL tells . to also match newline characters, which matters because your utterances span multiple physical lines in the raw file.


def clean_utterance(text:str) -> str:
    text = FILLER_PATTERN.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# This is a function — a reusable block that takes text in and returns a cleaned version out. text.lstrip(" .") strips any leading spaces or periods. 
# This exists because of a genuinely tricky bug your data has: your periods often land after the timestamp bracket (newspaper [01.05] . He-he looks serious), so when the script grabs "everything before the next bracket," it picks up that orphaned . from the previous sentence as debris at the front. Without this line you'd get . He-he looks serious with a stray leading period — I actually ran the regex without this fix first and saw exactly that, which is why it's here.
# FILLER_PATTERN.sub("", text) means "find every match of the filler pattern and replace it with an empty string" — this is what deletes (eeh), (uuh), (uhm) wherever they show up. It does not touch anything with a hyphen, so I-I, s-sad, grum-grumpy sail through untouched — that's your struggle/repair markers preserved on purpose.
# re.sub(r"\s+", " ", text) collapses any run of multiple spaces (left behind after deleting a filler) down to one space. \s+ means "one or more whitespace characters."
# strip() trims any leading/trailing whitespace left over, and returns it.


# turn everything into a clean file

def rescontructure_transcript(raw_text: str) -> list[str]:
    joined = raw_text.replace("\n", "")
    lines = []
    for raw_utterance, timestamp, end_punct in UTTERANCE_PATTERN.findall(joined):
        cleaned = clean_utterance(raw_utterance)
        if cleaned:
            end_punct = end_punct or "."
            lines.append(f"[{timestamp}] {cleaned}{end_punct}")

    return lines


# reading the file

def main():
   raw_path = Path(__file__).resolve().parent / "transcript.txt"
   clean_path = Path(__file__).resolve().parent / "clean_transcript.txt"

   raw_text = raw_path.read_text(encoding ="utf-8")
   cleaned_lines = rescontructure_transcript(raw_text)

   clean_path.write_text("\n".join(cleaned_lines), encoding="utf-8")
   print(f"Wrote {len(cleaned_lines)} utterances to {clean_path}")

if __name__== "__main__":
   main()





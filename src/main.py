import os
import shutil
from concurrent.futures import ThreadPoolExecutor

MD_DIR = "../md"
OUT_DIR = "../out"
STATIC_DIR = "../static"


def clean():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)


def copy_assets():
    shutil.copytree(STATIC_DIR, OUT_DIR)


def md_html(file):
    if file.endswith(".md"):
        input_file = os.path.join(MD_DIR, file)
        md_out_file = os.path.join(OUT_DIR, file)
        filename_base = os.path.splitext(file)[0]
        output_file = os.path.join(OUT_DIR, filename_base+ ".html")
        os.system(
            f"npx -p @mermaid-js/mermaid-cli mmdc -i {input_file} -o {md_out_file} --cssFile mermaid.css  --outputFormat=svg -t dark -b transparent"
        )
        os.system(
            f"pandoc {md_out_file} -o {output_file} --mathjax --template template.html --no-highlight --filter pandoc-sidenote --variable=filename_base:{filename_base}"
        )
        os.remove(md_out_file)


# def md_mp3(file):
from google.cloud import texttospeech


import undown
def md_mp3(
    file,
    voice="en-GB-Wavenet-B",
    gender="MALE",
    lang="en-GB",
    speed=1.0,
    pitch=1.0,
):
    if file.endswith(".md"):
    
        with open(os.path.join(MD_DIR,file), "r") as f:
            text = undown.md_to_text(f.read())
        file_path = os.path.join(OUT_DIR, os.path.splitext(file)[0] + ".mp3")

        if gender == "MALE":
            gender = 1
        elif gender == "FEMALE":
            gender = 2
        elif gender == "NEUTRAL":
            gender = 3
    
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()
    
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)
    
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang, ssml_gender=gender, name=voice
        )
    
        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speed, pitch=pitch
        )
    
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
    
        # The response's audio_content is binary.
        with open(file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{file_path}"')

def main():
    md_files = os.listdir(MD_DIR)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(md_html, md_files)
    for file in md_files:
        md_mp3(file) 



if __name__ == "__main__":
    clean()
    copy_assets()
    main()

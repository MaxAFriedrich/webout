import os
import shutil
from concurrent.futures import ThreadPoolExecutor

from pyrun import eval_and_replace_markdown_code_blocks as py_md

MD_DIR = "../md"
OUT_DIR = "../out"
STATIC_DIR = "../static"


def clean():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)


def copy_assets():
    shutil.copytree(STATIC_DIR, OUT_DIR)
    # Get the list of files in the source folder
    src_static = "./static"
    files = os.listdir(src_static)
    # Loop through the files and copy them to the destination folder
    for file in files:
        src_file = os.path.join(src_static, file)
        dst_file = os.path.join(OUT_DIR, file)
        shutil.copy(src_file, dst_file)


def md_html(file):
    if file.endswith(".md"):
        input_file = os.path.join(MD_DIR, file)
        md_out_file = os.path.join(OUT_DIR, file)
        filename_base = os.path.splitext(file)[0]
        output_file = os.path.join(OUT_DIR, filename_base + ".html")
        py_md(input_file, md_out_file)
        os.system(
            f"npx -p @mermaid-js/mermaid-cli mmdc -i {md_out_file} -o {md_out_file} --cssFile mermaid.css  --outputFormat=svg -t dark -b transparent"
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

        with open(os.path.join(MD_DIR, file), "r") as f:
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
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=pitch,
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


def get_dir(dir_path):
    files = []
    dirs = []
    for root, _, filenames in os.walk(dir_path):
        # Remove dir_path from the root path
        root = os.path.relpath(root, dir_path)
        dirs.append(root)
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return (files, dirs)


def make_dirs(dir_path):
    _, dirs = get_dir(dir_path)
    for dir_name in dirs:
        new_path = os.path.join(OUT_DIR, dir_name)
        os.makedirs(new_path, exist_ok=True)


def main(sound=True):
    md_files, _ = get_dir(MD_DIR) 
    make_dirs(MD_DIR)
    print(md_files)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(md_html, md_files)
    if sound:
        for file in md_files:
            md_mp3(file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-S", "--no-sound", help="Turn off sound", action="store_false")
    args = parser.parse_args()
    clean()
    copy_assets()
    main(sound=args.no_sound)

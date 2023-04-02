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


def process_file(file):
    if file.endswith(".md"):
        print(file)
        input_file = os.path.join(MD_DIR,file)
        md_out_file = os.path.join(OUT_DIR,file)
        output_file = os.path.join(OUT_DIR,os.path.splitext(file)[0]+".html")
        os.system(f"npx -p @mermaid-js/mermaid-cli mmdc -i {input_file} -o {md_out_file} --cssFile mermaid.css  --outputFormat=svg -t dark -b transparent")
        os.system(f"pandoc {md_out_file} -o {output_file} --mathjax --template template.html --no-highlight --filter pandoc-sidenote")
        os.remove(md_out_file)


def md_html():
    md_files = os.listdir(MD_DIR)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_file, md_files)


if __name__ == "__main__":
    clean()
    copy_assets()
    md_html()


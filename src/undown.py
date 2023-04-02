import re


def md_to_text(md):
    output = md

    output = re.sub(r"`[\s\S]*?`", "", output)  # Fenced codeblocks
    output = re.sub(r"^---[\S\s]*?---", "", output)  # Remove frontmatter
    # Remove horizontal rules (stripListHeaders conflict with this rule, which is why it has been moved to the top)
    output = re.sub(r"^(-\s*?|\*\s*?|_\s*?){3,}\s*", "", output, flags=re.MULTILINE)

    output = re.sub(r"^- \[ \] ", "", output, flags=re.MULTILINE)  # Remove todo lists
    output = re.sub(r"^- \[x\] ", "", output, flags=re.MULTILINE)  # Remove todo lists
    output = re.sub(r"^([\s\t]*)([\*\-\+]|\d+\.)\s+", "", output, flags=re.MULTILINE)
    output = re.sub(r"\n={2,}\n", "\n", output)  # Remove atx-style headers
    output = re.sub(r"~~", "", output)  # Strikethrough
    output = re.sub(r"\*\[.*\]:.*\n", "", output)  # Remove abbreviations
    htmlReplaceRegex = re.compile("<[^>]*>", flags=re.IGNORECASE)
    output = re.sub(
        r"^\|[^\|]+?\|.*?$", "", output, flags=re.MULTILINE
    )  # Remove tables
    output = re.sub(r"\$\$.+?\$\$", "", output, flags=re.MULTILINE)  # Remove math
    output = re.sub(htmlReplaceRegex, "", output)  # Remove HTML tags
    output = re.sub(
        r"^[=\-]{2,}\s*$", "", output, flags=re.MULTILINE
    )  # Remove setext-style headers
    output = re.sub(
        r"\s{0,2}\[.*?\]: .*?$", "", output, flags=re.MULTILINE
    )  # Remove footnotes?
    output = re.sub(r"\[\^.+?\](\: .*?$)?", "", output)  # Remove footnotes
    output = re.sub(
        r"\!\[(.*?)\][\[\(].*?[\]\)]",
        "",
        output,
    )  # Remove images
    output = re.sub(
        r"\[([^\]]*?)\][\[\(].*?[\]\)]",
        "",
        output,
    )  # Remove inline links
    output = re.sub(
        r"^\s{0,3}>\s?", "", output, flags=re.MULTILINE
    )  # Remove blockquotes
    output = re.sub(
        r"^(\n)?\s{0,}#{1,6}\s+| {0,}(\n)?\s{0,}#{0,} #{0,}(\n)?\s{0,}$",
        "",
        output,
        flags=re.MULTILINE,
    )  # Remove atx-style headers
    output = re.sub(r"([\*]+)(\S)(.*?\S)??\1", r"\2\3", output)  # Remove * emphasis
    output = re.sub(
        r"(^|\W)([_]+)(\S)(.*?\S)??\2($|\W)", r"\1\3\4\5", output
    )  # Remove _ emphasis. Unlike *, _ emphasis gets rendered only if
    #   1. Either there is a whitespace character before opening _ and after closing _.
    #   2. Or _ is at the start/end of the string.

    output = re.sub(r"`(.+?)`", r"\1", output)  # Remove inline code
    output = re.sub(r"~(.*?)~", r"\1", output)  # Replace strike through
    output = re.sub(r"==(.*?)==", r"\1", output)  # Replace highlights through
    return output




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert markdown to text")
    parser.add_argument("input", type=str, help="Input file")
    parser.add_argument("output", type=str, help="Output file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        txt = md_to_text(f.read())

    # save_text_to_speech(txt, args.output)

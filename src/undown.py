import re


def md_to_text(md, options=None):
        if not options:
            options = {}
        options['listUnicodeChar'] = options.get('listUnicodeChar', False)
        options['stripListLeaders'] = options.get('stripListLeaders', True)
        options['gfm'] = options.get('gfm', True)
        options['useImgAltText'] = options.get('useImgAltText', True)
        options['abbr'] = options.get('abbr', True)
        options['replaceLinksWithURL'] = options.get('replaceLinksWithURL', False)
        options['todo'] = options.get('todo', True)
        options['htmlTagsToSkip'] = options.get('htmlTagsToSkip', [])
    
        output = md or ''
    
        # Remove horizontal rules (stripListHeaders conflict with this rule, which is why it has been moved to the top)
        output = re.sub(r'^(-\s*?|\*\s*?|_\s*?){3,}\s*', '', output, flags=re.MULTILINE)
    
   
        if options['todo']:
            output = re.sub(r'^\s*\[.\]\s+', '', output, flags=re.MULTILINE)  # Remove todo lists
            output = re.sub(r'^\s*\[\s\]\s+', '', output, flags=re.MULTILINE)  # Remove todo lists
        if options['stripListLeaders']:
            if options['listUnicodeChar']:
                output = re.sub(r'^([\s\t]*)([\*\-\+]|\d+\.)\s+', options['listUnicodeChar'] + ' ', output, flags=re.MULTILINE)
            else:
                output = re.sub(r'^([\s\t]*)([\*\-\+]|\d+\.)\s+', r'\1', output, flags=re.MULTILINE)
        if options['gfm']:
            output = re.sub(r'^---[\S\s]*---', '', output)  # Remove frontmatter
            output = re.sub(r'\n={2,}\n', '\n', output)  # Remove atx-style headers
            output = re.sub(r'~{3}.*\n', '', output)  # Fenced codeblocks
            output = re.sub(r'~~', '', output)  # Strikethrough
            output = re.sub(r'`{3}.*\n', '', output)  # Fenced codeblocks
        if options['abbr']:
            output = re.sub(r'\*\[.*\]:.*\n', '', output)  # Remove abbreviations

        htmlReplaceRegex = re.compile('<[^>]*>', flags=re.IGNORECASE)
        if options['htmlTagsToSkip']:
            joinedHtmlTagsToSkip = '(?!' + '|'.join(options['htmlTagsToSkip']) + ')'
            htmlReplaceRegex = re.compile('<' + joinedHtmlTagsToSkip + '[^>]*>', flags=re.IGNORECASE)
        output = re.sub(r'^\|[^\|]+?\|.*?$', '', output, flags=re.MULTILINE)  # Remove tables
        output = re.sub(r'\$\$.+?\$\$', '', output, flags=re.MULTILINE)  # Remove math 
        output = re.sub(htmlReplaceRegex, '', output)  # Remove HTML tags
        output = re.sub(r'^[=\-]{2,}\s*$', '', output, flags=re.MULTILINE)  # Remove setext-style headers
        output = re.sub(r'\s{0,2}\[.*?\]: .*?$', '', output, flags=re.MULTILINE)  # Remove footnotes?
        output = re.sub(r'\[\^.+?\](\: .*?$)?', '', output)  # Remove footnotes
        output = re.sub(r'\n\n^```.*?\n.*?\n```', '', output, flags=re.MULTILINE)  # Remove code blocks
        output = re.sub(r'\!\[(.*?)\][\[\(].*?[\]\)]', lambda match: match.group(1) if options['useImgAltText'] else '', output)  # Remove images
        output = re.sub(r'\[([^\]]*?)\][\[\(].*?[\]\)]', lambda match: match.group(2) if options['replaceLinksWithURL'] else match.group(1), output)  # Remove inline links
        output = re.sub(r'^\s{0,3}>\s?', '', output, flags=re.MULTILINE)  # Remove blockquotes
        output = re.sub(r'^(\n)?\s{0,}#{1,6}\s+| {0,}(\n)?\s{0,}#{0,} #{0,}(\n)?\s{0,}$', lambda match: f"{match.group(1)}{match.group(2)}{match.group(3)}", output, flags=re.MULTILINE)  # Remove atx-style headers
        output = re.sub(r'([\*]+)(\S)(.*?\S)??\1', r'\2\3', output)  # Remove * emphasis
        output = re.sub(r'(^|\W)([_]+)(\S)(.*?\S)??\2($|\W)', r'\1\3\4\5', output)  # Remove _ emphasis. Unlike *, _ emphasis gets rendered only if 
        #   1. Either there is a whitespace character before opening _ and after closing _.
        #   2. Or _ is at the start/end of the string.
        output = re.sub(r'(`{3,})(.*?)\1', r'\2', output, flags=re.DOTALL)  # Remove code blocks
        output = re.sub(r'`(.+?)`', r'\1', output)  # Remove inline code
        output = re.sub(r'~(.*?)~', r'\1', output)  # Replace strike through 

        return output

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert markdown to text')
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('output', type=str, help='Output file')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        txt = md_to_text(f.read())

    with open(args.output, 'w') as f:
        f.write(txt)

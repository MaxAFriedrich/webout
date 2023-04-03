import io
import sys
import re

def eval_and_replace_markdown_code_blocks(file_path, output_path, is_pdf=False):
    # Read the file contents
    with open(file_path, 'r') as f:
        file_contents = f.read()

    # Find all code blocks delimited by ```py ... ```
    code_blocks = re.findall(r'```py\s+(.*?)```', file_contents, re.DOTALL)
    # Create an in-memory buffer for stdout and stderr
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    # Redirect stdout and stderr to the in-memory buffers
    sys.stdout = stdout_buf
    sys.stderr = stderr_buf

    # Replace each code block with its captured output
    for _, code_block in enumerate(code_blocks):
        try:
            exec(code_block)
        except Exception as e:
            # Print any exception messages to stderr
            print(e, file=sys.stderr)

        # Get the captured output as a string
        output_str = stdout_buf.getvalue() + stderr_buf.getvalue()

        # Replace the code block with the captured output in the file contents
        file_contents = file_contents.replace(f'```py\n{code_block}```', output_str, 1)

        # Reset the in-memory buffers for the next code block
        stdout_buf.truncate(0)
        stderr_buf.truncate(0)

    # Restore stdout and stderr to their original values
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    with open(output_path,"w") as f:
        f.write(file_contents)

if __name__ == '__main__':
    import os
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            out = sys.argv[2]
        except IndexError:
            out="/dev/stdout"
        eval_and_replace_markdown_code_blocks(os.path.join("../md",filename),out)
    else:
        print("Please provide a filename as argument")


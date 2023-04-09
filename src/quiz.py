import re
from random import randint

import htmlmin
import jsmin


class Quiz:
    def __init__(self):
        self.html = ""
        self.js = ""

    def code(self):
        # Minify HTML
        minified_html = htmlmin.minify(
            self.html, remove_comments=True, remove_empty_space=True
        )

        # Minify JS
        minified_js = jsmin.jsmin(self.js)

        return f"{minified_html}<script>{minified_js}</script>"

    def gaps(self, text):
        uuid = str(randint(1, 1000000))
        gaps = re.findall(r"(?<!\\){(.*?)(?<!\\)}", text)
        for i, gap in enumerate(gaps):
            text = text.replace(
                "{" + gap + "}",
                f'<input oninput="checkAnswers{uuid}()" style="width:{len(gap)}ch;" type="text" id="gap{i+1}_{uuid}" name="gap{i+1}_{uuid}" value="">',
                1,
            )
        self.html += f"<p>{text}</p>"
        self.js += (
            """
        function checkAnswers"""
            + uuid
            + """() {
            """
        )
        for i, gap in enumerate(gaps):
            self.js += f"""
            let gap{i+1} = document.getElementById("gap{i+1}_{uuid}");
            if (gap{i+1}.value.toLowerCase() === "{gap}".toLowerCase()) {{
                gap{i+1}.style.borderColor = "#181"
            }}else{{
                gap{i+1}.style.borderColor = ""
                }}
            """
        self.js += "}"

    def open(self, text, answer):
        uuid = str(randint(1, 1000000))
        self.html += f"<p>{text}</p>"
        self.html += f'<textarea oninput="checkAnswer{uuid}()"  id="{uuid}_answer" name="answer"></textarea>'
        self.js += f"""
        function checkAnswer{uuid}() {{
            let answer = document.getElementById("{uuid}_answer");
            """

        self.js += f"""
            if (answer.value.toLowerCase() === "{answer}".toLowerCase()) {{
                answer.style.borderColor = "#181"
            }} else {{
                answer.style.borderColor = ""
            }}
        }}
        """

    def choice(self, text, choices, answer):
        uuid = str(randint(1, 1000000))
        self.html += f"<p>{text}</p>"
        self.html += f"<p class='radioCorrect' style='display:none; color:#181; font-size:3rem;' id='correct{uuid}'>✔</p>"
        for i, choice in enumerate(choices):
            self.html += f"""
            <label for="choice{i+1}_{uuid}">
            <input onclick="checkAnswer{uuid}()" type="radio" id="choice{i+1}_{uuid}" name="choice{uuid}" value="{choice}">
            {choice}</label>
            <br>
            """
        self.js += f"""function checkAnswer{uuid}() {{
            let radios = document.getElementsByName("choice{uuid}");
            let selected = "";
            for (let i = 0; i < radios.length; i++) {{
                if (radios[i].checked) {{
                    selected = radios[i].value;
                    break;
                }}
            }}
            """
        self.js += f"""
            if (selected === "{choices[answer-1]}") {{
                document.getElementById("correct{uuid}").style.display="block";
            }} else {{
                document.getElementById("correct{uuid}").style.display="none";
            }}
        }}
        """

    def match(self, text: str):
        uuid = str(randint(1, 1000000))
        answers = ""
        questions = ""
        gaps = re.findall(r"(?<!\\){(.*?)(?<!\\)}", text)
        text_list = re.split(r"(?<!\\){.*?(?<!\\)}", text)
        for i in range(len(text_list) - 1):
            questions += f'{text_list[i]}<div class="droptarget" data-correct="{uuid}_{i}"></div>'
            answers += f'<p draggable="true" class="dragtarget" id="dragtarget" data-correct="{uuid}_{i}">{gaps[i]}</p>'
        self.html += f'<div id="DnDWrapper"><div class="container" data-correct="">{answers}</div><div class="questions"><div class="question">{questions}</div></div></div></div>'

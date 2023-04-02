clean:
	rm -rf out
	mkdir out

copyAssets: clean
	cp -r imgs/* out/.
	cp -r static/* out/.
pandoc:
	npx -p @mermaid-js/mermaid-cli mmdc --cssFile mermaid.css ".label foreignObject { font-size: 14px; }" -i src/*.md -o --outputFormat=svg -o out/index.md -t dark -b transparent
	pandoc out/index.md -o out/index.html --mathjax --template template.html --no-highlight --filter pandoc-sidenote

	rm out/index.md

build: copyAssets pandoc

view:  copyAssets pandoc
	xdg-open out/index.html


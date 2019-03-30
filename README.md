![](assets/logo.png)

# Dokanki

Convert google docs, pdfs, html and other structured documents to Anki flashcards.

## Supported formats
- Google Doc
- HTML
- DOCX
- And more!

## Usage

```
usage: dokanki [-h] --name NAME [--id ID] [-l LEVEL]
               [--steps STEPS [STEPS ...]] [-t TYPE] [-o OUT]
               url

Anki flashcard extractor from any document

positional arguments:
  url                   file or web url of a document

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           deck name
  --id ID               unique deck id, useful for updating existing anki
                        databases
  -l LEVEL, --level LEVEL
                        header level/depth to extract questions from
  --steps STEPS [STEPS ...]
                        time steps for flashcards
  -t TYPE, --type TYPE  file format to overwrite pandocs default behavior
  -o OUT, --out OUT     anki database output file name
```

### Example
```cmd
./dokanki.py 
    --name NAME
    --id ID
    --level 2
    --out file.apkg
    "https://docs..."
```
# TSranslator

TSranslator is a Python script to automatically translate Qt TS files using google translate.

1. Generate the TS file `lupdate-pro src/MyProgram.pro translations/MyProgram_fr.ts`
2. Translate file `python TSranslator translations/MyProgram_fr.ts`

Parameters:
* TSranslator can take a list of TS files. The output language is deducted directly from the input file.
* -d do not modify the TS file
* -i list of words to exclude from the translation (-d "MyProgram" "No translation")

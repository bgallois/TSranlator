import re
from googletrans import Translator
from tqdm import tqdm
import argparse
import os

def read(file):
    with open(file, "r") as file:
        return file.readlines()

def write(file, lines):
    with open(file, "w") as file:
        return file.write("".join(lines))

def translate_request(word, lang):
    translator = Translator()
    return translator.translate(word, dest=lang)

def special_format(word):
    return word.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\'", "&apos;")

def ignore_word(line, words, decode):
    for i in words:
        if not decode:
            line = line.replace(i, "".join(["_" + k for k in i]).format(i))
        else:
            line = line.replace("".join(["_" + k for k in i]).format(i), i)
    return line

def translate_file(lines, ignores):
    lang = re.search("language=\"(.+)\"", lines[2]).group(1)
    for i, j in tqdm(enumerate(lines)):
        m = re.search("<source>(.+)</source>", j)
        if m:
            src = m.group(1)
            src = ignore_word(src, ignores, False)
            trad = translate_request(src, lang).text
            trad = ignore_word(trad, ignores, True)
            trad = special_format(trad)
            lines[i+1] = "        <translation>{}</translation>\n".format(trad)
    return lines

def run(path, dryrun, ignores):
    output_lines = translate_file(read(path), ignores)
    if dryrun:
        print(output_lines)
    else:
        write(path, output_lines)

parser = argparse.ArgumentParser(description='Translate automatically a TS file')
parser.add_argument('path', metavar='path', type=str, nargs='+', help='path or list of path to the TS file')
parser.add_argument('-i', dest='ignore_words', type=str, nargs='+', help='keys to ignore in the traduction')
parser.add_argument('-d', dest='dryrun', action=argparse.BooleanOptionalAction, help='do not modify the file')
args = parser.parse_args()
for i in args.path:
    i = os.path.abspath(i)
    if os.path.exists(i):
        run(i, args.dryrun, args.ignore_words)
    else:
        raise ValueError("{} do not exist".format(i))

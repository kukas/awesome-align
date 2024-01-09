from mosestokenizer import MosesTokenizer
import tokenize_uk # tokenize_words, tokenize_sents, tokenize_text
import difflib
from IPython.display import display, HTML

def display_spaces(line):
    # usage:
    # HTML(display_spaces(df["original"][0]))

    words = line.split(" ")
    return "<span style='background-color: #FFFF88;'> </span>".join(words)
def display_diff(seqm):
    # code adapted from https://stackoverflow.com/questions/62008142/how-can-i-format-the-output-of-pythons-difflib-htmldiff-to-make-it-readable
    # usage:
    # display(HTML(display_diff(difflib.SequenceMatcher(None, df["original"][0], df["tokenize_uk"][0]))))

    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(display_spaces(seqm.b[b0:b1]))
        elif opcode == 'insert':
            output.append("<span style='background-color: #88FF88;'>" + seqm.b[b0:b1] + "</span>")
        elif opcode == 'delete':
            output.append("<div style='display:inline-block;background-color: #FF0000;width:2px;margin-right:-2px;height:1.5em;'></div>")
        elif opcode == 'replace':
            output.append("<span style='background-color: #FF88FF;'>" + seqm.b[b0:b1] + "</span>")
        else:
            raise RuntimeError( f"unexpected opcode unknown opcode {opcode}" )
    return ''.join(output)
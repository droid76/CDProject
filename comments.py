import re

def remove_comments(text):
    p = r'/\*[^*]*\*+([^/*][^*]*\*+)*/|//[^\n]*|("(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\'|.[^/"\'\\]*)'
    return ''.join(m.group(2) for m in re.finditer(p, text, re.M|re.S) if m.group(2))

code_w_comments = open("input.c").read()
code_wo_comments = remove_comments(code_w_comments)
fh = open("nocomments.c", "w")
fh.write(code_wo_comments)
fh.close()


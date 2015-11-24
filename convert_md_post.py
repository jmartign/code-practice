#!/usr/bin/env python

import codecs
import os.path
from StringIO import StringIO

def convert_md_file(src_file, dest_file):
    srcf = codecs.open(src_file, 'rb', 'utf-8')
    in_memory = False
    if os.path.abspath(src_file) == os.path.abspath(dest_file):
        outf = StringIO()
        in_memory = True
    else:
        outf = codecs.open(dest_file, 'wb', 'utf-8')
    in_codeblock = False
    for line in srcf:
        striped_line = line.strip(' \t\n')
        if striped_line == '{% include JB/setup %}':
            continue
        if striped_line.startswith('{% highlight'):
            lang = None
            parts = striped_line.split(' ')
            if len(parts) == 4:
                lang = parts[2]
            outf.write(lang and '{%% codeblock lang:%s %%}\n'%(lang,) or '{% codeblock %}\n')
            continue
        if striped_line == '{% endhighlight %}':
            outf.write('{% endcodeblock %}\n')
            continue
        if line.startswith('    :::') and not in_codeblock:
            in_codeblock = True
            codeblock_lines = []
            lang = striped_line[3:]
            outf.write(lang and '{%% codeblock lang:%s %%}\n'%(lang,) or '{% codeblock %}\n')
        elif in_codeblock:
            if line.startswith('    '):
                codeblock_lines.append(line[4:])
            elif len(striped_line) == 0:
                codeblock_lines.append('\n')
            else:
                i = 0
                while codeblock_lines[-1] == '\n':
                    del codeblock_lines[-1]
                    i += 1
                for ln in codeblock_lines:
                    outf.write(ln)
                outf.write('{% endcodeblock %}\n')
                outf.write('\n' * i)
                in_codeblock = False
                codeblock_lines = []
                outf.write(line)
        else:
            outf.write(line)
    srcf.close()
    if in_memory:
        wf = codecs.open(dest_file, 'wb', 'utf-8')
        wf.write(outf.getvalue())
        outf.close()
        wf.close()
    else:
        outf.close()

def convert_all_under_folder(folder_path):
    import glob
    import os.path
    flist = glob.glob(os.path.join(folder_path, '*.md'))
    for f in flist:
        convert_md_file(f, f)

if __name__ == '__main__':
    #convert_md_file('test.md', 'test2.md')
    convert_all_under_folder('./')




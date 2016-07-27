# coding: utf-8
import os
import codecs

input_file = u'在红尘中修行.txt'
output_dir = 'ebook'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    

book_name = ''
part_list = []
current_subject = ''
current_p_list = []

for line in codecs.open(input_file, 'r', 'utf-8'):
    if line.startswith('<'):
        book_name = line.strip('<>\r\n')
    elif not line.strip():
        continue
    elif line.startswith(' '):
        current_p_list.append(line.strip())
    else:
        line = line.strip()
        if not current_subject:
            current_subject = line
        else:
            part_list.append({
                'subject': current_subject,
                'p_list': current_p_list,
            })
            current_subject = line
            current_p_list = []

if current_p_list:
    part_list.append({
        'subject': current_subject,
        'p_list': current_p_list,
    })

# README.md
f = codecs.open(os.path.join(output_dir, 'README.md'), 'w', 'utf-8')
f.write(u'# %s\n\n' % book_name)
f.close()

# SUMMARY.md
f = codecs.open(os.path.join(output_dir, 'SUMMARY.md'), 'w', 'utf-8')
f.write(u'# %s\n\n' % book_name)
n = 0
for part in part_list:
    n += 1
    f.write(u'* [%s](content/%02d.md)\n' % (part['subject'], n))
f.close()

# content
content_dir = os.path.join(output_dir, 'content')
if not os.path.exists(content_dir):
    os.mkdir(content_dir)
n = 0
for part in part_list:
    n += 1
    f = codecs.open(os.path.join(content_dir, '%02d.md' % n), 'w', 'utf-8')
    f.write(u'# %s\n\n' % part['subject'])
    for p in part['p_list']:
        f.write(p)
        f.write('\n\n')
    f.close()


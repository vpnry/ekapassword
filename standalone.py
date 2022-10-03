'''Generate v1_ekapassword_standalone.html

'''

import os
import re

rep_places = '''
<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
<script src="js/jquery-3.6.1.min.js"></script>
<script src="bootstrap/js/bootstrap.min.js"></script>
<script src="js/jsSHA-3.2.0/dist/sha512.js"></script>
'''.strip().split('\n')


def rf(f):
    with open(f, 'r', encoding='utf-8') as fin:
        return fin.read()


def getAttr(txt):
    reg = re.compile(r'(<link href|<script src)="(.*?)"')
    x = re.findall(reg, txt)
    return x


def joinall(f='./index.html'):
    html = rf(f)

    for e in rep_places:
        if not e in html:
            print('** NOT FOUND', e)
            continue

        attr = getAttr(e)

        file_pat = attr[0][1]
        if not os.path.isfile(file_pat):
            print('This file is not exist', file_pat)
            continue

        ct = rf(file_pat)
        print('Adding', file_pat)

        if attr[0][0] == '<script src':
            html = html.replace(e, '<script>\n' + ct + '\n</script>', 1)

        elif attr[0][0] == '<link href':
            html = html.replace(e, '<style>\n' + ct + '\n</style>', 1)

    with open('./v1_ekapassword_standalone.html', 'w', encoding='utf-8') as fio:
        fio.write(html)

    print('\n\n v1_ekapassword_standalone.html sha512sum now is:')

    os.system('sha512sum v1_ekapassword_standalone.html')

    print('\n\n Remember to update sha512sum value in the Readme file.')

    print('Done')


if __name__ == '__main__':
    joinall()

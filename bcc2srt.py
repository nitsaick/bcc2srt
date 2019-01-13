import re
import sys
from optparse import OptionParser

def check(s):
    symbols = {'}': '{', ']': '[', ')': '('}
    symbols_l, symbols_r = symbols.values(), symbols.keys()
    arr = []
    for c in s:
        if c in symbols_l:
            arr.append(c)
        elif c in symbols_r:
            if arr and arr[-1] == symbols[c]:
                arr.pop()
            else:
                return False
    
    return not arr


def time2str(t):
    ms = int(round(t % 1, 3) * 1000)
    s = int(t)
    m = s // 60
    h = m // 60
    m = m % 60
    s = s % 60
    t_str = '{:0>2}:{:0>2}:{:0>2},{:0>3}'.format(h, m, s, ms)
    return t_str


def bcc2srt(bcc_filename, srt_filename):
    bcc_file = open(bcc_filename, 'r', encoding='utf8')
    text = bcc_file.read()
    if check(text) is False:
        print('Bad format!')
        sys.exit(-1)

    body = re.findall('\[(.*?)\]', text)[0]
    elements = re.findall('\{(.*?)\}', body)
    srt_file = open(srt_filename, 'w', encoding='utf8')
    
    for i in range(len(elements)):
        element = elements[i].split(',')
        time_from = float(element[0].split(':')[1])
        time_to = float(element[1].split(':')[1])
        location = int(element[2].split(':')[1])
        content = element[3].split(':')[1][1:-1].replace('\\"', '"')
        
        srt_file.write('{}\n'.format(i + 1))
        srt_file.write('{} --> {}\n'.format(time2str(time_from), time2str(time_to)))
        srt_file.write('{}\n\n'.format(content))
        
    srt_file.close()
    bcc_file.close()


def get_args():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='bcc_filename', default='', help='bcc filename')
    parser.add_option('-o', '--output', dest='srt_filename', default='', help='srt filename')
    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    args = get_args()
    assert len(args.bcc_filename) != 0
    assert len(args.srt_filename) != 0
    
    bcc2srt(args.bcc_filename, args.srt_filename)

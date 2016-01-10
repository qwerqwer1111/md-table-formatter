# coding: utf-8

import re
import sys
import unicodedata


(ALIGN_LEFT,
 ALIGN_CENTER,
 ALIGN_RIGHT) = range(3)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    encoding = get_text_encoding('\n'.join(lines))

    lines = [line.decode(encoding) if isinstance(line, str) else line for line in lines]

    formatted_lines = lines[:]
    buf = []
    for i, line in enumerate(lines):
        if '|' in line:
            buf.append(line)
        else:
            buf_length = len(buf)
            if buf_length >= 3:
                formatted_lines[i - buf_length:i] = table_formatter(buf)
            buf = []
    buf_length = len(buf)
    if buf_length >= 3:
        formatted_lines[len(lines) - buf_length:len(lines)] = table_formatter(buf)

    formatted_lines = [line.encode(encoding) if isinstance(line, unicode) else line
                       for line in formatted_lines]

    for line in formatted_lines:
        print line


def table_formatter(original_table):
    elements = [split_table_row(row) for row in original_table]

    if min([len(row) for row in elements]) != max([len(row) for row in elements]):
        return original_table

    columns_max_width = [get_text_width(s) for s in elements[0]]
    for content in elements[2:]:
        for i, c in enumerate(content):
            columns_max_width[i] = max(get_text_width(c), columns_max_width[i])

    aligns = []

    for align in elements[1]:
        if re.match(r'^:?-+:?$', str(align)) is None:
            return original_table

        if str(align).startswith(':-') and str(align).endswith('-:'):
            aligns.append(ALIGN_CENTER)
        elif str(align).endswith('-:'):
            aligns.append(ALIGN_RIGHT)
        else:
            aligns.append(ALIGN_LEFT)

    formatted_table = []

    formatted_headers = [append_space(header, align, width)
                         for header, align, width in zip(elements[0], aligns, columns_max_width)]
    formatted_table.append('|' + '|'.join(formatted_headers) + '|')
    formatted_aligns = [generate_align_element(align, width)
                        for align, width in zip(aligns, columns_max_width)]
    formatted_table.append('|' + '|'.join(formatted_aligns) + '|')
    for contents in elements[2:]:
        formatted_contents = [append_space(content, align, width)
                              for content, align, width in zip(contents, aligns, columns_max_width)]
        formatted_table.append('|' + '|'.join(formatted_contents) + '|')

    return formatted_table


def generate_align_element(align, width):
    formatted_align = '-' * (width + 2)
    if align == ALIGN_CENTER:
        formatted_align = ':' + formatted_align[1:-1] + ':'
    elif align == ALIGN_RIGHT:
        formatted_align = formatted_align[:-1] + ':'
    else:
        formatted_align = ':' + formatted_align[1:]
    return formatted_align


def append_space(text, align, width):
    num_spaces = width - get_text_width(text)
    left_spaces = ''
    right_spaces = ''
    if align == ALIGN_CENTER:
        left_spaces = ' ' * int(num_spaces / 2)
        right_spaces = ' ' * (int(num_spaces / 2) + num_spaces % 2)
    elif align == ALIGN_RIGHT:
        left_spaces = ' ' * num_spaces
    else:
        right_spaces = ' ' * num_spaces
    return ' ' + left_spaces + text + right_spaces + ' '


def split_table_row(table_row):
    ret = table_row.split('|')
    ret = [s.strip() for s in ret]
    if table_row.startswith('|'):
        ret = ret[1:]
    if table_row.endswith('|'):
        ret = ret[:-1]
    return ret


def get_text_width(text):
    num_full_width = 0
    for c in text:
        eaw = unicodedata.east_asian_width(c)
        if eaw in (u'W', u'F', u'A'):
            num_full_width += 1
    return len(text) + num_full_width


def get_text_encoding(text):
    encodings = ('utf8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                 'shift_jis', 'shift_jis_2004', 'shift_jisx0213',
                 'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
                 'iso2022_jp_ext', 'latin_1', 'ascii')
    for encoding in encodings:
        try:
            text = text.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass


if __name__ == '__main__':
    main()

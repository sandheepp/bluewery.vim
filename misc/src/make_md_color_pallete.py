#!/usr/bin/env python3
'''
Generate color pallete for markdown document
from color/bluewery.vim source code.
'''
from pprint import pprint as pp

import argparse
import re
from pprint import pprint as pp  # noqa
from typing import (  # noqa
        Any,
        List,
        Dict,
        Tuple,
        )


color_map: Dict[int, str] = {
    0: 'black',
    1: 'red',
    2: 'green',
    3: 'yellow',
    4: 'blue',
    5: 'magenta',
    6: 'cyan',
    7: 'white',
}

MD_START_TMPL = '<!-- Autogenerated-pallete start {} -->'
MD_END_TMPL = '<!-- Autogenerated-pallete end {} -->'


def _dump_pallete_table(colors: List[str]) -> str:
    # make table sources
    table_sources: List[List[str]] = []
    table_sources.append([
        'color_name',
        'color_code',
        'color',
        'color_name',
        'color_code',
        'color',
    ])
    table_sources.append(['---'] * 6)
    for i, (n_color, b_color) in enumerate(zip(colors[:8], colors[8:])):
        table_sources.append(
                [
                    f'{color_map[i]} (normal)',
                    f'`#{n_color}`',
                    f'![#{n_color}](https://placehold.it/50x20/{n_color}/000000?text=+)',  # noqa
                    f'{color_map[i]} (bright)',
                    f'`#{b_color}`',
                    f'![#{b_color}](https://placehold.it/50x20/{b_color}/000000?text=+)',  # noqa
                    ]
                )

    # calc max length for each column
    column_max_lengths: List[int] = []
    for column_i in range(6):
        column = [source[column_i] for source in table_sources]
        column_max_lengths.append(max([len(item) for item in column]))

    # align
    for table_source in table_sources:
        for i, item in enumerate(table_source):
            table_source[i] = item + ' ' * (column_max_lengths[i] - len(item))

    res = ''
    # dump
    for source in table_sources:
        res += '|' + '|'.join(source) + '|\n'
    return res


def main() -> None:
    with open(args.color_script_path) as f:
        lines = f.readlines()

    colors = []
    for line in lines:
        m = re.search(r'let *\S* *= *\[\d+, *\'#(?P<color>\w{6})\'\]', line)
        if m is not None:
            colors.append(m.group('color'))
    table_str = _dump_pallete_table(colors)
    with open(args.target_markdown) as f:
        content = f.read()
    # replace autogenerated part
    start_key = MD_START_TMPL.format(args.template_key)
    end_key = MD_END_TMPL.format(args.template_key)
    content = re.sub(
        (
            re.escape(start_key) +
            r'(.|\s)*' +
            re.escape(end_key)),
        start_key + '\n' + table_str + end_key,
        content,
    )
    # re-write
    with open(args.target_markdown, 'w') as f:
        f.write(content)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('color_script_path', type=str)
    parser.add_argument('target_markdown', type=str)
    parser.add_argument('template_key', type=str)
    args = parser.parse_args()
    main()

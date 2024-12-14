import re

def add_star_badge(repo_link):
    match = re.search(r'https?://github\.com/([\w\-_]+)/([\w\-_]+)', repo_link)
    if match:
        user, repo = match.groups()
        star_badge = f' ![Star](https://img.shields.io/github/stars/{user}/{repo}.svg?style=social&label=Star)'
        if star_badge not in repo_link:
            return repo_link + star_badge
    return repo_link

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

def process_table(table_text):
    lines = table_text.strip().split('\n')
    if len(lines) < 3:
        return table_text

    header = lines[0]
    separator = lines[1]
    rows = lines[2:]

    headers = [h.strip() for h in header.strip('|').split('|')]
    try:
        repo_index = headers.index('Repo')
    except ValueError:
        return table_text

    new_rows = []
    for row in rows:
        cells = [c.strip() for c in row.strip('|').split('|')]
        if len(cells) != len(headers):
            new_rows.append(row)
            continue
        repo_cell = cells[repo_index]
        if 'github.com' in repo_cell and 'img.shields.io/github/stars' not in repo_cell:
            cells[repo_index] = add_star_badge(repo_cell)
        new_row = '| ' + ' | '.join(cells) + ' |'
        new_rows.append(new_row)

    return '\n'.join([header, separator] + new_rows)

def update_content(content):
    table_pattern = re.compile(r'(\|.*?\|\n\|[-\s|:]*\|\n(?:\|.*?\|\n)+)', re.MULTILINE)
    new_content = table_pattern.sub(lambda m: process_table(m.group(1)), content)
    return new_content

new_content = update_content(content)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
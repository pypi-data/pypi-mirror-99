from sys import argv
import re

tags = [
    'a', 'abbr', 'adress', 'area',
    'article', 'aside', 'audio', 'b',
    'base', 'bdi', 'bdo', 'blockquote',
    'body', 'br', 'button', 'canvas',
    'caption', 'cite', 'code', 'col',
    'colgroup', 'data', 'datalist', 'dd',
    'del', 'details', 'dfn', 'dialog',
    'div', 'dl', 'dt', 'em', 'embed',
    'fieldset', 'figcaption', 'figure',
    'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'head', 'header', 'hr', 'html', 'i',
    'iframe', 'img', 'input', 'title', 'html'
]


def html_render(line):
    tag = re.search(r'\w+', line)
    if tag:
        tag = tag.group(0)
        if tag in tags:
            if ('.' + tag) in line:
                line = line.replace('.' + tag, '</' + tag).replace('\n', '>\n')
            else:
                line = line.replace(tag, '<' + tag).replace('\n', '>\n')
    return line


def repeat_input(file, array, count):
    for i in range(count):
        for line in array:
            line = html_render(line)
            file.write(line)


def main(file_name):
    fox_file = open(file_name, 'r')
    arr_file = []
    for line in fox_file:
        arr_file.append(line)
    fox_file.close()
    result_file = open('fox_' + file_name, 'w')

    i = 0
    while i < len(arr_file):
        line = arr_file[i]
        if '% repeat ' in line:
            quantity = int(line[line.rfind(' %') - 1])
            for k in range(i + 1, len(arr_file)):
                if '% end %' in arr_file[k]:
                    repeat_input(result_file, arr_file[i + 1: k], quantity)
                    i += len(arr_file[i + 1: k]) + 2
                    break
            continue
        i += 1
        line = html_render(line)
        result_file.write(line)

    result_file.close()


if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        print('Необходимо ввести 1 параметр - имя файла, если он находится в одной директории со скриптом'
              ',или путь до файла!')

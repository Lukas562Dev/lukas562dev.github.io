from subprocess import Popen, PIPE, STDOUT


def md_to_html(md):
    p = Popen(['pandoc', '-f', 'markdown_github', '-t', 'html'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout = p.communicate(input=md.encode())[0]

    text = stdout.decode()

    text = text.replace('href="', 'rel="noopener noreferrer nofollow" target="_blank" href="')

    return text


if __name__ == "__main__":
    print('This file is supposed to be used as a library')

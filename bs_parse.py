import requests
from bs4 import BeautifulSoup, NavigableString, Comment
import argparse
import textwrap as tw
import requests_cache

requests_cache.install_cache('demo_cache')


def print_content(body, args):
    descendants_list = list(body.descendants)
    res = []
    for child in descendants_list:
        if isinstance(child, NavigableString):
            child = child.strip()
            res.append(child)
        elif args.img and child.name == 'img':  # replace images with their links if neccessary
            res.append(child['src'])
    res = list(map(lambda x: x.strip(), res))
    res = list(filter(lambda x: x != '', res))
    text = "\n".join(res)
    wrapper = tw.TextWrapper(width=args.width, break_long_words=args.break_long, replace_whitespace=False)
    if args.file:  # write in file
        with open(args.file, 'w', encoding="utf-8") as fp:
            fp.write(wrapper.fill(text))
    else:
        print(wrapper.fill(text))


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", dest="width", default=70,
                        type=int, help='an integer for the accumulator')
    parser.add_argument("-i", "--images", dest="img", default=False,
                        action="store_true", help="replace images with their links")
    parser.add_argument("-b", "--breaklong", dest="break_long", default=False,
                        action="store_true", help="break long words")
    parser.add_argument("-u", "--url", dest="url", default='https://www.python.org/',
                        type=str)
    parser.add_argument("-f", "--file", dest="file", default="",
                        type=str)
    args = parser.parse_args()
    return args


def remove_redundant_tags(soup):
    for _ in soup.find_all("script"):
        soup.script.decompose()
    for _ in soup.find_all("style"):
        soup.style.decompose()
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()


def main():
    # default url = 'https://www.python.org/'
    args = parse_options()
    page = requests.get(args.url)
    soup = BeautifulSoup(page.text, "html.parser")
    remove_redundant_tags(soup)
    body = soup.body
    if body is not None:
        print_content(body, args)
    else:
        print("No useful content... Check response")


if __name__ == "__main__":
    main()

# python bs_parse.py -f page_content.txt -u https://www.python.org/ -i

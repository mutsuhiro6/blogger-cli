#! /usr/bin/env python
import argparse
import os
import json
from blogger_service import blogger_service
from markdown import Markdown


def post(blogId, isDraft, body):
    blogger = blogger_service()
    res = blogger.posts().insert(blogId=blogId, isDraft=isDraft, body=body).execute()
    return res


def generate_body(title, content, labels):
    dict = {
        'title': title,
        'content': content,
        'labels': labels
    }
    return dict


def html_content_from_md(md_file_path):
    md = Markdown(extensions=['tables'])
    f = open(md_file_path, 'r')
    return md.convert(f.read())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', type=str)
    parser.add_argument('input', type=str, help='Input .md file path.')
    parser.add_argument('-d', '--draft', action='store_true',
                        help='Post as a draft.')
    parser.add_argument('-l', '--labels', nargs='*')
    parser.add_argument(
        '--id', type=str, help='Can specify blog ID of Blogger.')

    args = parser.parse_args()
    blogId = args.id
    if blogId is None:
        path = os.path.join(os.path.dirname(__file__), 'blogId.txt')
        blogId = open(path, 'r').read()

    labels = args.labels
    if labels is None:
        labels = []

    content = html_content_from_md(args.input)
    body = generate_body(args.title, content, labels)

    # print(args.input)
    # print(blogId)
    # print(args.draft)
    # print(body)

    response = post(blogId=blogId, isDraft=args.draft, body=body)
    input_dir = os.path.dirname(args.input)
    with open(os.path.join(input_dir, 'post.json'), 'w') as f:
        json.dump(response, f, ensure_ascii=False)


if __name__ == "__main__":
    main()

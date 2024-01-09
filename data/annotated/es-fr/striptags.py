import argparse
import re

def strip_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Use regex to strip tags and call strip() to remove leading and trailing whitespaces
    stripped_lines = [re.sub(r'<[^>]+>', '', line).strip() for line in lines]

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(stripped_lines))

def main():
    parser = argparse.ArgumentParser(description='Strip tags from a file and remove leading and trailing whitespaces.')
    parser.add_argument('input_file', help='Input filename with tags')
    parser.add_argument('output_file', help='Output filename without tags')

    args = parser.parse_args()

    strip_tags(args.input_file, args.output_file)
    print(f'Tags stripped successfully. Result saved to {args.output_file}')

if __name__ == '__main__':
    main()

import argparse
from convert_annotations_utils import Alignment
from collections import defaultdict

def convert_to_pharaoh_format(input_file, output_file):
    alignments = []

    # Read alignments from the input file
    with open(input_file, 'r') as f:
        for line in f:
            sentence_num, src_index, tgt_index, alignment_type = line.split()

            sentence_num, src_index, tgt_index = map(int, (sentence_num, src_index, tgt_index))
            alignment = Alignment(src_index, tgt_index, alignment_type)
            alignments.append((sentence_num, alignment))

    # Group alignments by sentence number
    sentence_alignments = defaultdict(list)
    for sentence_num, alignment in alignments:
        sentence_alignments[sentence_num].append(alignment)

    # Convert alignments to Pharaoh format
    pharaoh_alignments = []
    for sentence_num, alignments in sentence_alignments.items():
        pharaoh_line = " ".join(str(alignment) for alignment in sorted(alignments))
        pharaoh_alignments.append(pharaoh_line)

    # Write Pharaoh format to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(pharaoh_alignments))

def main():
    parser = argparse.ArgumentParser(description='Convert word alignments from flattened format to Pharaoh format.')
    parser.add_argument('input_file', help='Input filename with flattened alignments')
    parser.add_argument('output_file', help='Output filename for Pharaoh format alignments')

    args = parser.parse_args()

    convert_to_pharaoh_format(args.input_file, args.output_file)
    print(f'Alignments converted successfully. Result saved to {args.output_file}')

if __name__ == '__main__':
    main()

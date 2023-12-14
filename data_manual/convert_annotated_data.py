import xml.etree.ElementTree as ET
import argparse

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    sentences = []
    
    for s in root.findall('.//s'):
        ukrainian = s.find('ukrainian').text
        czech = s.find('czech').text
        sure = s.find('sure').text
        possible = s.find('possible').text
        if sure is None:
            sure = ""
        if possible is None:
            possible = ""
        
        sentences.append({
            'ukrainian': ukrainian,
            'czech': czech,
            'sure': sure,
            'possible': possible
        })
    
    return sentences

def create_gold_file(sentences, output_file):
    with open(output_file, 'w') as f:
        for s in sentences:
            sure = s['sure'].split()
            possible = s['possible'].replace("-", "p").split()
            all_alignments = sure + possible
            # all_alignments = sorted(all_alignments)
            f.write(' '.join(all_alignments) + '\n')

def create_src_tgt_file(sentences, output_file):
    with open(output_file, 'w') as f:
        for s in sentences:
            f.write(s['czech'] + ' ||| ' + s['ukrainian'] + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process XML file and create .gold and .src-tgt files.')
    parser.add_argument('input_xml', help='Input XML file')
    parser.add_argument('output_gold', help='Output .gold file')
    parser.add_argument('output_src_tgt', help='Output .src-tgt file')
    
    args = parser.parse_args()
    
    sentences = parse_xml(args.input_xml)
    
    create_gold_file(sentences, args.output_gold)
    create_src_tgt_file(sentences, args.output_src_tgt)

import os
import argparse


#check if the input file that is provided by the user exists
def check_if_file_exists(file):
    if not os.path.exists(file):
        raise argparse.ArgumentTypeError(f"{file} does not exist")
    return file

#parse command line arguments, 5 flags that are described below
def parse():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-db', '--database', required = True, type = check_if_file_exists, help='Path to zipped FASTA input file.')
    parser.add_argument('-list', '--list_file', required = True, type = check_if_file_exists, help='Path to file with peptide list.')

    mut_exclu = parser.add_mutually_exclusive_group(required=True)
    mut_exclu.add_argument('-exact', '--exact_match', action = 'store_const', const = 'exact', help = 'Exact match')
    mut_exclu.add_argument('-inexact', '--inexact_match', type=int, default=None, help='Inexact match with number of mismatches.')

    parser.add_argument('-out', '--output', required=True, help = 'Enter the name for the output file')
    args = parser.parse_args()

    return args

def get_fasta_file(args):
    fasta_file = args.database
    return fasta_file

def get_peptide_list_from_args(args):
    peptide_list = args.list_file
    return peptide_list

def proceed_with_exact_match(args):
    exact_match = args.exact_match
    return exact_match

def proceed_with_inexact_match(args):
    inexact_match = args.inexact_match
    return inexact_match

def output_file(args):
    output_name = args.output
    return output_name
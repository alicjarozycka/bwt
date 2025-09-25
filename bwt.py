import cli
import csv
import time
import pyfastx
import extract_sequences_from_fasta
from exact_match import *
from inexact_match import *


def create_permutations(sequence):
    '''
    Function name: create_permutations
    Arguments: sequence
    Returns: seq_array
    Function takes sequence that is provided by user in the input fasta file, and performs cyclic rotations. Creating all possible roations is an important step in the Burrows-Wheeler transformation.
    '''
    seq_array = []
    for i in range(len(sequence)):
        seq = bytearray(sequence[i:i+len(sequence)] + sequence[:i], 'utf-8')
        seq_array.append(seq)
    return seq_array


def sort_array_lexicographically(sequence_array):
    '''
    Function name: sort_array_lexicographically
    Arguments: sequence_array
    Returns: sorted array
    Function takes generated sequence array and then sorts it with lexicographic order.
    '''
    return sorted(sequence_array)


def get_bwt(sorted_array):
    '''
    Function name: get_bwt
    Arguments: sorted_array
    Returns: bwt
    Function takes sorted array and extracts last character from each element in sorted array. The result is the bwt string.
    '''
    bwt = []
    for element in sorted_array:
        element = element.decode()
        bwt.append(element[-1])
    return bwt


def get_index(sequence_array):
    '''
    Function name: get_index
    Arguments: sequence_array
    Returns: ind
    Function takes sequence array and returns indexes for each element.
    '''
    ind = []
    for i in range(len(sequence_array)):
        ind.append(i)
    return ind


def indexes_after_sorting(array_before_sorting, array_after_sorting):
    '''
    Function name: indexes_after_sorting
    Arguments: array_before_sorting, array_after_sorting
    Returns: suffix_id
    Function takes array before and after sorting and generates SA (suffix_id), which are the positions of the first symbols from the SA.
    '''
    suffix_id = []
    for index, element in enumerate(array_after_sorting):
        for indexx, elementt in enumerate(array_before_sorting):
            if element == elementt:
                suffix_id.append(indexx)
    return suffix_id


def c_array(bwt):
    '''
    Function name: c_array
    Arguments: bwt
    Returns: c_array
    Function takes a character from BWT and returns how many characters in the BWT are smaller than it.
    '''
    c_array = {}
    sorted_bwt = sorted(bwt)
    starting_number = 0

    for character in sorted_bwt:
        if character not in c_array:
            c_array[character] = starting_number
        starting_number += 1

    return c_array


def o_array(bwt):
    '''
    Function name: o_array
    Arguments: bwt
    Returns: o_array
    Function takes a character and a position in the BWT and returns the occurences - how many times that character appeared in the BWT to that position.
    '''
    o_array = {}

    for element in bwt:
        o_array[element] = [0]

    for index, element in enumerate(bwt):
        for key in o_array:
            if key == element:
                o_array[key].append(o_array[key][-1] + 1)
            else:
                o_array[key].append(o_array[key][-1])

    for element in o_array:
        o_array[element] = o_array[element][1:]

    return o_array


def read_peptide_list(path_to_peptide_file):
    '''
    Function name: read_peptide_list
    Arguments: path_to_peptide_file
    Returns: peptides from the file
    Function that extracts peptides from the file provided by the user.
    '''
    filename = path_to_peptide_file.split("/")[-1]
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()


def write_results_to_output(results, outputName, headers):
    '''
    Function name: write_results_to_output
    Arguments: results, outputName, headers
    Returns: TSV file
    Function saves results to the TSV file with the necessary headers.
    '''
    output_filename = f"{outputName}.tsv"
    with open(output_filename, 'w', newline='') as f:
        tsv_writer = csv.DictWriter(f, delimiter='\t', fieldnames=headers)
        tsv_writer.writeheader()
        tsv_writer.writerows(results)
        f.close()
    print(f"Results written to {output_filename}")


if __name__ == "__main__":

    #execution start time
    time_start = time.time()

    #parsing command line arguments and assigning the flags to variables
    args = cli.parse()
    fastaFilePath = cli.get_fasta_file(args=args)
    peptideListPath = cli.get_peptide_list_from_args(args=args)

    exactMatch = cli.proceed_with_exact_match(args=args)
    inexactMatch = cli.proceed_with_inexact_match(args=args)

    outputFileName = cli.output_file(args=args)


    results = []

    fastaLength = len(pyfastx.Fasta(fastaFilePath))

    c = 0

    #iterating over FASTA file and for each sequence performing Burrows-Wheeler transformation
    for sequence, sequenceId in extract_sequences_from_fasta.read_fasta(path_to_fasta_file=fastaFilePath):
        c+=1
        print(f"Successfully extracted protein {sequenceId}: {c} from a total of {fastaLength} sequences.")

        sequence = sequence + "$"

        seqArray = create_permutations(sequence=sequence)
        sortedArray = sort_array_lexicographically(sequence_array=seqArray)

        bwt = get_bwt(sorted_array=sortedArray)

        indexBefore = get_index(sequence_array=seqArray)
        indexAfter = indexes_after_sorting(array_before_sorting=seqArray,
                                            array_after_sorting=sortedArray)

        #iterating over peptides that are provided by the user and then performing either exact or inexact mapping
        for i, query in enumerate(read_peptide_list(peptideListPath), start=1):

            print(f"Working on {sequenceId} ({c}) => searching for peptide {query} (peptide {i})")


            if args.exact_match:
                exactMatches = exact_match(pattern=query,
                                        o_array=o_array(bwt=bwt),
                                        c_array=c_array(bwt=bwt),
                                        bwt=bwt)

                exactMatchesPositions = extract_positions(SA_intervals=exactMatches,
                                            SA=indexAfter,
                                            pattern=query)


                try:
                    if exactMatchesPositions:
                        for start_index, end_index in exactMatchesPositions:
                            results.append({"peptide": query, "protein_id": sequenceId, "start_index": start_index, "end_index": end_index})
                except (TypeError, IndexError):
                    pass



            elif args.inexact_match is not None:
                inexactMatches = inexact_search(W=query,
                                        z=inexactMatch,
                                        X=sequence,
                                        bwt=bwt)

                inexactMatchesPositions = positions(SA_intervals=inexactMatches,
                                            SA=indexAfter,
                                            pattern=query)
                try:
                    if inexactMatchesPositions:
                        for start_index, end_index in inexactMatchesPositions:
                            results.append({"peptide": query, "protein_id": sequenceId, "start_index": start_index, "end_index": end_index})
                except (TypeError, IndexError):
                    pass


    #saving results to TSV file
    write_results_to_output(results=results,
                            outputName=outputFileName,
                            headers = ["peptide", "protein_id", "start_index", "end_index"])


    #execution end time
    time_end = time.time()

    #duration time
    elapsed_time = (time_end - time_start)/60

    print(f'It took {elapsed_time} minutes')
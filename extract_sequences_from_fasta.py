import pyfastx

def read_fasta(path_to_fasta_file):
    '''
    Function name: read_fasta
    Arguments: path_to_fast_file
    Returns: seq, name
    Function read fasta file using pyfastx extension. It returns the sequence and its id.
    '''
    for seq in pyfastx.Fasta(path_to_fasta_file):
        yield seq.seq, seq.name.split("|")[1]
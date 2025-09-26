# Burrows-Wheeler Transformation (BWT)

## General info

The aim of the work was to implement a BWT algorithm that maps peptide sequences to protein sequences.

This implementation is the result of Master's Project at the Intercollegiate Faculty of Biotechnology UG&MUG in the Laboratory of Biopolymers Structure.

It was built using Python 3.10.4 version.

## How to run

To use this implementation, the first step is to install required library. From the project root directory, run this command in the terminal:

```
$ pip install -r requirements.txt
```

This command installs external library that is used in this project.

To run the bwt.pt script, pay close attention to the arguments outlined in the table below:

| Argument | Parameter description | Is the argument required? |
| :-----: | :---: | :---: |
| -db / --database | Path to the input file that acts as a database (.fa.gz) | Yes |
| -list / --list_file | Path to the file with peptides list (.txt/.list) | Yes |
| -out / --output | Provide the name for the output file | Yes |
| -exact / --exact_match | An argument used to enable exact search | Yes |
| -inexact / --inexact_match | An argument that enables mismatch search; provide a value following the argument | Yes |


Example commands to execute exact and inexact matching in the algorithm:

- Exact match:
```
$ py bwt.py -db path_to_database.fa.gz -list path_to_peptides_list -out output_filename -exact 
```

- Inexact match with 1 mismatch:
```
$ py bwt.py -db path_to_database.fa.gz -list path_to_peptides_list -out output_filename -inexact 1
```

#Data Summariser
This repository uses python (2.7) to summarise data from Comma Seperated Values (CSV), Teb-Separated Values (TSV) and JSON file.
The result produces JSON file which summrises data with basic statistics.

##Introduction
Data comes in many formats and in varying degrees of quality. The first steps when considering a new file of data for processing are to establish facts about its format, the special characters it uses such as separators and string enclosures, whether or not it has a header row, and so on. Once these things have been established, you might want to summarise the data or identify problems such as missing values.

This Python program uses JSON to describe the contents of a file and as a form of command language for manipulating data. JSON will be used both to control the program (there will be no GUI) and as the format in which results are generated.

##Generating Metadata
The program will read a file and generate metadata about that file. The file format details are one example of metadata. Other required metadata fields are described below. The output from program will be a JSON object containing the metadata extracted from a given file. The JSON object will contain an array of JSON objects, one for every field (or variable) defined in the file, plus some other fields describing the file as a whole. 

The JSON output about a file describes the following:
  - Filename
  - Format (JSON or tabular)
    - If tabular, specify character for field separator
    - If tabular, specify whether first row contains field names or not
  - Number of entries (rows if tabular, objects if JSON)
  - Number of fields (columns if tabular, different fields if JSON)
  - For each field:
    - Name
    - Type (numeric or string)
    - For numeric data: max, min
    - For string data: Number of different values the field takes

Here is an example:
  `{
  ‘filename’:’C:/data/data.csv’,
  ‘format’:{‘type’:’tabular’,’sep’:’,’},
  ‘headerrow’:1,
  ‘numentries’:100,
  ‘numfields’:2,
  ‘fields:[{‘name’:’ID’,’type’:’numeric’,’min’:0,’max’:100}, {‘name’:’Name’,’type’:’string’,’uniquevals’:30}]
  }`
  
If the input file is in CSV format, use the first row as column headings or, if there are no column headings, use ‘var1’, ‘var2’, etc.  If the file is in JSON format, the program builds the list of keys from the objects in the data. Only list the top level keys (i.e. ignore keys in embedded objects).

##Format Detection
The program accepts data in JSON or tabular format. It infers the format of the file from the file extension (.JSON, .txt, .csv), but also allow the input JSON parameter file to specify things about the format where known. For tabular files (.csv, .txt, etc.), the program attempts to guess the following:

- Does the first row contain field headings? If all the entries on the top row are strings, but subsequent rows contain numbers
, then your program can infer that the top row is a header.
- What is the field separator character? You may assume that .csv files use a comma and .txt files use a tab (\t).

For JSON format files, the program accepts a file where every row contains a single JSON object. The results of the guesses above should be written to the output file in JSON format, as in the example above. 

##Type Detection
The program attempts to detect the most likely type of each field, classifying each as either numeric or string. Use a regular expression to define the possible formats for a number (remember the possibility of scientific notation: 2.304e+3, for example
and negative numbers such as - 4.5). It is enough to identify the type of each variable based on the first record in a 
tabular file. For JSON, the program scans through the whole file to be sure of finding every variable, but it can still make reasonable decision about type based on the first occurrence of each variable name. When the data is in JSON format, the program can work on the top level fields only – do not process embedded objects. 

The default (if parameters do not specify otherwise) should be to write all fields of all records in the same format as the input file, including those with missing values. Consequently, all parameters are optional except the output file name. If that is missing, nothing is written.

##Counting Values and Max and Min
The JSON output file lists the maximum and minimum value for numeric fields and the number of unique values string fields can take. Check the type of each variable and decide which calculation to make. To count the number of unique values a field takes, store its possible values in a Python set and then find its length.


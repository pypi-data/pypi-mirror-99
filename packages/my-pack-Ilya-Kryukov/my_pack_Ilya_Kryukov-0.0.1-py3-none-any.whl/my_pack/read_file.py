def read_file(file_name="input.txt"):
    """Method for reading input data from a file.
    
    Keyword arguments:
    file_name -- name of the input file (default 'input.txt')
    
    """
    file = open(file_name,'r', encoding="utf-8")
    in_str = file.read()
    return in_str
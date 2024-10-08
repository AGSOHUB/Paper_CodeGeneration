import re
from pycparser import CParser, parse_file, c_ast
import subprocess
import os

# Set of known standard library functions and keywords
known_functions_and_keywords = {
    'printf', 'scanf', 'malloc', 'free', 'memcpy', 'memset', 'strcpy', 'strcmp', 
    'strlen', 'fopen', 'fclose', 'fread', 'fwrite', 'sprintf', 'sscanf', 
    'exit', 'abort', 'size_t', 'FILE', 'NULL', '__LINE__', '__FILE__', '__DATE__',
    '__asm__', 'sizeof', 'alignof', 'offsetof', 'static_assert', '__asm'
}
# Function to collect identifiers
class FunctionVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.defined_functions = set()
        self.undefined_functions = {}
        self.called_functions = []  # Initialize the called_functions list
        self.defined_variables = set()
        self.undefined_variables = set()
        self.defined_typedefs = set()
        self.undefined_typedefs = set()
        self.typedefs = set()
        self.defined_structs = set()
        self.undefined_structs = set()
        self.all_identifiers = set()
        self.function_identifiers = set()

    def visit_FuncDef(self, node):
        self.add_unique_identifier(node.decl.name, self.defined_functions)
        self.function_identifiers.add(node.decl.name)
        self.generic_visit(node)

    def visit_FuncCall(self, node):
        if isinstance(node.name, c_ast.ID):
            func_name = node.name.name
            if func_name in known_functions_and_keywords:
                return  # Skip known functions and keywords
            params = []
            if node.args:
                for arg in node.args.exprs:
                    if isinstance(arg, c_ast.ID):
                        params.append(arg.name)
            self.called_functions.append((func_name, ', '.join(params)))
            self.function_identifiers.add(func_name)
        self.generic_visit(node)

    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.TypeDecl) and node.name not in self.function_identifiers:
            self.add_unique_identifier(node.name, self.defined_variables)
        if isinstance(node.type, c_ast.Typename):
            type_name = node.type.type.names[0]
            self.add_unique_identifier(type_name, self.typedefs)
        self.generic_visit(node)

    def visit_TypeDecl(self, node):
        if node.declname and node.declname not in self.function_identifiers:
            self.add_unique_identifier(node.declname, self.defined_typedefs)
        self.generic_visit(node)

    def visit_Typedef(self, node):
        self.add_unique_identifier(node.name, self.typedefs)
        self.add_unique_identifier(node.name, self.defined_typedefs)
        self.generic_visit(node)

    def visit_Struct(self, node):
        if node.name:
            self.add_unique_identifier(node.name, self.defined_structs)
        self.generic_visit(node)

    def visit_ID(self, node):
        if node.name not in self.all_identifiers and node.name not in self.function_identifiers:
            self.add_unique_identifier(node.name, self.undefined_variables)
        self.generic_visit(node)

    def add_unique_identifier(self, identifier, collection):
        if identifier not in self.all_identifiers:
            self.all_identifiers.add(identifier)
            collection.add(identifier)

def find_missing():
    # Path to the fake includes directory
    fake_includes = r"compile_project\fake_libc_include"

    # Preprocess the main C file using gcc with fake includes
    preprocessed_file = r'compile_project\src\main.i'
    main_c_path = r'compile_project\src\main.c'

    # Create a visitor for function discovery
    visitor = FunctionVisitor()

    # Preprocess the main C file
    subprocess.run(['gcc', '-E', '-I', fake_includes, main_c_path, '-o', preprocessed_file], check=True)

    # Read the preprocessed file content
    with open(preprocessed_file, 'r') as file:
        content = file.read()

    # Replace hexadecimal constants with decimal equivalents
    content = re.sub(r'0x([0-9A-Fa-f]+)', lambda x: str(int(x.group(0), 16)), content)

    # Write the modified content back to the preprocessed file
    with open(preprocessed_file, 'w') as file:
        file.write(content)

    # Parse the preprocessed file
    parser = CParser()
    try:
        ast = parse_file(preprocessed_file, use_cpp=False)
    except Exception as e:
        print(f"Error parsing {main_c_path}: {e}")
        return [], [], []  # Return empty lists in case of an error

    # Visit the AST to gather function information
    visitor.visit(ast)

    # Read the original source code from the main C file
    with open(main_c_path, 'r') as file:
        source_code = file.read()

    # Find macro functions
    macro_functions = re.findall(r'#define\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)', source_code)
    macro_function_names = {name.strip() for name in macro_functions}

    # Find missing functions
    called_functions = [(name.strip(), params.strip()) for name, params in visitor.called_functions]
    missing_functions = [func for func in called_functions if func[0] not in visitor.defined_functions and func[0] not in macro_function_names]

    # Update params of missing functions with regex search
    for i, func in enumerate(missing_functions):
        func_name = func[0]
        # Create a regex pattern to find the function call with its parameters in the source code
        pattern = re.compile(rf'\b{re.escape(func_name)}\s*\(([^)]*)\)')
        match = pattern.search(source_code)
        if match:
            params = match.group(1)
            missing_functions[i] = (func_name, params)

    return missing_functions, visitor.undefined_variables, visitor.undefined_structs




def get_all_elements_from_codebase():
    # Path to the fake includes directory
    fake_includes = r"compile_project\fake_libc_include"

    # Preprocess the C file using gcc with fake includes
    preprocessed_file = r'compile_project\src\main.i'

    main_c_path =  r'compile_project\src\main.c'
    main_c_dir = os.path.dirname(main_c_path)

    # Collect all .c files in the directory
    c_files = [os.path.join(main_c_dir, f) for f in os.listdir(main_c_dir) if f.endswith('.c')]

    # Create a visitor and visit the AST
    visitor = FunctionVisitor()

    # Preprocess all .c files
    for c_file in c_files:
        subprocess.run(['gcc', '-E', '-I', fake_includes, c_file, '-o', preprocessed_file], check=True)

        # Read the preprocessed file content
        with open(preprocessed_file, 'r') as file:
            content = file.read()

        # Replace hexadecimal constants (e.g., 0x40020800) with decimal equivalents
        content = re.sub(r'0x([0-9A-Fa-f]+)', lambda x: str(int(x.group(0), 16)), content)

        # Write the modified content back to the preprocessed file
        with open(preprocessed_file, 'w') as file:
            file.write(content)

        # Parse the preprocessed file
        parser = CParser()
        try:
            ast = parse_file(preprocessed_file, use_cpp=False)
        except Exception as e:
            print(f"Error parsing {c_file}: {e}")
            continue

        visitor.visit(ast)

    # Collect all identifiers into lists
    all_elements = {
        'functions': list(visitor.defined_functions),
        'variables': list(visitor.defined_variables),
        'typedefs': list(visitor.defined_typedefs),
        'structs': list(visitor.defined_structs),
    }
    return all_elements
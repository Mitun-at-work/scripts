import ast

class ImportChecker:
    
    def __init__(self):
        pass

    def check_unused_imports(self, imports, code):

        self.imports = imports 
        self.code = code  

        try : 
            self.tree = ast.parse(code) 
        except :
            pass
        # Set to store used names
        used_names = set()

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name): 
                used_names.add(node.id)

        unused_imports = []
        for imp in self.imports:
            if imp not in used_names:
                unused_imports.append(imp)
        return unused_imports



if __name__ == '__main__' :
    ImportChecker().check_unused_imports()
class FetchImports() :
    
    def __init__(self):
        pass

    def fetch_imports(self, code) :

        imports_used = []
        import_lines = code.split('\n\n')[0]
        import_lines =  import_lines.split("\n")

        for line in import_lines : 
            line = line.split(' ')
            if line[0] == 'import' :
                imports_used.append(line[-1])
            else :
                n = len(line)
                flag = True
                for i in range(n - 1, -1, -1) :
                    if line[i] == 'import' :
                        break
                    if not('Axes3D' == line[i]) :
                        imports_used.append(line[i])
        return imports_used
            

if __name__ == '__main__' :
    fi = FetchImports()
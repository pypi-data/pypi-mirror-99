import os
def BuildPythonFile(self):
        if not self.algorithmFunc:
            raise Exception("""\n No algorithm supplied \n put the algorithm decorator over your function like this \n @CompuTradeEngine.algorithm \n def algorithm(): \n \t#algorithm""")
        else:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            with open(os.path.join(__location__, 'template.txt'), 'r') as fp:
                template = fp.readlines()
                fp.close()
            index=0

            AlgorithmPrep = []
            for line in self.algorithmFunc:
                AlgorithmPrep.append('    ' + line)

            index=0
            for line in template:
                if '#InsertAlgorithm' in line:
                    del template[index]
                    template[index:index] = AlgorithmPrep
                    break
                index+=1
            BuildDirectory = os.path.join(self.path, 'build')
            try:
                os.mkdir(BuildDirectory)
            except FileExistsError:
                pass
            with open(os.path.join(BuildDirectory, str(self.algorithm_name + '.py')), 'w') as file:
                file.writelines(template)




            print(BuildDirectory)
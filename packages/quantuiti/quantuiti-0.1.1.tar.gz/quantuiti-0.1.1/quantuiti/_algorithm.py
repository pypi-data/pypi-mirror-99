import inspect
def algorithm(self, function):
        lines = inspect.getsource(function)
        temp = lines.split('\n')
        del temp[0]
        index=0
        for line in temp:
            if 'def' in line:
                temp2 = line.split('def ')
                for line in temp2:
                    if line != '':
                        temp2 = line.split('(')
                        self.algorithm_name = temp2[0]
                        break

                subindex=0
                for line in temp2:
                    if '):' in line:
                        temp2 = line.split('):')
                        
                        subsubindex=0
                        temp3 = []
                        for line in temp2:
                            temp2[subsubindex] = temp2[subsubindex].strip()
                            if temp2[subsubindex]!='':
                                temp3.append(temp2[subsubindex])
                            subsubindex+=1
                        temp2=temp3
                                


                        break

                if len(temp2) > 0:
                    temp2.insert(0, 'self,')
                else:
                    temp2.insert(0, 'self')
                    
                temp2.insert(0, 'def ')
                temp2.insert(1, self.algorithm_name)
                temp2.insert(2, '(')
                temp2.insert(len(temp2), '):')
                temp2 = ''.join(temp2)
            

            index+=1
        temp[0] = temp2
        index=0
        for line in temp:
            temp[index] = str(line + '\n')
            index+=1

        self.algorithmFunc = temp
        self.algo = {}
        TempFunc = compile(''.join(self.algorithmFunc), 'algo', 'exec')
        exec(''.join(self.algorithmFunc), {}, self.algo)
        self.algo = self.algo['algo']
        if self.backtest:
            self.backtest_algorithm()
        if self.build:
            self.BuildPythonFile()
            
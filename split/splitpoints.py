import numpy as np

class Line():
    def __init__(self,startPos,values):
        self.startPos=startPos
        self.values=values
        self.length=len(values)

    def __eq__(self, other):
        return (self.length == other.length)

    def __gt__(self, other):
        return (self.length> other.length)

    def __lt__(self, other):
        return (self.length < other.length)


    def split(self):
        absDist=np.abs(self.values-np.mean(self.values))
        maxIndex=np.argmax(absDist)
        return self.startPos+maxIndex



def getSplitPoints(values,num):
    selected=np.zeros(len(values),dtype=int)

    selectedNum = 0

    lines =[]
    line = Line(0, values)
    if(line.length>5):
        lines.append(line)

    while (len(lines)>0 and selectedNum<num):

        lines=sorted(lines)
        line=lines.pop()
        splitIndex=line.split()

        selected[splitIndex] = 1
        selectedNum = selectedNum + 1


        if splitIndex-line.startPos>=5:
            lineLeft=Line(line.startPos,values[line.startPos:splitIndex])
            lines.append(lineLeft)
        if (line.startPos+line.length)-(splitIndex+1)>=5:
            lineRight=Line(splitIndex+1,values[splitIndex+1:line.startPos+line.length])
            lines.append(lineRight)

    if(selected[0]==0):
        selected[0]=1
    if(selected[len(values)-1]==0):
        selected[len(values) - 1] =1

    splitPoints=[]
    for i in range(len(selected)):
        if(selected[i]==1):
            splitPoints.append(i)


    return splitPoints


if __name__ == '__main__':
    values=np.random.rand(30)
    selected=getSplitPoints(values,5)
    print(selected)



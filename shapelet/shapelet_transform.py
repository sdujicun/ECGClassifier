import sys
import numpy as np
import math
import time
from split.splitpoints import getSplitPoints

class Shapelet:
    def __init__(self,seriesId,startPos,length,values):
        self.seriesId = seriesId     # 序列id
        self.startPos = startPos
        self.length = length     # shapelet长度
        self.values = values    # shapelet值
        self.threshold = -1
        self.gain = float("-inf")   #信息增益
        self.gap= float("-inf")    #separation gap

    def setQualityValue(self,gain,gap,threshold):
        self.gain=gain
        self.gap=gap
        self.threshold=threshold

    def __eq__(self, other):
        return (self.gain == other.gain) and (self.gap ==other.gap)

    def __gt__(self, other):
        return (self.gain > other.gain) or ((self.gain == other.gain) and (self.gap>other.gap))

    def __lt__(self, other):
        return (self.gain < other.gain) or ((self.gain == other.gain) and (self.gap<other.gap))

class OrderLineObj():
    def __init__(self,distance,label):
        self.distance=distance
        self.label=label


    def __eq__(self, other):
        return (self.distance == other.distance)

    def __gt__(self, other):
        return (self.distance> other.distance)

    def __lt__(self, other):
        return (self.distance < other.distance)

class ClassDistribution():
    def __init__(self):
        self.classDictionary={}

    def getEntropy(self):
        p=list(self.classDictionary.values())
        p=p/np.sum(p)
        entropy = 0
        for i in range(len(p)):
            entropy = entropy - p[i] * math.log(p[i], 2)
        return entropy

    def setValueFromLabel(self,labels):
        classes = set(labels)
        for i in iter(classes):
            num = np.sum(labels == i)
            self.classDictionary.update({i:num})

    def size(self):
        return len(self.classDictionary.keys())

def transform(dataset,shapelets):
    instanceNum=len(dataset)
    shapeletNum=len(shapelets)
    features=np.zeros((instanceNum,shapeletNum))
    for j in range(shapeletNum):
        values=shapelets[j].values
        for i in range(instanceNum):
            features[i,j]=getMinDistance(values,dataset[i])

    return features

def findBestKShapeletWithSplitPoints(dataset,label,minLen,maxLen,k):
    classDistribution=ClassDistribution()
    classDistribution.setValueFromLabel(label)
    entropy_all=classDistribution.getEntropy()
    best_K_shapelet=[]
    gain_threshold=float("-inf")
    for seriesId in range(len(dataset)):
        print("time",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("已选shapelet数量", len(best_K_shapelet))
        print("信息增益下限",gain_threshold)
        print("percent", seriesId, "/", len(dataset))

        shapelet_in_series=[]
        timeseries=dataset[seriesId]

        splitPoints=getSplitPoints(timeseries,math.ceil(len(timeseries)/10))
        for i in range(len(splitPoints)-1):
            startPos=splitPoints[i]
            for j in range(i+1,len(splitPoints)):
                endPos=splitPoints[j]
                length=endPos-startPos+1
                '''
                if(length<minLen):
                    continue
                if(length>maxLen):
                    break
                '''

                values=timeseries[startPos:endPos+1]
                shapelet=Shapelet(seriesId,startPos,length,values)
                dist=getAllDistance(shapelet,dataset)
                orderline=[]
                for i in range(len(dist)):
                    orderLineObj=OrderLineObj(dist[i],label[i])
                    orderline.append(orderLineObj)
                orderline=sorted(orderline)

                threshold, gain,gap=getBestSplit(orderline,entropy_all)
                shapelet.setQualityValue(gain,gap,threshold)
                shapelet_in_series.append(shapelet)
        #sort shapelet in series
        shapelet_in_series=sorted(shapelet_in_series,reverse=True)
        # remove similar shapelet
        shapelet_in_series=removeSelfSimilar(shapelet_in_series)
        #combine the best k shapelet
        best_K_shapelet=combine(k,best_K_shapelet,shapelet_in_series)

        if(len(best_K_shapelet)==k):
            gain_threshold=best_K_shapelet[k-1].gain

    return best_K_shapelet

def findBestKShapelet(dataset,label,minLen,maxLen,k):
    classDistribution=ClassDistribution()
    classDistribution.setValueFromLabel(label)
    entropy_all=classDistribution.getEntropy()
    best_K_shapelet=[]
    for seriesId in range(len(dataset)):
        print("time",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        print("percent", seriesId, "/", len(dataset))
        shapelet_in_series=[]
        timeseries=dataset[seriesId]
        for length in range(minLen,maxLen+1):
            for startPos in range(len(timeseries)-length+1):
                values=timeseries[startPos:startPos+length]
                shapelet=Shapelet(seriesId,startPos,length,values)
                dist=getAllDistance(shapelet,dataset)

                orderline=[]
                for i in range(len(dist)):
                    orderLineObj=OrderLineObj(dist[i],label[i])
                    orderline.append(orderLineObj)
                orderline=sorted(orderline)

                threshold, gain,gap=getBestSplit(orderline,entropy_all)
                shapelet.setQualityValue(gain,gap,threshold)
                shapelet_in_series.append(shapelet)
        #sort shapelet in series
        shapelet_in_series=sorted(shapelet_in_series,reverse=True)
        # remove similar shapelet
        shapelet_in_series=removeSelfSimilar(shapelet_in_series)
        #combine the best k shapelet
        best_K_shapelet=combine(k,best_K_shapelet,shapelet_in_series)

    return best_K_shapelet

def combine(k,kBestSoFar,timeSeriesShapelets):
    newBestSoFar = []
    # best so far pointer
    bsfPtr = 0;
    # new time seris pointer
    tssPtr = 0
    for i in range(k):
        if bsfPtr<len(kBestSoFar):
            shapelet1=kBestSoFar[bsfPtr]
        else:
            shapelet1=None
        if tssPtr<len(timeSeriesShapelets):
            shapelet2=timeSeriesShapelets[tssPtr]
        else:
            shapelet2=None
        shapelet1Null = (shapelet1 is None)
        shapelet2Null = (shapelet2 is None)
        #both lists have been explored, but we have less than K elements.
        if (shapelet1Null and shapelet2Null):
            break
        #one list is expired keep adding the other list until we reach K.
        if (shapelet1Null):
            newBestSoFar.append(shapelet2)
            tssPtr=tssPtr+1
            continue
        #one list is expired keep adding the other list until we reach K.
        if (shapelet2Null):
            newBestSoFar.append(shapelet1)
            bsfPtr=bsfPtr+1
            continue
        #if both lists are fine then we need to compare which one to use.
        if shapelet1> shapelet2 :
            newBestSoFar.append(shapelet1)
            bsfPtr=bsfPtr+1
        else:
            newBestSoFar.append(shapelet2);
            tssPtr=tssPtr+1
    return newBestSoFar;

def removeSelfSimilar(shapelet_in_series):
    shapelet_not_similar=[]

    for i in range(len(shapelet_in_series)):
        shapelet=shapelet_in_series[i]

        if not (hasSimilar(shapelet, shapelet_not_similar)):
            shapelet_not_similar.append(shapelet)

    return shapelet_not_similar

def hasSimilar(shapelet,shapelet_not_similar):
    for i in range(len(shapelet_not_similar)):
        candidate=shapelet_not_similar[i]
        if (candidate.startPos >= shapelet.startPos) and (candidate.startPos < shapelet.startPos + shapelet.length):
            # return True
            #candidates is subsequence of shapelet
            if(candidate.startPos+candidate.length)<=(shapelet.startPos + shapelet.length):
                return True
            #the some subsequence is big than half of any one
            similar_length=shapelet.startPos + shapelet.length-candidate.startPos+1
            if(similar_length>shapelet.length/2) or (similar_length>candidate.length/2):
                return True

        if (shapelet.startPos >= candidate.startPos) and (shapelet.startPos < candidate.startPos + candidate.length):
            #return True
            # shapelet is  subsequence of candidates
            if (shapelet.startPos + shapelet.length) <= (candidate.startPos + candidate.length):
                return True
            # the some subsequence is big than half of any one
            similar_length = candidate.startPos + candidate.length - shapelet.startPos + 1
            if (similar_length > shapelet.length / 2) or (similar_length > candidate.length / 2):
                return True

        if (len(shapelet.values)==len(candidate.values)):
            if ((shapelet.values==candidate.values).all()):
                return True
    return False

def getMinDistance(values,timeSeries):
    min=sys.float_info.max
    l1=len(values)
    l2=len(timeSeries)
    for i in range(0,l2-l1+1):
        dist=0.0
        for j in range(0,l1):
            dist=dist+np.square(values[j]-timeSeries[i+j])
            if dist>=min:
                break
        if dist<min:
            min=dist
    return np.sqrt(min/l1)

def getAllDistance(shapelet,dataset):
    values=shapelet.values
    seriesId=shapelet.seriesId
    dist=np.zeros(len(dataset))
    for i in  range(len(dataset)):
        if(i==seriesId):
            dist[i]=0.0
        else:
            dist[i]=getMinDistance(values,dataset[i])
    return dist

def getBestSplit(orderline,entropy_all):
    #for each split point, starting between 0 and 1, ending between end-1 and end
    #addition: track the last threshold that  was used, don't bother if it's the same as the last one
    lastDist = orderline[0].distance #must be initialised as not visited(no point breaking before any data!)
    bsfGain = -1
    threshold = -1

    for i in  range(1,len(orderline)):
        thisDist=orderline[i].distance
        if (i==1) or (thisDist!=lastDist):#check that threshold has moved(no point in sampling identical thresholds)- special case - if 0 and 1 are the same dist

            #count class instances below and above threshold
            lessClasses=ClassDistribution()
            greaterClasses=ClassDistribution()
            sumOfLessClasses = 0
            sumOfGreaterClasses = 0

            # visit those belowthreshold
            for j in range(0,i):
                thisClassVal = orderline[j].label
                storedTotal=1
                if(thisClassVal in lessClasses.classDictionary):
                    storedTotal=storedTotal+lessClasses.classDictionary[thisClassVal]
                lessClasses.classDictionary.update({thisClassVal:storedTotal})
                sumOfLessClasses=sumOfLessClasses+1

            # visit  those above threshold
            for j in range(i,len(orderline)):
                thisClassVal = orderline[j].label
                storedTotal = 1
                if (thisClassVal in greaterClasses.classDictionary):
                    storedTotal = storedTotal + greaterClasses.classDictionary[thisClassVal]
                greaterClasses.classDictionary.update({thisClassVal: storedTotal})
                sumOfGreaterClasses = sumOfLessClasses + 1
            sumOfAllClasses = sumOfLessClasses + sumOfGreaterClasses
            lessFrac = sumOfLessClasses / sumOfAllClasses

            entropyLess = lessClasses.getEntropy()
            greaterFrac = sumOfGreaterClasses / sumOfAllClasses
            entropyGreater = greaterClasses.getEntropy()
            gain = entropy_all - lessFrac * entropyLess - greaterFrac * entropyGreater
            if (gain > bsfGain):
                bsfGain = gain
                threshold = (thisDist - lastDist) / 2 + lastDist
        lastDist = thisDist

    if bsfGain >= 0:
        gap = calculateSeparationGap(orderline, threshold)

    return threshold, bsfGain, gap

def calculateSeparationGap(orderline, threshold):
    sumLeft=0
    leftSize=0
    sumRight=0
    rightSize=0

    for orderlineobj in orderline:
        if orderlineobj.distance<threshold:
            sumLeft=sumLeft+orderlineobj.distance
            leftSize=leftSize+1
        else:
            sumRight=sumRight+orderlineobj.distance
            rightSize=rightSize+1
    if (rightSize==0) or (leftSize==0):
        return -1
    gap=1/rightSize*sumRight-1/leftSize*sumLeft
    return gap



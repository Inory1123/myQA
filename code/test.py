from Mention2ID import Mention2ID
from KnowledgeBase import KnowledgeBase
from similar import Similar
import jieba
import urllib.request
import urllib.parse
import json
import time

def getEntityList(qestion:str,m2id):
    urlPath = 'http://shuyantech.com/api/entitylinking/cutsegment?q='
    urlstr = urlPath+urllib.parse.quote(qestion)

    urlRST = urllib.request.urlopen(urlstr)
    dic = json.loads(urlRST.read().decode('utf-8'))
    entityList = []
    for entity in dic['entities']:
        if len(entity)==2:
            entityList.append(qestion[entity[0][0]:entity[0][1]])

    for entity in entityList:
        queryRST = m2id.queryM2ID(entity)
        if len(queryRST)>0:
            idstrRST = queryRST[0][1]
            entityList = entityList + idstrRST.split(' ')
    entityList = list(set(entityList))

    return (entityList)

def getAnswerList(entityList:list,kb):
    answerList = []
    for entity in entityList:
        answerList = answerList + kb.queryKB(entity)
    return answerList


if __name__ == '__main__':
    similar = Similar()
    m2id = Mention2ID()
    kb = KnowledgeBase()

    while True:
        questionstr = input('question:\n')
        if questionstr == 'end':
            break

        entityList = getEntityList(questionstr,m2id)
        #print(entityList)

        if len(entityList)==0:
            print('查无实体')
            continue

        answerList = getAnswerList(entityList,kb)
        #print(answerList)
        #答案排名
        questionVec = similar.questionEnb(questionstr,usePSEG=True)
        for idx in range(len(answerList)):
            answerVec = similar.answerEnb('|||'.join(answerList[idx][:3]))
            answerList[idx] = answerList[idx] + (similar.vectorS(questionVec,answerVec),)
        answerList.sort(key=lambda element: element[3],reverse=True)
        for answer in answerList[:5]:
            print(answer)
    m2id.close()
    kb.close()



import FilePath
import jieba
import numpy as np
from gensim.models import Word2Vec
import jieba.posseg as pseg


class Similar:
    def __init__(self):
        #loading model
        print('loading model')
        self.model = Word2Vec.load(FilePath.WIKI_WORD2VEC_PATH)
        print('ok')
        self.topic = ['nr','ns','nt','nrt']
        self.attri = ['n','v','r','p']
        self.commom = ['的','是','什么','啥','和']
        self.remove = ['x','w']

    def questionEnb(self,message,usePSEG:bool=True):
        cutRST = pseg.cut(message)
        wvRST = np.zeros(400,dtype=np.float32)
        start = True
        for word,flag in cutRST:
            # print(word,flag)
            if start:
                wvRST = self.getWV(word, flag, usePSEG)
                start = False
            else:
                wvRST = np.vstack((wvRST,self.getWV(word, flag, usePSEG)))
        return np.mean(wvRST,axis=0) if wvRST.ndim==2 else wvRST

    def getWV(self, word, flag, usePSEG:bool):
        wvRST = np.zeros(400, dtype=np.float32)
        try:
            if usePSEG is False:
                return self.model.wv[word] * 1
            if (word in self.commom) or (flag in self.remove):
                return self.model.wv[word] * 0
            if flag in self.attri:
                return self.model.wv[word] * 1.2
            if flag in self.topic:
                return self.model.wv[word] * 0.8
            else:
                return self.model.wv[word] * 1
        except KeyError:
            #print(word, 'not in vocabulary')
            return wvRST

    def answerEnb(self,message:str):
        messages = message.split('|||')
        wvRST = np.zeros(400, dtype=np.float32)
        start = True
        for idx in range(len(messages)):
            if start:
                wvRST = ((idx%2)+0.5)*self.questionEnb(messages[idx])
                start = False
            else:
                wvRST = np.vstack((wvRST,((idx%2)+0.5)*self.questionEnb(messages[idx])))
        return np.mean(wvRST, axis=0) if wvRST.ndim == 2 else wvRST

    def textS(self, text1, text2,usePSEG:bool=True):
        qwv = self.questionEnb(text1,usePSEG)
        awv = self.answerEnb(text2)
        cos_sim = np.dot(qwv, awv) / (np.linalg.norm(qwv) * np.linalg.norm(awv))
        return (cos_sim + 1.0) / 2.0
    def vectorS(self,v1,v2):
        cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return (cos_sim + 1.0) / 2.0


if __name__ == '__main__':
    similar = Similar()
    qwv = similar.setenceEnb('类胡萝卜素的成分有哪些')
    awv1 = similar.setenceEnb('类胡萝卜素性质色素')
    awv2 = similar.setenceEnb('类胡萝卜素识别116-31-4')
    awv3 = similar.setenceEnb('类胡萝卜素包含胡萝卜素和叶黄素')
    awv4 = similar.setenceEnb('类胡萝卜素外文名carotenoid')
    print(qwv.dot(awv1))
    print(qwv.dot(awv2))
    print(qwv.dot(awv3))
    print(qwv.dot(awv4))

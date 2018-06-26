import FilePath
import jieba
import re
import time
import multiprocessing
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


def testWikiCorpus():
    outputFile = open(FilePath.ZH_WIKI_TXT_DATA_PATH, 'w', encoding='utf-8')
    wikiData = WikiCorpus(FilePath.ZH_WIKI_XML_DATA_PATH, dictionary={}, lemmatize=False)
    wikiData.save_corpus('test', WikiCorpus)
    num = 0
    for text in wikiData.get_texts():
        print(text)
    # outputFile.write(text + '\n')
        num = num + 1
        if num == 10:
            break
        # if (num % 10000 == 0):
        #     print("Saved " + str(num) + " articles")

    outputFile.close()
    print("Finished Saved " + str(num) + " articles")


def filter():
    #total linenumber: 14126651
    # skipped: 8988501
    p1 = re.compile('-*[{（(].*[）)}]')
    p2 = re.compile('《》')
    p3 = re.compile('「')
    p4 = re.compile('」')
    p5 = re.compile('<doc (.*)>')
    p6 = re.compile('</doc>')
    p7 = re.compile('\[\[')
    p8 = re.compile('\]\]')
    lineNumber = 0
    skipped = 0
    outfile = open(FilePath.ZH_WIKI_TXT_DATA_PATH , 'w', encoding='utf-8')
    with open(FilePath.ZH_WIKI_EXTRACT_PATH, 'r', encoding='utf-8') as myfile:
        for line in myfile:
            lineNumber = lineNumber + 1
            if lineNumber % 10000 == 0:
                print('Processed', lineNumber, 'lines')
            if len(line)<10 :
                skipped = skipped + 1
                continue
            line = p1.sub('', line)
            line = p2.sub('', line)
            line = p3.sub('', line)
            line = p4.sub('', line)
            line = p5.sub('', line)
            line = p6.sub('', line)
            line = p7.sub('', line)
            line = p8.sub('', line)
            outfile.write(line)
    outfile.close()
    print('total linenumber:',lineNumber)
    print('skipped:', skipped)

def cut_text():
    inputFile = open(FilePath.ZH_WIKI_TXT_DATA_PATH,'r',encoding='utf-8')
    outputFile = open(FilePath.ZH_WIKI_TXT_DATA_CUT_PATH,'w',encoding='utf-8')
    lineNum = 0;
    for line in inputFile.readlines():
        if len(line)<10:
            continue
        cutRST = jieba.cut(line)
        strCutRST = ' '.join(cutRST)
        outputFile.write(strCutRST)
        lineNum = lineNum + 1
        if lineNum % 10000 ==0:
            print('process',lineNum,'lines')
    inputFile.close()
    outputFile.close()

def trainWord2vec():
    #train word2vec used： 2863.67817902565 seconds
    inputPath = FilePath.ZH_WIKI_TXT_DATA_CUT_PATH
    outputPath = FilePath.WIKI_WORD2VEC_PATH
    timeStart = time.time()
    model = Word2Vec(LineSentence(inputPath), size=400, window=5, min_count=5,workers=multiprocessing.cpu_count())
    timeEnd = time.time()
    print('train word2vec used：', timeEnd - timeStart, 'seconds')
    model.save(outputPath)

if __name__ == '__main__':
    trainWord2vec()
    # model = Word2Vec.load(FilePath.WIKI_WORD2VEC_PATH)
    # while True:
    #     instr = input('输入词：\n')
    #     if instr == 'end':
    #         break
    #     rst1 = model.wv[instr]
    #     print(rst1)

import FilePath
import io
import time
import sqlite3


class Mention2ID:
    def __init__(self):

        self.conn = sqlite3.connect('KB.db')
        self.curs = self.conn.cursor()
        self.m2idName = 'mention2id2'

    def creatM2ID(self):
        self.curs.execute('CREATE TABLE '+self.m2idName+'(mention TEXT PRIMARYKEY,id TEXT)')
        self.curs.execute('CREATE INDEX index_mention ON '+self.m2idName+'(mention)')
        self.conn.commit()
        print("数据库创建成功")

    def loadM2ID(self ,M2IDPath=FilePath.MENTION2ID_DIC_PATH):
        #with primary key need 42.2622275352478 seconds
        #with index and primary key need137.4370789527893 seconds
        #total line number: 7623035
        #skipped: 861554
        timeStart = time.time()
        M2IDFile = io.open(M2IDPath,'r',encoding='utf-8')
        lineNumber, skipped = 0, 0
        while True:
        # for idx in range(10):
            line = M2IDFile.readline().rstrip()
            if len(line) == 0:
                break

            lineNumber += 1
            if lineNumber % 100000 == 0:
                print('Processed', lineNumber, 'lines')
            try:
                lineElements = line.split(' ||| ')
                if len(lineElements)==2 and lineElements[0] != lineElements[1] :
                    tempRST = [lineElements[0].replace(' ', ''),lineElements[1].replace('\t', ' ')]
                    self.curs.execute('INSERT INTO '+self.m2idName+' VALUES(?,?)',tempRST)
                else:
                    if len(lineElements)!=2:
                        print(line)
                    skipped += 1
                    continue
            except ValueError:
                skipped += 1
                continue
        self.conn.commit()
        M2IDFile.close()
        print ('total line number:', lineNumber)
        print ('skipped:', skipped)
        timeEnd = time.time()
        print ('Loading mention2id consumed', timeEnd - timeStart, 'seconds')

    def clearM2ID(self):
        self.curs.execute('DELETE FROM '+self.m2idName)
        self.conn.commit()
        print("成功清除表")

    def dropM2ID(self,):
        self.curs.execute('Drop TABLE ' + self.m2idName)
        self.conn.commit()

    def queryM2ID(self,subjectName):
        #query msg
        #primary Key:query time： 0.9943585395812988 seconds
        #index and primary Key:query time： 0.00041866302490234375 seconds
        timeStart = time.time()
        query = 'SELECT * FROM '+self.m2idName+' WHERE mention = ?'
        queryRst = self.curs.execute(query,[subjectName]).fetchall()
        # print(queryRst)
        timeEnd = time.time()
        # print('M2ID query time：', timeEnd - timeStart, 'seconds')
        return queryRst


    def close(self):
        self.conn.close()



if __name__ == '__main__':
    m2id = Mention2ID()
    rst = m2id.queryM2ID('太原')
    print(rst)
    m2id.close()

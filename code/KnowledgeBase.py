import FilePath
import time
import sqlite3
import io

class KnowledgeBase:
    def __init__(self):
        self.conn = sqlite3.connect('KB.db')
        self.curs = self.conn.cursor()
        self.kbName = 'kb2'

    def creatKB(self):
        #kb1 without index
        #kb2 with index
        self.curs.execute('CREATE TABLE '+self.kbName+'(subject TEXT ,attribute TEXT,object TEXT)')
        self.curs.execute('CREATE INDEX index_subject ON '+self.kbName+'(subject)')
        self.conn.commit()

    def loadKB(self ,KBPath=FilePath.KNOWLEDGE_BASE_PATH):
        #without index need 223.07511067390442 seconds
        #with index need 1169.2613544464111 seconds
        timeStart = time.time()
        KBFile = io.open(KBPath,'r',encoding='utf-8')
        lineNumber, skipped = 0, 0
        while True:
            line = KBFile.readline().rstrip()
            if len(line) == 0:
                break

            lineNumber += 1
            if lineNumber % 1000000 == 0:
                print('Processed', lineNumber, 'lines')
            try:
                self.curs.execute('INSERT INTO '+self.kbName+' VALUES(?,?,?)',line.split(' ||| '))

            except ValueError:
                skipped += 1
                continue
        self.conn.commit()
        KBFile.close()
        print ('total line number:', lineNumber)
        print ('skipped:', skipped)
        timeEnd = time.time()
        print ('Loading knowledge base consumed', timeEnd - timeStart, 'seconds')

    def clearKB(self):
        self.curs.execute('DELETE FROM '+self.kbName)
        self.conn.commit()

    def dropKB(self,kbName):
        self.curs.execute('Drop TABLE ' + self.kbName)
        self.conn.commit()

    def queryKB(self,subjectName):
        #query msg
        #without primary Key:query time： 5.509960651397705 seconds
        #with idx:query time： 0.0008268356323242188 seconds
        timeStart = time.time()
        query = 'SELECT * FROM '+self.kbName+' WHERE subject = ?'
        queryRst = self.curs.execute(query,[subjectName]).fetchall()
        # print(queryRst)
        timeEnd = time.time()
        # print('KB query time：', timeEnd - timeStart, 'seconds')
        return queryRst


    def close(self):
        self.conn.close()



if __name__ == '__main__':
    kb = KnowledgeBase()
    rst = kb.queryKB('红楼梦')
    print(rst)
    kb.close()

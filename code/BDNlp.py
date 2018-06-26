from aip import AipNlp
from Mention2ID import Mention2ID
from KnowledgeBase import KnowledgeBase
from similar import Similar
import jieba
import time

""" 你的 APPID AK SK """
APP_ID = '11435194'
API_KEY = '5UvM2LWUAG84EPG7HtpolDSV'
SECRET_KEY = 'gDRB6dhYyHCUl74SYp9QyTnk6dHIoG6E'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
client.setConnectionTimeoutInMillis(3000)
client.setSocketTimeoutInMillis(3000)

""" 如果有可选参数 """
options = {}
options["model"] = "GRNN"

m2id = Mention2ID()
kb = KnowledgeBase()

# while True:
#     questionstr = input('question:\n')
#     if questionstr == 'end':
#         break
#     querystr = input('entity:\n')
#
#     entitymsg = kb.queryKB(querystr)
#     if len(entitymsg) == 0:
#         print('查无实体')
#         continue
#     for idx in range(len(entitymsg)):
#         score = client.simnet(questionstr, ' '.join(entitymsg[idx][:2]),options)['score']
#         time.sleep(0.2)
#         entitymsg[idx] = entitymsg[idx] + (score,)
#     entitymsg.sort(key=lambda element: element[3], reverse=True)
#     print(entitymsg)
# m2id.close()
# kb.close()


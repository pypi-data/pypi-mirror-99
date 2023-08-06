from udpipe_parser import *
P = UDPipeParser()
text = 'я сказал ребятам идти прочь!'

q = P.run(text,logging=True,solve_anaphora=True)
for q_i in q:
    print(q_i)
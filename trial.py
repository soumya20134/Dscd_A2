cLogTerm =  6
lastTerm = 4
cLogLength = 5
log = [1,2,3]


logOk = (cLogTerm>lastTerm) or ((cLogTerm == lastTerm) and (cLogLength >= len(log)))
print(logOk)

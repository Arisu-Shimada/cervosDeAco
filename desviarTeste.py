motor(-1,-1)
time.sleep(0.1)
motor(1,-1)
time.sleep(0.7)
motor(0,1)
while True:
    if(verificacao == True):
        break
    if(sensor2 == 1):
        motor(1,1)
        time.sleep(0.3)
        while True:
            if(sensor2 == 1):
                break
            motor(1,-1)
        verificacao = True
verificacao = False
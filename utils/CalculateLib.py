import time
import pprint

def bruteCal(takenNode, program, node):
    i = 0
    time = 0
    tempDamage = 0
    preGuardianBuffer = 0
    while True:
        for j in program:
            tempDamage = program[j]['damage']
            if time >= program[j]['installTime']:
                program[j]['localCounter'] += 0.1
            if program[j]['localCounter'] == max(program[j]['interval'] - program[j]['projectileTime'], 0.1):
                if program[j]['mode'] == 'single':
                    for k in node:
                        if node[k]['firewall'] > 0:
                            tempDamage = program[j]['damage']
                            for l in node[k]['guardians']:
                                if node[k]['guardians'][l][1] == time:
                                    node[k]['guardians'][l][0] = node[k]['guardians'][l][2] #reset guardian shield
                                if node[k]['guardians'][l][0] > 0:
                                    node[k]['guardians'][l][1] = time + 7 #reset guardian shield delay
                                if tempDamage <= 0:
                                    continue
                                preGuardianBuffer = node[k]['guardians'][l][0]
                                node[k]['guardians'][l][0] -= tempDamage
                                tempDamage = max(tempDamage - preGuardianBuffer, 0)
                            node[k]['firewall'] -= tempDamage
                            break
                elif program[j]['mode'] == 'multi':
                    for k in node:
                        if node[k]['firewall'] > 0:
                            tempDamage = program[j]['damage']
                            for l in node[k]['guardians']:
                                if node[k]['guardians'][l][1] == time:
                                    node[k]['guardians'][l][0] = node[k]['guardians'][l][2] #reset guardian shield
                                if node[k]['guardians'][l][0] > 0:
                                    node[k]['guardians'][l][1] = time + 7 #reset guardian shield delay
                                if tempDamage <= 0:
                                    continue
                                preGuardianBuffer = node[k]['guardians'][l][0]
                                node[k]['guardians'][l][0] -= tempDamage
                                tempDamage = max(tempDamage - preGuardianBuffer, 0)
                        node[k]['firewall'] -= tempDamage
                    if node[k]['stunCounter'] 
                            
        time += 0.1
        
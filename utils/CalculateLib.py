import time
import pprint
import json

def bruteCal(takenNode, program, node):
    i = 0
    time = 0
    tempDamage = 0
    preGuardianBuffer = 0
    fallenNode = 0
    while True:
        if takenNode['firewall'] <= 0:
            return [time, "TakenNode//Retaken",takenNode['firewall']]
        if fallenNode == len(node):
            return [time, "TakenNode//Success",takenNode['firewall']]
        fallenNode = 0
        if time >= 180:
            time = 180
            return [time, "Time//Impossible",takenNode['firewall']]
        for j in program:
            tempDamage = program[j]['damage']
            if time >= program[j]['installTime']:
                program[j]['localCounter'] += 0.1
            if program[j]['localCounter'] == max(program[j]['interval'] - program[j]['projectileTime'], 0.1):
                tempDamage = program[j]['damage']
                for k in node:
                    if node[k]['firewall'] <= 0:
                        node[k]['firewall'] = 0
                        fallenNode += 1
                        print(fallenNode)
                        continue
                    if node[k]['firewall'] > 0:
                        if program[j]['mode'] == 'multi':
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
                    if program[j]['stun'] != 0:
                        node[k]['stunCounter'] = time + program[j]['stun']
                    if node[k]['stunCounter'] <= time:
                        node[k]['firewall'] += node[k]['firewall'] / 1000 * node[k]['regen'] 
                program[j]['localCounter'] = 0
        for k in node:
            if node[k]['nodeCounter'] == max(node[k]['interval'] - node[k]['projectileTime'], 0.1):
                for n in takenNode['defProg']:
                    takenNode['defProg'][n][0] += takenNode['defProg'][n][0] / 100 * takenNode['defProg'][n][1]
                    takenNode['defProg'][n][0] -= node[k]['DPS']
                    if node[k]['sentryCounter'] == 1:
                        takenNode['defProg'][n][0] -= node[k]['sentryDPS']
                        node[k]['sentryCounter'] = 0
                    node[k]['nodeCounter'] = 0
                    if takenNode['defProg'][n][0] <= 0:
                        takenNode['defProg'].pop(n)
                if len(takenNode['defProg']) == 0:
                    takenNode['firewall'] -= node[k]['DPS']
                    if node[k]['sentryCounter'] == 1:
                        takenNode['firewall'] -= node[k]['sentryDPS']
                        node[k]['sentryCounter'] = 0
                node[k]['nodeCounter'] = 0
        time += 0.1
        print(takenNode['firewall'], end= f"       {node['1']['firewall']}\n")
        #if time >= 180:
        #    return [time, 'Time//Impossible', takenNode['firewall'], node[0]['firewall']]
        
if __name__ == '__main__':
    takenNode = json.loads(input())
    node = json.loads(input())
    program = json.loads(input())
    print(bruteCal(takenNode, program, node))
    

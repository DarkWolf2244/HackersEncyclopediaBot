import time
import pprint

def bruteCal(takenNode, program, node):
    i = 0
    time = 0
    tempDamage = 0
    preGuardianBuffer = 0
    while True
        for j in program:
            tempDamage = program[j]['damage']
            if time >= program[j]['installTime']:
                program[j]['localCounter'] += 0.1
            if program[j]['localCounter'] == max(program[j]['interval'] - program[j]['projectileTime'], 0.1):
                tempDamage = program[j]['damage']
                for k in node:
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
                        node[k]['firewall'] += node[k]['firewall'] / 100 * node[k]['regen']
                if len(node) == 0:
                    return [time, "TakenNode//Success"]
        if takenNode['firewall'] <= 0:
            return [time, "TakenNode//Retaken"]
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
                    if node[k]['sentryCounter'] = 1:
                        takenNode['firewall'] -= node[k]['sentryDPS']
        time += 0.1
        if time >= 180:
            return [time, 'Time//Impossible']
        

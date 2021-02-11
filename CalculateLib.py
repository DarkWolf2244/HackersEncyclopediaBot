import json
import concurrent.futures


def bruteCal(progDamage, progInstallTime, progHitInterval, progProjectileTime, progAmount, isProgMulti, nodeFirewall, nodeRegeneration, nodeAmount):
    firewall = nodeFirewall
    regen = nodeRegeneration
    time = progInstallTime
    i = 0
    if int(progAmount) <= 0:
        return None
    if isProgMulti == 0:
        for x in range(1,int(nodeAmount)+1):
            while True:
                if firewall <= 0:
                    break
                i += 0.1
                if i == max(progHitInterval - progProjectileTime, 0.1):
                    if (progDamage * int(progAmount)) / 10 > (firewall / 100 * regen) / 10 :
                        firewall -= progDamage * int(progAmount) / 10 
                    else:
                        return None
                    i = 0
                firewall += (firewall / 100 * regen) / 10 
                time += 0.1
                if time > 10000:
                    return time
            firewall = nodeFirewall
    elif isProgMulti == 1:
        while True:
            if firewall <= 0:
                break
            i += 0.1
            if i == max(progHitInterval - progProjectileTime, 0.1):
                if (progDamage * int(progAmount)) / 10 > (firewall / 100 * regen) / 10 :
                    firewall -= progDamage * int(progAmount) / 10
                else:
                    return None
                i = 0
            firewall += (firewall / 100 * regen) 
            time += 0.1
            if time > 10000:
                return time
    return time
      
     
def stealthCalMT(visibilityboost, stealthProgVisibility, stealthProgInstallTime):
    time = 0
    i = 0
    while i < stealthProgInstallTime:
        time += 20
        time += (stealthProgVisibility / 100 * visibilityboost)
        i += 1
    return time    





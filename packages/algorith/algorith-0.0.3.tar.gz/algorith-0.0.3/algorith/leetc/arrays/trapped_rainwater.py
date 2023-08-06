import numpy as np


def trapped_rainwater(arr_tank):
    """
    The elements of the array are heights of walls.
    If it rains, how much rain water will be trapped?
    I will answer this question for any array you give me.
    """
    prev_ht = arr_tank[0]
    drops = []
    goingdown=True
    area = 0
    for ht in arr_tank[1:]:
        for i in range(len(drops)):
            drops[i]+=1
        if ht < prev_ht:
            #if not goingdown:
            #    drops = []
            goingdown=True
            for _ in range(prev_ht-ht):
                drops.append(0)
        elif ht > prev_ht:
            goingdown=False
            for _ in range(ht-prev_ht):
                if len(drops)>0:
                    area += drops.pop()
        prev_ht = ht
        print(str(drops))
    return area


if __name__=='__main__':
    trapped_rainwater([5,2,1,2,1,5])


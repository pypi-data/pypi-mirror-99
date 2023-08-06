import numpy as np

#This can be memorized so that a vertex seen in previous path is saved.
def max_wt_path_recurse(adj_lst, wt_lst, i, j):
    if i==j:
        return 0
    if len(adj_lst[i])==0:
        return -np.inf
    else:
        maxx = 0; maxx_ix=-1
        for ix in range(len(adj_lst[i])):
            cand = wt_lst[i][ix]+\
                max_wt_path_recurse(adj_lst,wt_lst,adj_lst[i][ix],j)
            if cand > maxx:
                maxx = cand
                maxx_ix=adj_lst[i][ix]
        print("Go from " + str(i) + " to: " + str(maxx_ix))
        return maxx


def tst():
    adj_lst = [[1,2],
                [3,4],
                [5,8],
                [5,6],
                [3,6,9],
                [6,7],
                [],[],[],[]]
    wt_lst = [[2,5],
                [7,1],
                [1,4],
                [1,1],
                [3,9,1],
                [4,6],
                [],[],[],[]]
    res = max_wt_path_recurse(adj_lst, wt_lst, 0, 6)
    print(res)


if __name__=="__main__":
    tst()

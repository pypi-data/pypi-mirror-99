import numpy as np
import algorith.clr_book.ch12_binary_srch_trees.tree as tr 


## Per fig 15.9, q is 0 indexed while p is 1 indexed.
# This is why 1 will be subtracted from p's indices 
# but not q's. 
def opt_bst_recurse(p,q,i,j):
    w=0
    for l in range(i,j+1):
        w+=p[l-1]#p[l] if p were 1 indexed.
    for l in range(i-1,j+1):
        w+=q[l]
    if j==i-1:
        return q[i-1]
    else:
        minn = np.inf
        for r in range(i,j+1):
            trm = opt_bst_recurse(p,q,i,r-1)+\
                opt_bst_recurse(p,q,r+1,j)+w
            if trm<minn:
                minn=trm
        return minn


def opt_bst_top_dwn_strt(p,q):
    n=len(p)
    ## e is 1 to n+1, 0 to n.
    e = np.ones((n+2,n+1))*np.inf
    w = np.zeros((n+2,n+1)).astype(int)
    root = np.zeros((n+2,n+1)).astype(int)
    return opt_bst_top_dwn(p,q,1,len(p),e,w,root)


def opt_bst_top_dwn(p,q,i,j,e,w,root):
    if e[i,j]<np.inf:
        return e[i,j], w, root
    w1=0
    for l in range(i,j+1):
        w1+=p[l-1]#p[l] if p were 1 indexed.
    for l in range(i-1,j+1):
        w1+=q[l]
    w[i,j] = w1
    if j==i-1:
        e[i,j] = q[i-1]
    else:
        e[i,j] = np.inf
        for r in range(i,j+1):
            trm = opt_bst_top_dwn(p,q,i,r-1,e,w,root)[0]+\
                opt_bst_top_dwn(p,q,r+1,j,e,w,root)[0]+w1
            if trm<e[i,j]:
                e[i,j]=trm
                root[i,j] = r
    return e[i,j], w, root


def create_tree(root,i,j):
    if j<=i-1:
        node = tr.TreeNode("d"+str(i-1),None,None)
    else:
        node = tr.TreeNode("k"+str(root[i,j]),None,None)
        node.left = create_tree(root,i,root[i,j]-1)
        node.right = create_tree(root,root[i,j]+1,j)
    return node


def walk_preorder(tn,parent=None,left=True):
    if tn is not None:
        if parent is None:
            print(str(tn.key) + " is the root")
        elif left:
            print(str(tn.key) + " is the left child of " + str(parent.key))
        else:
            print(str(tn.key) + " is the right child of " + str(parent.key))
        walk_preorder(tn.left,tn,True)        
        walk_preorder(tn.right,tn,False)


if __name__=="__main__":
    p=np.array([.15,.1,.05,.1,.2])
    q=np.array([.05,.1,.05,.05,.05,.1])
    res = opt_bst_recurse(p,q,1,len(p))
    print(res)
    e,w,root=opt_bst_top_dwn_strt(p,q)
    print(e)
    print(root)
    r_node = create_tree(root,1,len(p))
    # You can put a break point here and verify the tree is
    # the same as fig 15.9-b.
    walk_preorder(r_node)


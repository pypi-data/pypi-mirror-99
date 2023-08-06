import numpy as np
from typing import List

## Read the solution before attempting.

class Solution:
    def longestPalindrome(self, s: str) -> str:
        return max_palindrome(s)

def max_palindrome_centered_at(ss,i,j):
    """
    The maximal palindrome in string ss,
    centered at the index between
    i and j. If i and j are the same, then
    this becomes the index.
    """
    if j==i+1:
        l_ix = i; r_ix = j
    elif j==i:
        l_ix=r_ix=i
    else:
        raise Exception("Invalid indice arguments paased.")
    while l_ix>=0 and r_ix<=len(ss)-1 and ss[l_ix]==ss[r_ix]:
        l_ix-=1; r_ix+=1
    return ss[l_ix+1:r_ix]


def max_palindrome(ss):
    max_len=0; max_palindr=""
    for i in range(len(ss)):
        s_r = max_palindrome_centered_at(ss,i,i)
        if len(s_r)>max_len:
            max_len=len(s_r)
            max_palindr = s_r
        if i<len(ss)-1:
            s_r = max_palindrome_centered_at(ss,i,i+1)
            if len(s_r)>max_len:
                max_len=len(s_r)
                max_palindr = s_r
    return max_palindr


if __name__=="__main__":
    ss = "abcdcba"
    s_r = max_palindrome_centered_at(ss,3,3)
    print(s_r)
    s_r = max_palindrome_centered_at(ss,0,0)
    print(s_r)
    s_r = max_palindrome(ss)
    print(s_r)
    s_r = max_palindrome("cbbd")
    print(s_r)
    s_r = max_palindrome_centered_at("cbbd",1,2)
    print(s_r)


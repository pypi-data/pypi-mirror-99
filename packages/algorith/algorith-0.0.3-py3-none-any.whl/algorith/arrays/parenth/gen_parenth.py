import numpy as np

# Whiteboard: https://wbd.ms/share/v2/aHR0cHM6Ly93aGl0ZWJvYXJkLm1pY3Jvc29mdC5jb20vYXBpL3YxLjAvd2hpdGVib2FyZHMvcmVkZWVtLzk4ZjBjYzM3OTc1MzQ3YjY5ZTQ4OTA3MjYxODIxN2Y0X0JCQTcxNzYyLTEyRTAtNDJFMS1CMzI0LTVCMTMxRjQyNEUzRA==


def print_paths(n, start, end, arr):
    """
    We leverage the bijection between Catalan paths
    and valid parenthesizations. start and end are the
    coordinates of the starting and ending points in the
    Catalan paths.
    Note that end never changes, so passing it to the function
    is redundant. Also, n never changes.
    """
    # one less on the x-coordiate and one more on
    # the y-coordinate, means we're one step away
    # from end point. We could also check for start[1]-end[1]==1
    # but the abs makes it not specific to paths above the grid
    if start[0]==end[0]-1 and abs(start[1]-end[1])==1:
        arr.append(')')
        print(''.join(arr))
    ## This means we're at the peak (n,n).
    # We can never let the sum of the x and y-coordinates
    # exceed 2n. This ensures we stay within the square boundary
    # of the grid. We can never cross the line x=y by design.
    # the condition ensure we also never cross 
    # x+y=2n, the other boundary.
    elif sum(start)==2*n:
        # Since we're at the peak, must move down.
        arr.append(')')
        start+=np.array([1,-1])
        print_paths(n,start,end,arr)
    # If we've touched the x-axis, we move up.
    ## this is specific to Catalan paths.
    elif start[1] == 0:
        # Must move up now.
        arr.append('(')
        start+=np.array([1,1])
        print_paths(n,start,end,arr)
    ## If within all boundaries, move up and also move down.
    else:
        arr_up = arr.copy()
        arr_down=arr.copy()
        arr_up.append('(')
        start1=start+np.array([1,1])
        print_paths(n,start1,end,arr_up)
        arr_down.append(')')
        start2=start+np.array([1,-1])
        print_paths(n,start2,end,arr_down)


def valid_parenth(n):
    start=np.array([0,0])
    end=np.array([2*n,0])
    arr=[]
    print_paths(n,start,end,arr)


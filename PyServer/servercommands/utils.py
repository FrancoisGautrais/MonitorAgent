
#
#  opt = {
#       NOM_ARG: ([-a, -A], DEAFULT),
#       NOM_ARG_2: [0]
#  }
def parse_args(args, opt):
    arr=[]
    param={}
    n=len(args)
    for i in opt:
        param[i]=opt[i][1]

    for k in opt:
        p=opt[k][0]
        if isinstance(p, (str, int)):
            opt[k]=([p], opt[k][1])

    i=0
    while i<n:
        p=args[i]
        found=False
        for k in opt:
            if p in opt[k][0]:
                if i+1<n:
                    i+=1
                    param[k]=args[i]
                    found=True
                    break
        if not found:
            arr.append(args[i])
        i+=1

    for i in range(len(arr)):
        for k in opt:
            if i in opt[k][0]:
                param[k]=arr[i]
                break
    print(param)
    print(arr)
    return arr, param

def tribonacci(signature,n):
    if n <= 3:
        return signature[:n]
    else:
        result = [i for i in signature]
        i=0
        while i<n-3:
            next_item = sum(signature)
            result.append(next_item)
            signature.append(next_item)
            signature.pop(0)
            i = i+1
        return result


def tribonacci(s, n):
    for i in range(3, n): s.append(s[i-1] + s[i-2] + s[i-3])
    return s[:n]

def tribonacci(s, n):
    for i in range(3, n): s.append(sum(s[-3:]))
    return s[:n]

def tribonacci(signature,n):
    signature.extend(sum(signature[-3:]) for i in range(3, n))
    return signature[:n]

def tribonacci(signature,n):
    a,b,c = signature
    result = []
    for i in range(n):
        result.append(a)
        a,b,c = b,c,a+b+c
    return result

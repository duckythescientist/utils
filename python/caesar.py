caesar_lambda = lambda w,n: "".join(chr((ord(x.upper())+n-ord("A"))%26+ord("A")) if ord(x.upper()) in range(ord("A"), ord("Z")+1) else x for x in w)

def caesar(w, shift=13):
    n = ""
    for l in w:
        if l.islower():
            n += chr((ord(l)-ord('a')+shift)%26 + ord('a'))
        else if l.isupper():
            n += chr((ord(l)-ord('A')+shift)%26 + ord('A'))
        else:
            n += l
    return n

def simple_caesar(w, shift=13):
    return caesar_lambda(w, shift)
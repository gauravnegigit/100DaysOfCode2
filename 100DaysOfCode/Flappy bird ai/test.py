def prime():
    a = 2 

    while True :
        flag = 0 
        for i in range(2 , a // 2 + 1) :
            if a % i == 0 :
                flag = 1 
                break 
        
        if flag == 0 :
            yield a 
        
        a += 1

def test(func):
    num = int(input("ENTER THE NUMBER OF PRIME NUMBERSS YOU WANT TO PRINT : "))

    for i , val in enumerate(func):
        if i == num :
            quit()
        
        print(val)

test(prime())
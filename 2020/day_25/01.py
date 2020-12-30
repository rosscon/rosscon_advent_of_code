

cardPub = 5764801
doorPub = 17807724

cardPub = 4707356
doorPub = 12092626

n = 1
loop_size = 0

while n != cardPub:
    n = (n * 7) % 20201227
    loop_size += 1

print(pow(doorPub, loop_size, 20201227))
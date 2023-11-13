import tracemalloc
import sys

tracemalloc.start()

x = []
for i in range(10):
    print(i)
    x.append('a')

snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics('lineno')
print(sys.getsizeof(x))


with open('/home/jeffisteddy/Documents/school/5AHIT/ITPP/HandsOn/backend-leikauf/HandsOn-Backend/pyenv/test.debug.txt', '+a') as FO:
    FO.write(str(x) + '\n')
    for i in stats:
        FO.write(str(i))
        FO.write('\n\n')
    print('Wrote data...')



print(stats)
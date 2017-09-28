from hw01heat import hw01heat
from hw01matrix import hw01matrix
from hw01gears import hw01gears

scores = [hw01gears, hw01heat, hw01matrix]
for d in scores:
    acc = 0
    for key, value in d.items():
        if value == 0:
            acc += 1
    print (acc)

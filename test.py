dict = {
    "a": (10, [1, 2, 3, 4, 5])
}

count, _ = dict["a"]
count += 1
nV = (count, _)

print(nV)
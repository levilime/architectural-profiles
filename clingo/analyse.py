f= open("analyse.txt","r")

d = {}

for line in f:
    name = line.split("(")[0]
    if name in d:
        d[name] += 1
    else:
        d[name] = 1

f.close()
ll = ((name, d[name]) for name in d)

f = open("result.txt","w+")
for e in sorted(ll, key=lambda t: t[1], reverse=True):
    f.write(f"{str(e[0])}, {str(e[1])}\n")
f.close()


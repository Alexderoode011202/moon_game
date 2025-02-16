class Test:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return f"test:{self.num}"
    
    def __repr__(self):
        return f"test:{self.num}"
a = Test(1)
b = Test(2)
c = Test(3)


d = {a: b}

b.num += 1
print(b)
print(d)

print({a,c} == {c,b})

print({a, c} in [{a, b}, {c, a}])
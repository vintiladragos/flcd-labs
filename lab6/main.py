from recursive_descentant import RecursiveDescendant
from lab5 import grammar
gram = grammar.Grammar("gtest.txt")
rd = RecursiveDescendant(gram)


a = ("exp adv exp adv exp mi at mi at adv adv exp mi at mi at adv mi back at back back at back at adv exp mi at mi at "
     "adv adv exp mi at mi at adv success")


a_split = a.split()

for i in range(len(a_split)):
    if a_split[i] == "exp":
        rd.expand()
    elif a_split[i] == "adv":
        rd.advance()
    elif a_split[i] == "mi":
        rd.momentary_insuccess()
    elif a_split[i] == "back":
        rd.back()
    elif a_split[i] == "at":
        rd.another_try()
    elif a_split[i] == "success":
        rd.success()
    else:
        print("error")


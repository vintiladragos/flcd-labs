from recursive_descentant import RecursiveDescendant
from lab5 import grammar
gram = grammar.Grammar("gtest.txt")
rd = RecursiveDescendant(gram)
"""
simulating input w=b on gtest.txt
"""
rd.expand()
rd.momentary_insuccess()
rd.another_try()
rd.momentary_insuccess()
rd.another_try()
rd.momentary_insuccess()
rd.another_try()
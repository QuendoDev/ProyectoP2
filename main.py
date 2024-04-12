import setup.initial_conditions as ic
import anim.animation as an

s = ic.s.copy()
T = ic.T
an.make_anim(T, s)

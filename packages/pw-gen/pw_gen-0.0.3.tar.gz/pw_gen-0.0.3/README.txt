A library for generating secure randomised passwords.


Usage (Simple password):
---------------------------------------------------
from pw_gen import Simple

var = Simple(20)

print(var.generate(3))
print(var.return_result(1))
---------------------------------------------------


Usage (Complex password):
---------------------------------------------------
from pw_gen import Complex

var = Complex(20, 'both', True, False)

print(var.generate(3))
print(var.return_result(1))
---------------------------------------------------


Usage (Memorable password):
---------------------------------------------------
from pw_gen import Memorable

var = Memorable(True)

print(var.generate(3))
print(var.return_result(1))
---------------------------------------------------

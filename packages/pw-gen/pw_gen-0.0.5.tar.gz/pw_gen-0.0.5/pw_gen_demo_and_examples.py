from pw_gen import Simple, Complex, Memorable, Pin

# ---------------------------------------------------------------------------- #
# ----------------------------Simple-Password-Tests--------------------------- #
# ---------------------------------------------------------------------------- #

password1 = Simple(20, 'abcdefghijklmnopqrstuvwxyz0123456789')
print(password1.generate(3))
print(password1.return_result(1))
password1.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['j81j14nujfaeit3fppkd', 'tn1m6qbg7vrt11a71qsr', 'k54s1ix3x7vku4vympno']
# tn1m6qbg7vrt11a71qsr
# ---------------------------------OUTPUT------------------------------------- #

password1 = Simple(20, 'abcdefghijklmnopqrstuvwxyz0123456789')
print(password1.generate(3))
print(password1.return_result(1))
password1.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['sfmraiaimdrl743o7z5j', '2e2m2qr6e4jd03hev4fd', 'j6l45ojcjfjude71ghy9']
# 2e2m2qr6e4jd03hev4fd
# ---------------------------------OUTPUT------------------------------------- #




# ---------------------------------------------------------------------------- #
# ---------------------------Complex-Password-Tests--------------------------- #
# ---------------------------------------------------------------------------- #

password2 = Complex(20, 'lower', False, True)
print(password2.generate(3))
print(password2.return_result(1))
password2.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['/$i=pigz/b[b`rr`+\\_g', ']z^cwe.o;@jvo;k+"zaa', "ovi@?]ttt'_\\f:j=+#*p"]
# ]z^cwe.o;@jvo;k+"zaa
# ---------------------------------OUTPUT------------------------------------- #

password2 = Complex(20, 'upper', True, False)
print(password2.generate(3))
print(password2.return_result(1))
password2.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['LSK0OU29NJCA93FPPK9D', 'SYCEEJJI1WURUZC42I43', 'VHJY8CTELMMOUZNSEB0N']
# SYCEEJJI1WURUZC42I43
# ---------------------------------OUTPUT------------------------------------- #

password2 = Complex(20, 'both', True, True)
print(password2.generate(3))
print(password2.return_result(1))
password2.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['G+dLU[+N;K&:r.CEf?k2', 'Bi27W4L41Zq6S[vlVya\\', '9("KF5#;H>[W"p77>uI{']
# Bi27W4L41Zq6S[vlVya\
# ---------------------------------OUTPUT------------------------------------- #



# ---------------------------------------------------------------------------- #
# -------------------------Memorable-Password-Tests--------------------------- #
# ---------------------------------------------------------------------------- #

password3 = Memorable()
print(password3.generate(3))
print(password3.return_result(1))
password3.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['PelicanDaffy5333', 'SidewalkRetrofitting685', 'TramwaySuppressor816']
# SidewalkRetrofitting685
# ---------------------------------OUTPUT------------------------------------- #

password3 = Memorable(True)
print(password3.generate(3))
print(password3.return_result(1))
password3.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['ShayHarvey097', 'ToggingConfect1648', 'HaloBernini219']
# ToggingConfect1648
# ---------------------------------OUTPUT------------------------------------- #

password3 = Memorable(False)
print(password3.generate(3))
print(password3.return_result(1))
password3.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['AcculturateProtagonist', 'UnderclassmenFiddle', 'EverymanIntimacy']
# UnderclassmenFiddle
# ---------------------------------OUTPUT------------------------------------- #




# ---------------------------------------------------------------------------- #
# ---------------------------Pin-Password-Tests------------------------------- #
# ---------------------------------------------------------------------------- #

password4 = Pin(4)
print(password4.generate(3))
print(password4.return_result(1))
password4.clear_results()

# ---------------------------------OUTPUT------------------------------------- #
# ['4854', '5587', '1374']
# 5587
# ---------------------------------OUTPUT------------------------------------- #

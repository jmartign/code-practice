import dis

s = open('scope01.py').read()
co = compile(s, 'scope01.py', 'exec')
print dis.dis(co)


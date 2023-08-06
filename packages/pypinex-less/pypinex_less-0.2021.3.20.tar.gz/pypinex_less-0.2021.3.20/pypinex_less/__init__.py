


__version__ = "0.2021.3.20"



from .LessC import LessC

def lessc(minify:bool = False):
	return LessC(minify)
#
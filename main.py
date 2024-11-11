from mazelib import Maze
from mazelib.generate.Prims import Prims

N = 20
m = Maze ( )
m.generator = Prims ( int (N/ 2 ) , int (N/ 2))
m. generate()
m.generate_entrances( True , True )

print(m)

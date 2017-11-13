import numpy as np
import numpy.random as npr
prob1 = np.array( range( 7575,7642 ) )
prob2 = np.array( range( 5050,5098 ) )
vals = np.zeros( (18*40,4),dtype=np.int16 )
for i in range( len(vals) ):
    vals[ i,0:2 ] = ( npr.choice( prob1, size=(2,), replace=False ) )
    vals[ i,2: ]  = ( npr.choice( prob2, size=(2,), replace=False ) )
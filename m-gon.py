from lib import *
import time

m=8

def PolygonRelation(m):
	r = list(range(1,m+1))
	return ReducedPathRelation(nx.cycle_graph(r), r, r)

start_time = time.time()
rel = PolygonRelation(m)
end_time = time.time()

print(rel)
print('m={}'.format(m))
print('length of the relation: {}'.format(len(rel),len(rel)//4))
print('expected length: 4+(m-4)*2^(m-1)={}'.format(4+(m-4)*(2**(m-1))))
print('computed in {} seconds'.format(end_time-start_time))

from lib import *
import time

m=12

#def PolygonRelation(m):
#	r = list(range(1,m+1))
#	return ReducedPathRelation(nx.cycle_graph(r), r, r)

#start_time = time.time()
#rel = PolygonRelation(m)
#end_time = time.time()
#print('rel={}, m={}'.format(rel,m))

r = list(range(1,m+1))
G = nx.cycle_graph(r)

print('presenting the commutator subgroup in the RACG for the {}-cycle.'.format(m))
print('the generators:')
#print(*ListGens(G),sep='\n')

print('computing the relation... ', end='', flush=True)
start_time = time.time()
rel = ReducedPathRelation(G,r,r)
end_time = time.time()

print('computed: the relation is')
print(str(rel))

##a self-check
#print('does the relation hold? verifying... ', end='', flush=True)
#is_a_relation = IsARelation(rel, G)
#print(is_a_relation)

print('length of the relation: {}'.format(len(rel),len(rel)//4))
print('expected length: 4+(m-4)*2^(m-1)={} (where m={})'.format(4+(m-4)*(2**(m-1)), m))
print('relation computed in {} seconds.'.format(end_time-start_time))

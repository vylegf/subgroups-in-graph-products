import networkx as nx

#------------------------------------------------------------------------
# Provided a simple graph $Г$ and a simplicial loop $l$ in $Г$, this library
# allows to compute the relation $Red(R(l))$ between the Li Cai's generators
# for the right-angled Coxeter group $RC'_Г$.
#
#
# The code below computes the single relation in the case of m-gon.
# It was used to verify the claim that the obtained presentation of the
# group RC'_Г, which is a surface group of genus g(m)=1+(m-1)2^(m-3),
# is a one-relator presentation with the relation of length exactly 4g(m).
# (see Remark 4.15(?) in Subsection 4.4)
#------------------------------------------------------------------------

#An instance of Gen corresponds to either L(i,J) or its inverse,
#where J < V is a set and i\in J.
#Example: L(3,1358)=g1g3g5g8*g3*g8g5g1 is stored as
#elem = 3, amb_set=set([1,3,5,8]), inverted=0
#while L(3,1358)^-1 has inverted=1
class Gen:
	__slots__ = ['elem', 'amb_set', 'inverted']

	def __init__(self, *args):
		if len(args) == 0:
			print('error: zero arguments in Gen.__init__()')
			return

		#constructing from scratch
		#example: command "a=Gen(3,set([1,3,5,8]),1)"
		#gives a==$L(3,1358)^-1$
		if len(args) == 3:
			self.elem, self.amb_set, self.inverted = args
			self.amb_set = set(list(self.amb_set))
			return

		#copying a different commutator with the prescribed sign.
		#example: if a==$L(i,J)^e$, then command "b=L+generator(a,f)"
		#gives b==$L(i,J)^f$
		if len(args) == 2:
			other, inv = args
			self.elem = other.elem
			self.amb_set = set(list(other.amb_set))
			self.inverted = inv
			return

		print('error: too many args in Gen.__init__(*args)')

	def __hash__(self):
		return hash(tuple([self.elem, self.inverted]+self.amb_set))

	def __len__(self):
		return len(self.amb_set)

	def __neg__(self):
		return Gen(self, not self.inverted)

	def __eq__(self,other):
		return self.elem == other.elem and self.amb_set == other.amb_set and self.inverted == other.inverted

	#Example: StringForm of $L(3,1358)^{-1}$ is            '(3<1358)'
	#            __str__ of $L(3,1358)^{-1}$ is 'Gen(3<1358)^-1'
	#           __repr__ of $L(3,1358)^{-1}$ is            '(3<1358)^-1'
	def StringForm(self):
#		ans = 'Gen('
		ans = '('
		ans += str(self.elem) + '<' + ''.join(map(str,list(self.amb_set)))
#		if self.inverted:
#			ans += '^-1'
		return ans + ')'

	def __str_(self):
#		ans = 'Gen'+self.StringForm()
		ans = self.StringForm()
		if self.inverted:
			ans += '^-1'
		return ans

	def __repr__(self):
		ans = self.StringForm()
		if self.inverted:
			ans += '^-1'
		return ans

#A reduced word in the free group on L-generators.
class Word:
	__slots__ = ['letters']

	def __init__(self, *args):
		#Word() is an empty word
		if len(args) == 0:
			self.letters = []
			return

		#Word(W) is a copy of W
		if len(args) == 1:
			self.letters = args[0].letters[:]
			return
		
		#Assuming that a is an L-generator or its inverse:
		#Word(a,0) is the word $a$
		#Word(a,1) is the word $a^-1$.
		if len(args) == 2:
			K, inverted = args
			if not inverted:
				self.letters = [K]
			else:
				self.letters = [-K]
			return

		print('error: too many args in Word.__init__(*args)')
		
	def AddLetter(self,let):
		if not len(self.letters):
			self.letters = [let]
			return
		if self.letters[-1] == -let:
			self.letters = self.letters[:-1]
		else:
			self.letters.append(let)

	#'==' is the strict equality of words, i.e. the words a*a^-1 and 1 are not equal.
	def __eq__(self, other):
		return (self.letters == other.letters)

	def __len__(self):
		return len(self.letters)

	#the concatenation of words is made with reductions.
	def __add__(self,other):
		ans = Word()
		ans.letters = self.letters[:]
		for L in other.letters:
			ans.AddLetter(L)
		return ans

	def __sub__(self,other):
		return self + (-other)

	def __neg__(self):
		ans = Word()
		for let in reversed(self.letters):
			ans.AddLetter(-let)
		return ans

	def __repr__(self):
		return 'Word['+''.join(str(K) for K in self.letters)+']'
#		return ''.join(str(K) for K in self.letters)

	def __str__(self):
		return 'Word['+''.join(str(K) for K in self.letters)+']'
#		return ''.join(str(K) for K in self.letters)

#-------------------------------------------------------------------------------------
# Elementary operations
#-------------------------------------------------------------------------------------

#The one-letter word $K$ which corresponds to an L-generator $K$.
def OneLetterWord(K):
	return Word(K,False)

#The reduced word which corresponds to a sequence of L-generators.
def LTW(lets):
	ans = Word()
	for lt in lets:
		ans.AddLetter(lt)
	return ans

#-----------------------------------------------------------
# Functions about graphs
#------------------------------------------------------------

#are the vertices i,j in the same connected component of G?
def AreInSameComponent(i,j, G):
	return (j in nx.node_connected_component(G,i))

#what is the minimal element of the same path component as i?
def MinInComponent(i, G):
	return min(nx.node_connected_component(G,i))

#what is the first vertex in a shortest path from i to j along edges of G?
def FirstStep(i,j, G):
	return nx.shortest_path(G,source=i,target=j)[1]

#   GenIsDistinguished($L(i,J)$, $Г$) finds if L(i,J) is distinguished.
def GenIsDistinguished(K, graph):
	elem = K.elem
	amb_set = K.amb_set
	maxel = max(amb_set)
	g = graph.subgraph(amb_set)

	if AreInSameComponent(elem, maxel, g):
		return False
	if elem != MinInComponent(elem, g):
		return False
	return True

#----------------------------------------------------------------------------
#  Reduction of L-generators
#----------------------------------------------------------------------------

#   GenShift($L(i,J)$   ,$j$)
#	returns the word $L(j,J)*L(i,J\j)*L(j,J\i)^-1$.
#   GenShift($L(i,J)^-1$,$j$)
#	returns its inverse.
def GenShift(K, j):
	if K.inverted:
		return -GenShift(-K,j)
	i = K.elem
	inv = K.inverted
	amb_set = set(list(K.amb_set))
	
	ans = Word()
	ans.AddLetter(Gen(j, amb_set         , 0))
	ans.AddLetter(Gen(i, amb_set-set([j]), 0))
	ans.AddLetter(Gen(j, amb_set-set([i]), 1))
	
	return ans

#   GenMakeDistinguished($L(i,J)$, $Г_J$)
#   computes the word $Red(L(i,J))$.
def GenMakeDistinguished(K, graph):
	if K.inverted:
		return -GenMakeDistinguished(-K, graph)

	if GenIsDistinguished(K, graph):
		return OneLetterWord(K)

	#L(max(J),J)=1
	elem = K.elem
	maxel = max(K.amb_set)
	if elem == maxel:
		return Word()

	#An optimisation:
	#It i and max(J) are connected by an edge,
	#then L(i,J) = L(i,J\max(J)).
	if graph.has_edge(elem, maxel):
		newset = K.amb_set - set([maxel])
		return GenMakeDistinguished(
			Gen(elem, newset, K.inverted),
			graph.subgraph(list(newset))
		)


	if AreInSameComponent(elem, maxel, graph):
		j = FirstStep(elem, maxel, graph)
	else:
		j = FirstStep(elem, MinInComponent(elem, graph), graph)

	return WordMakeDistinguished(GenShift(K, j), graph)

#   WordMakeDistinguished($W$,$Г$) returns $Red(W)$.
def WordMakeDistinguished(W, graph):
	ans = Word()

	for K in W.letters:
		g = graph.subgraph(list(K.amb_set))
		ans += GenMakeDistinguished(K, g)
	return ans

#----------------------------------------------------------------------------
#  Relations which correspond to paths
#----------------------------------------------------------------------------

#   PathRelation($Г$, [i1,i2,...,ik], $J$)
#   produces the relation $R((i1,i2,..ik,i1),J)$.
def PathRelation(path, J):
	ans = Word()

	cycle = path + [path[0]]
	l = len(path)
	for i in range(l):
		ans.AddLetter(Gen(cycle[i+1], set(J)-set([cycle[i  ]]), False))
		ans.AddLetter(Gen(cycle[i  ], set(J)-set([cycle[i+1]]), True ))

	return ans
	
def ReducedPathRelation(big_graph, path, J):
	return WordMakeDistinguished(
		PathRelation(path, J),
		big_graph.subgraph(J)
	)

#----------------------------------------------------------------------------
# Verification of relations.
#
# In the code below, each L-generator is rewritten as a product of g_1,..,g_m;
# Then the function SimplifyStr computes the reduced form for this element of RC_\Gamma.
# To improve the performance, everything is encoded in strings (where g_1 is 'b', g_2 is 'c', etc.)
#----------------------------------------------------------------------------
def inttochar(k):
	return chr(k+ord('a'))

def chartoint(c):
	return ord(c)-ord('a')

def GenToStr(K):
	if K.inverted:
		return GenToStr(-K)[::-1]
	x = K.elem
	lst = sorted(K.amb_set)
	ans = ''.join(map(inttochar,lst))
	lst.remove(x)
	return ans + inttochar(x) + ''.join(map(inttochar,lst))[::-1] 

def SimplifyStr(s, m, graph):
	upd = True
	n = len(s)
	currshift = 0#position, starting from which we try to cancel two letters
	while upd and n > 0:
		upd = False
		for ti in range(n):
			i = (ti+currshift) % n
			lt = s[i]#current letter
			if lt in s[i+1:]:
				nextpos = i+1+s[i+1:].index(lt)#next occurence of that letter
				if all(graph.has_edge(chartoint(lt), chartoint(ot))
						for ot in s[i+1:nextpos]):
					n -= 2
					s = s[:i]+s[i+1:nextpos]+s[nextpos+1:]
					upd = True
					currshift = i-1#an optimization to remove "abcddcba" faster
					break
	return s

def WordToStr(W):
	return ''.join(map(GenToStr,W.letters))
	
def IsARelation(W, m, graph):
	s = WordToStr(W)
	return len(SimplifyStr(s,m,graph) == 0)


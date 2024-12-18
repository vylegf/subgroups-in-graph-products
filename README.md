# Subgroups in graph products of groups
This project contains some algorithms (in Python3) related to presentations of Cartesian subgroups in graph products of groups. This is the topic of the upcoming paper "Cartesian subgroups in graph products of groups" by the author.

# Mathematics 
For a simple graph $\Gamma$ on the vertex set $[m]=(1,\dots,m)$, consider the **right-angled Coxeter group**
$RC_\Gamma=\langle g_1,\dots,g_m\mid g_i^2=1; g_ig_j=g_jg_i, (i,j)\in\Gamma\rangle.$

We describe a small presentation of its commutator subgroup $RC'_\Gamma,$ which is also identified with fundamental groups of corresponding real moment-angle complexes.
By "duplicating" generators and relations, one obtains presentations for Cartesian subgroups of graph products of arbitrary discrete groups, $Cart(\underline{G},\Gamma):=Ker(\underline{G}^\Gamma\to G_1\times\dots\times G_m)$ (see the paper for the details).

## Generators
For $i\in J\subset[m]$, consider the elements $L(i,J):=\prod_{j\in J}g_j\cdot g_i^{-1}\cdot (\prod_{j\in J\setminus i}g_j)^{-1}\in RC'_ \Gamma$ (the products are in the ascending order, eg $L(3,1358)=g_1g_3g_5g_8\cdot g_3^{-1}\cdot (g_1g_5g_8)^{-1} = g_1g_3g_5g_8g_3g_8g_5g_1$). 

Consider the following subset $\Theta(J)$ of $J$: we have $i\in\Theta(J)$ if and only if the following two conditions are satisfied:
* In the induced subgraph $\Gamma_J$, the vertex $i$ is the smallest in its path component;
* The vertices $i$ and $\max(J)$ are in different path components of $\Gamma_J$.

Then the set $\widehat{D}:=(L(i,J):i\in\Theta(J),J\subset[m])$ of **distinguished elements** is our generating set for $RC'_\Gamma$. (This set of generators was suggested by Li Cai.)

In particular, each $L(i,J)$ can be written as a word $Red(L(i,J))$ on distinguished elements. The function `lib.GenMakeDistinguished(K,graph)` computes this word (here `K`= $L(i,J)$, `graph`= $\Gamma$).

## Relations
The relations correspond to the cycles in induced subgraphs. In more detail, let $\lambda=(i_1,\dots,i_k,i_{k+1}=i_1)$ be a cycle in the induced subgraph $\Gamma_J$. Then $R(\lambda)=1$ in $RC'_\Gamma$, where

$R(\lambda)=\prod_{t=1}^k L(i_{t+1},J\setminus i_t)\cdot L(i_t,J\setminus i_{t+1})^{-1}.$

After applying $Red(-)$, we obtain a relation $Red(R(\lambda))=1$ between the generators. The function `lib.ReducedPathRelation(big_graph, path, J)` computes this relation (as a word on distinguished elements).

# Content

All functions are in the file `lib.py`. In the file `m-gon.py` we compute the single relation in the group $RC'_\Gamma$, where $\Gamma$ is an $m$-cycle. This group is known to be a surface group of genus $g(m)=1+(m-4)2^{m-3}$. Curiously, our methods also produce a one-relator presentation where the relation has length $4g(m)$ (we checked this for $m\leq 20$).

# Long-term plans
A similar approach can be used to study certain subgroups in $\mathrm{RC}_\Gamma$ (i.e. fundamental groups of real toric spaces, including small covers, and some coverings of real moment-angle complexes).
Related code may appear in this repository.

# Subgroups in graph products of groups
Cartesian subgroups in graph products of groups are generalisations of commutator subgroups in right-angled Coxeter groups (RACGs).

In the paper "Cartesian subgroups in graph products of groups" (available at https://arxiv.org/abs/2412.19764 ), we describe how to compute "small" presentations of these subgroups by generators and relations.
This repository contains algorithms (implemented in Python3) which do most of the calculations.

# Mathematics 
For a simple graph $\Gamma$ on the vertex set $[m]=(1,\dots,m)$, consider the **right-angled Coxeter group**
$RC_\Gamma=\langle g_1,\dots,g_m\mid g_i^2=1; g_ig_j=g_jg_i, \lbrace i,j\rbrace\in\Gamma\rangle.$

We describe a small presentation of its commutator subgroup $RC'_\Gamma,$ which is also identified with fundamental groups of corresponding real moment-angle complexes.
By "duplicating" generators and relations, one obtains presentations for Cartesian subgroups of graph products of arbitrary discrete groups, $Cart(\underline{G},\Gamma):=Ker(\underline{G}^\Gamma\to G_1\times\dots\times G_m)$ (see Section 4 of the paper for details).

## Generators
Given $i\in J\subset[m]$, consider the element $L(i,J):=\prod_{j\in J}g_j\cdot g_i^{-1}\cdot (\prod_{j\in J\setminus i}g_j)^{-1}$ of the group $RC'_ \Gamma$. Here the products are in the ascending order, eg $L(3,1358)=g_1g_3g_5g_8\cdot g_3^{-1}\cdot (g_1g_5g_8)^{-1} = g_1g_3g_5g_8g_3g_8g_5g_1$. 

Consider the following subset $\Theta(J)$ of $J$. We have $i\in\Theta(J)$ if and only if the following two conditions are satisfied:
* In the induced subgraph $\Gamma_J$, the vertex $i$ is the smallest in its path component;
* The vertices $i$ and $\max(J)$ are in different path components of $\Gamma_J$.

>The set $\widehat{D}:=\lbrace L(i,J):i\in\Theta(J),J\subset[m]\rbrace$ of **distinguished elements** is our generating set for $RC'_\Gamma$. (This set of generators was suggested by Li Cai.)

This set is computed by the function `ListGens(graph)`.

Since $\widehat{D}$ generates the whole group, each element $L(i,J)$ is equal in $RC'_\Gamma$ to a word $Red(L(i,J))$ on distinguished elements. This word is computed by the function `lib.GenMakeDistinguished(K,graph)` (here `K`= $L(i,J)$, `graph`= $\Gamma$).

($Red$ works recursively, using elementary identities $L(\max(J),J)=1$ and $L(i,J)L(j,J\setminus i)=L(j,J)L(i,J\setminus j)$ for $\lbrace i,j\rbrace\in\Gamma_J$.)

## Relations
The relations correspond to the cycles in induced subgraphs. In more detail, let $\lambda=(i_1,\dots,i_k,i_{k+1}=i_1)$ be a cycle in the induced subgraph $\Gamma_J$. Then $R(\lambda,J)=1$ in $RC'_\Gamma$, where

$R(\lambda,J)=\prod_{t=1}^k L(i_{t+1},J\setminus i_t)\cdot L(i_t,J\setminus i_{t+1})^{-1}.$

After applying $Red(-)$, we obtain a relation $Red(R(\lambda,J))=1$ between the generators. The function `lib.ReducedPathRelation(big_graph, path, J)` computes this relation (as a word on distinguished elements).

>For each $J\subset[m]$, choose a set of cycles $Gen(J)$ which generates the fundamental groups of clique complexes for each path component of $\Gamma_J$. Then $\lbrace Red(R(\lambda,J)):\lambda\in Gen(J),J\subset[m]\rbrace$ is a sufficient set of relations.

To conclude, $RC_\Gamma =\langle L(i,J):i\in\Theta(J),J\in[m]\mid Red(R(\lambda,J)):\lambda\in Gen(J),J\subset[m]\rangle.$

# Content
Dependencies: [networkx](networkx.org) package for Python.

All functions are in the file `lib.py`. In the file `m-gon.py` we compute the single relation in the group $RC'_ \Gamma$, where $\Gamma$ is an m-cycle. This group is known to be a surface group $\langle a_1,b_1,\dots,a_ g,b_ g\mid (a_1,b_1)\cdot\dots\cdot (a_g,b_g)=1\rangle.$ of genus $g(m)=1+(m-4)2^{m-3}$. Our methods also produce a presentation on $2g(m)$ generators and one relation. Curiously, the length of our relation also equals $4g(m)$ (we checked this for $m\leq 20$).

# Long-term plans
A similar approach can be used to study certain subgroups in $\mathrm{RC}_\Gamma$ (i.e. fundamental groups of real toric spaces, including small covers, and some coverings of real moment-angle complexes).
Related code may appear in this repository.


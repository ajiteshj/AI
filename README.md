# AI
Artificial Intelligence Project1 - SAT SOLVER

Problem Description : 
Suppose you have a wedding to plan, and want to arrange the wedding seating for a certain
number of guests in a hall. The hall has a certain number of tables for seating. Some pairs of
guests are couples or close Friends (F) and want to sit together at the same table. Some other
pairs of guests are Enemies (E) and must be separated into different tables. The rest of the pairs
are Indifferent (I) to each other and do not mind sitting together or not. However, each pair of
guests can have only one relationship, (F), (E) or (I). You must find a seating arrangement that
satisfies all the constraints.


SAT Encoding :
To decompose the arrangement task, there are three constraints you have to satisfy:
(a) Each guest should be seated at one and only one table.
(b) For any two guests who are Friends (F), you should seat them at the same table.
(c) For any two guests who are Enemies (E), you should seat them at different tables.
Note that, for simplicity, you do NOT need to consider the capacity constraint of a table. This
means the size of each table is assumed to be large enough to seat all the guests.
The arrangement task can be encoded as a Boolean satisfaction problem. We introduce
Boolean variables X mn to represent whether each guest m will be seated at a specific table ​ n .
You are asked to construct clauses and generate CNF sentence for each instance of the seating
arrangement.Suppose there are <M> guests in total, and there are <N> tables in the hall. You
may assume each table has an unlimited capacity.
You need to express each of the above-mentioned constraints as clauses in CNF format.
  
Task :
Write a program to generate CNF sentences for an input instance of wedding seating arrangements. The inputs include the
number of guests <M >, the number of tables <N >, and a sparse representation of the relationship matrix  R with elements R ij = 1, -1 or 0 to represent whether guests i and j are Friends (F), Enemies (E) or Indifferent (I).
  
Implement a SAT solver to find a satisfying assignment for any given CNF
sentences.

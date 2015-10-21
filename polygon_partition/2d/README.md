This proj is a simple polypartition algorithm prototype.
The algorithm used are presented in:
https://en.wikipedia.org/wiki/Minimum-weight_triangulation
Simple explain of the principles:
1, this algorithm use the floyd dp algorithm find the euclide minimal distance 
between every pair of polygon verts.
2, then from the minimal array c[0][n-1] build a triangle (0,r,n-1) where r is
the middle point in the minimal dist.
3, this triangle split the polygon into two parts, recursively process the two parts
until the least polygon (which is a triangle)

Its hard to prove the minimal, but its obviously a polygon partition and every edge 
comes from the minimal distance.

Remember, This algorithm cannot handle complex polygon or polygon with holes.
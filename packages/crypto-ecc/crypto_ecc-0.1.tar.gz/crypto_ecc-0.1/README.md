# ECC crypto functions

* ECCDouble(point) - Add point to itself, returns new point
* ECCadd(point1, point2) - Add point1 to point2, returns new point
* ECCDiv(point) - Reverse method of ECCDouble, returns new point
* ECCSub(point1, point2) - Sub point2 from point1, returns new point
* get_point(key) - Arg is 32 byte key, returns point   
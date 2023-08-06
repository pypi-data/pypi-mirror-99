class Rect:
    def __init__(self,cpt,w,h):
        self.x = cpt[0]
        self.y = cpt[1]
        self.w = w
        self.h = h

    def dist(self,other):
        #overlaps in x or y:
        if abs(self.x - other.x) <= (self.w + other.w):
            dx = 0;
        else:
            dx = abs(self.x - other.x) - (self.w + other.w)
        #
        if abs(self.y - other.y) <= (self.h + other.h):
            dy = 0;
        else:
            dy = abs(self.y - other.y) - (self.h + other.h)
        return dx + dy

#example:

# (271, 818, 278, 826) (281, 772, 305, 821)
A = Rect((0,0),2,1)
B = Rect((4,5),1,2)
C = Rect((-1,-5),1,1)

D = Rect(((818+826)/2, (271+278)/2), 826-818, (278-271))
E = Rect(((772+821)/2, (281+305)/2),821-772,  (305-281))

print(A.dist(C))
print(A.dist(B))
print(B.dist(C))

print(D.dist(E))
print(E.dist(E))


# rect
#   var
#     x1;y1;x2;y2

import math

def DistanceTo(rect, R2):
    # // assume always that x1<=x2 and y1<=y2
    # // that can be handled in New()

    # (271, 818, 278, 826)(281, 772, 305, 821)
    # (271, 818, 278, 826)(277, 786, 288, 830)
    x1 = 271
    x2 = 278
    y1 = 818
    y2 = 826
    R2x1 = 277#281
    R2x2 = 288#305
    R2y1 = 786#772
    R2y2 = 830#821

    dx=max(x1,R2x1)-min(x2,R2x2)
    dy=max(y1,R2y1)-min(y2,R2y2)
    if(dx<0):
        return max(dy,0)
    if(dy<0):
        return dx
    return math.sqrt(dx*dx+dy*dy)



print(DistanceTo(None, None)) # ok

# def intersects(self, other):
#     return not (self.top_right.x < other.bottom_left.x or self.bottom_left.x > other.top_right.x or self.top_right.y < other.bottom_left.y or self.bottom_left.y > other.top_right.y)


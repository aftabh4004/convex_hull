import math


# description: Function to read data from the file
# param:
#     file: pointer to the file
# Return:
#     g: grid quantum value read from the file
#     n: Total number of point
#     S: Set of points as list of coordinate(as list of 2 element)
#     (g, n, S)
    
def read_from_file(file):
    file = open(file, "r")
    g = int(file.readline())
    n = int(file.readline())

    x = []
    y = []
    S = []
    for i in range(n):
        points = [int(i) for i in file.readline().split()]
        S.append(points)
    return (g, n, S)



# description: Function to translate the given pount set accroding to the SVG coordinate system
# param:
#     S: Set of all points
#     g: grid unit length
# return:
#     St: translated set of points

def translate(S, g):
    x = []
    y = []
    St = []
    for p in S:
        x.append(p[0])
        y.append(p[1])
        
    minx = min(x)
    miny = min(y)
    maxy = max(y)
    maxx = max(x)
    
    #translate
    for i in range(len(x)):
        x[i] = x[i] - minx + g
        y[i] = (y[i] - maxy)*-1 + g
        St.append([x[i], y[i]])
    return St 


# #########################################################################
#  Part 1

# ##########################################################################

# description: Function to create a SVG file and draw all the points in the canvas as Part 1 asked.
# param:
#     P: translated set of points
#     g: grid unit length
#     file: name of file as string that has to be created
# return:
#     None

def draw_part1(P, g, file):
    
    x = []
    y = []
    St = []
    for p in P:
        x.append(p[0])
        y.append(p[1])
        
    minx = min(x)
    miny = min(y)
    maxy = max(y)
    maxx = max(x)
    
    
    # setting the demension of canvas
    width = maxx - minx  + 2 * g
    height = maxy - miny + 2 * g
    
    # Points of boundary rectange 
    rect_points = f"{g},{g} {width - g},{g} {width - g},{height - g} {g},{height - g}"

    fsvg = open(file, "w")
    fsvg.write(f"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" >\n")
    
    # making background of canvas white
    fsvg.write(f"<rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n")
    
    fsvg.write(f"<polygon stroke=\"red\" points=\"{rect_points}\" fill=\"none\" stroke-width=\"1\" stroke-dasharray=\"8\"/>\n")
    for point in P:
        fsvg.write(f"<circle cx=\"{point[0]}\" cy=\"{point[1]}\" r=\"2\" fill=\"black\" />\n")
    fsvg.write("</svg>")
    fsvg.close()


# #####################################################################################
# ## Part 2
# 
# #####################################################################################




# description: Calculate Euclidean distance between to points
# param:
#     p: first point
#     q: second point
# return:
#     distance between p and q
    
def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2) 



# description: Order given set of points in the order of polygon
# param:
#     S: Set of unordered points
#     g: grid unit length
# return:
#     P: Set of points in polygon order

def order_polygon_points(S, g):
    if len(S) == 0: return []
    P = [S[0]]
    
    visited = [False]* len(S)
    visited[0] = True
    i = 0

    # pick the point which is g or sqrt(2)*g distance apart and iteratively
    # find the next point aroung the picked point
    while len(S) != len(P):
        for j in range(len(S)):
            
            if (dist(S[i], S[j]) == g or dist(S[i], S[j]) == math.sqrt(2) * g) and visited[j] == False:
                P.append(S[j])
                visited[j] = True
                i = j
                break
    return P




# description: Function to create a SVG file and draw polygon in the canvas as Part 2 asked.
# param:
#     S: translated set of points
#     g: grid unit length
#     file: name of file as string that has to be created
# return:
#     None

def draw_polygon(S, g, file):
    P = order_polygon_points(S, g)
    x = []
    y = []
    St = []
    for p in P:
        x.append(p[0])
        y.append(p[1])
        
    minx = min(x)
    miny = min(y)
    maxy = max(y)
    maxx = max(x)
    
    # setting the demension of canvas
    width = maxx - minx  + 2 * g
    height = maxy - miny + 2 * g
    
    # Points of boundary rectange
    rect_points = f"{g},{g} {width - g},{g} {width - g},{height - g} {g},{height - g}"
    
    # Points of polygon in order
    poly_points = [f"{x},{y}" for [x, y] in P]
    poly_points = " ".join(poly_points)

    # Writing in SVG file
    fsvg = open(file, "w")
    fsvg.write(f"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" >\n")
    fsvg.write(f"<rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n")
    fsvg.write(f"<polygon stroke=\"red\" points=\"{rect_points}\" fill=\"none\" stroke-width=\"1\" stroke-dasharray=\"8\"/>\n")
    fsvg.write(f"<polygon stroke=\"black\" points=\"{poly_points}\" fill=\"yellow\" stroke-width=\"1\" />\n")

    # drwaing small circle for the points of polygon
    for point in P:
        fsvg.write(f"<circle cx=\"{point[0]}\" cy=\"{point[1]}\" r=\"2\" fill=\"black\" />\n")
    fsvg.write("</svg>")
    fsvg.close()

# #################################################################################
# ## Part 3
# ## Convex Hull
# 
# #################################################################################



# description: Function to create a SVG file and draw the original polygon and the 
#              convex hull polygon with provided set of points  in the canvas as Part 3 asked.
# param:
#     CH: points of convex hull in order
#     S: translated set of points
#     g: grid unit length
#     file: name of file as string that has to be created
# return:
#     None



def draw_hull(CH, S, g, file):
    P = order_polygon_points(S, g)
    x = []
    y = []
    for p in P:
        x.append(p[0])
        y.append(p[1])
        
    minx = min(x)
    miny = min(y)
    maxy = max(y)
    maxx = max(x)
    
    # setting the demension of canvas
    width = maxx - minx  + 2 * g
    height = maxy - miny + 2 * g
    
    # Points of boundary rectange
    rect_points = f"{g},{g} {width - g},{g} {width - g},{height - g} {g},{height - g}"
    
    # Convex Hull points in order
    ch_points = [f"{x},{y}" for [x, y] in CH]
    ch_points = " ".join(ch_points)
    
    # Points of polygon in order
    poly_points = [f"{x},{y}" for [x, y] in P]
    poly_points = " ".join(poly_points)
    

    fsvg = open(file, "w")
    fsvg.write(f"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" >\n")
    fsvg.write(f"<rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n")
    fsvg.write(f"<polygon stroke=\"red\" points=\"{rect_points}\" fill=\"none\" stroke-width=\"1\" stroke-dasharray=\"8\"/>\n")
    fsvg.write(f"<polygon stroke=\"black\" points=\"{ch_points}\" fill=\"#66CDAA\" stroke-width=\"1\" />\n")
    fsvg.write(f"<polygon stroke=\"black\" points=\"{poly_points}\" fill=\"yellow\" stroke-width=\"1\" />\n")
    

    for point in CH:
        fsvg.write(f"<circle cx=\"{point[0]}\" cy=\"{point[1]}\" r=\"2\" fill=\"black\" />\n")
    fsvg.write("</svg>")
    fsvg.close()



# description: Recursive function to find the Convex Hull of set of points
# param:
#     S: Set of points sorted accroding to the x-coordinate
# return:
#     CH: Convex Hull of the set of points

def Convex_Hull(S):
    
    n = len(S)
    CH = S

    # Handling the base cases
    if n == 2:
        return CH
    
    # if three points are colinear, return the extream two points as Convex Hull, otherwise return
    # the points in anti-clockwise order
    if len(S) == 3:
        r = is_collinear(S[0], S[1], S[2])
        if r == 1:
            CH = [S[2], S[1], S[0]]
        elif r == 0:
            CH = [S[0], S[2]]
        return CH
            
    
    # Divide step 
    mid = (n - 1)//2 
    Ha = Convex_Hull(S[:mid + 1])
    Hb = Convex_Hull(S[mid + 1:])
    CH = Combine(Ha, Hb)
    return CH


# description: Combine step of the algorithm, Combine Hull A and Hull B into bigger Hull
# param:
#     Ha: Left sub Convex Hull
#     Hb: Right sub Convex Hull
# return:
#     CH: Combined Convex Hull
        
def Combine(Ha, Hb):
    
    # Considering the case of all the four points in Ha and Hb are colinear
    # if colinear then return the extream two points as CH
    if len(Ha) == len(Hb) and len(Ha) == 2:
        r1 = is_collinear(Ha[0], Ha[1], Hb[0])
        r2 = is_collinear(Ha[0], Ha[1], Hb[1])
        
        if r1 == 0 and r2 == 0:
            return [Ha[0], Hb[1]]
    
    # finding the upper and lower tangent
    lt = lower_tangent(Ha, Hb)
    ut = upper_tangent(Ha, Hb)
    CH = []
    
    
    
    # Combine 
    i = ut[0]
    while i != lt[0]:
        CH.append(Ha[i])
        i = (i + 1) % len(Ha)
    CH.append(Ha[i])
        
    i = lt[1]
    while i != ut[1]:
        CH.append(Hb[i])
        i = (i + 1) % len(Hb)
    CH.append(Hb[i])
    return CH


# ## Lower and upper tangent


# description: Find the upper tangent of Ha and Hb
# param:
#     Ha: Left sub Convex Hull
#     Hb: Right sub Convex Hull
# return:
#     (rm , lm): index of the upper tangent points in Ha and Hb respectivily
   
def upper_tangent(Ha, Hb):
    lm = 0
    rm = 0
    
    #top right most of Ha
    for i in range(1, len(Ha)):
        if Ha[i][0] > Ha[rm][0]:
            rm = i
        elif Ha[i][0] == Ha[rm][0]  and Ha[i][1] < Ha[rm][1]:
            rm = i
       
    
    #top left most of Hb
    for i in range(1, len(Hb)):
        if Hb[i][0] < Hb[lm][0]:
            lm = i
        elif Hb[i][0] == Hb[lm][0]  and Hb[i][1] < Hb[lm][1]:
            lm = i
        
    
    isChanged = True 
    while isChanged:
        isChanged = False 
        isUT_to_Ha = False
        isUT_to_Hb = False
        while not isUT_to_Ha:
            rposition = is_collinear(Ha[rm], Hb[lm], Ha[(rm + 1) % len(Ha)])
            
            # next point in order is on the right of <rm, lm> vector
            if rposition == 1 :
                isUT_to_Ha = True
            
            # next point in order is colinear with  <rm, lm> vector
            elif rposition == 0:
                isUT_to_Ha = True
                rm = (rm + 1) % len(Ha)
            else:
                rm = (rm + 1) % len(Ha)
                isChanged = True
        
        while not isUT_to_Hb:
            rposition = is_collinear(Hb[lm], Ha[rm], Hb[(len(Hb) + lm - 1) % len(Hb)])
            
            # prev point in order is on the left of <lm, rm> vector
            if rposition == -1 :
                isUT_to_Hb = True
                
            # prev point in order is colinear with  <lm, rm> vector
            elif rposition == 0:
                isUT_to_Hb = True
                lm = (len(Hb) + lm - 1) % len(Hb)
            else:
                lm = (len(Hb) + lm - 1) % len(Hb)
                isChanged = True
    return (rm, lm)


# description: Find the lower tangent of Ha and Hb
# param:
#     Ha: Left sub Convex Hull
#     Hb: Right sub Convex Hull
# return:
#     (rm , lm): index of the lower tangent points in Ha and Hb respectivily


def lower_tangent(Ha, Hb):
    lm = 0
    rm = 0
            
    #right most of Ha
    for i in range(1, len(Ha)):
        if Ha[i][0] > Ha[rm][0]:
            rm = i
        elif Ha[i][0] == Ha[rm][0]  and Ha[i][1] > Ha[rm][1]:
            rm = i
       
    
    #left most of Hb
    for i in range(1, len(Hb)):
        if Hb[i][0] < Hb[lm][0]:
            lm = i
        elif Hb[i][0] == Hb[lm][0]  and Hb[i][1] > Hb[lm][1]:
            lm = i
       
    
    
    
    isChanged = True 
    while isChanged:
        isChanged = False 
        isLT_to_Ha = False
        isLT_to_Hb = False
        while not isLT_to_Ha:
            rposition = is_collinear(Ha[rm], Hb[lm], Ha[(len(Ha) + rm - 1) % len(Ha)])
            
            # prev point in order is on the left of <rm, lm> vector
            if rposition == -1 :
                isLT_to_Ha = True
                
            # prev point in order is colinear with  <rm, lm> vector
            elif rposition == 0:
                isLT_to_Ha = True
                rm = (len(Ha) + rm - 1) % len(Ha)
            else:
                rm = (len(Ha) + rm - 1) % len(Ha)
                isChanged = True
        
        while not isLT_to_Hb:
            rposition = is_collinear(Hb[lm], Ha[rm], Hb[(lm + 1) % len(Hb)])
            
            
            # next point in order is on the right of <lm, rm> vector
            if rposition == 1 :
                isLT_to_Hb = True
                
            # next point in order is colinear with  <lm, rm> vector
            elif rposition == 0:
                isLT_to_Hb = True
                lm = (lm + 1) % len(Hb)
            else:
                lm = (lm + 1) % len(Hb)
                isChanged = True
    return (rm, lm)



# description: Give orientation of r w.r.t the vector pq
            
# param:
#     p: tail of vector
#     q: head of vector
#     r: test point
# return:
#      -1 if the r is left of vector pq
#       1 if the r is right of vector pq
#       0 if p, q, r are collinear

    
def is_collinear(p, q, r):
    delta = (q[1] - p[1]) * (r[0] - q[0])  - (q[0] - p[0]) * (r[1] - q[1])
    
    if delta < 0:
        return 1
    if delta > 0:
        return -1
    return 0



def main():
    
    # For Aero
    g, n, S, = read_from_file("aero.txt")
    S = translate(S, g)
    draw_part1(S, g, "aero_1.svg")
    draw_polygon(S, g, "aero_2.svg")
    S.sort()
    CH = Convex_Hull(S)
    draw_hull(CH, S, g, "aero_3.svg")
    
    # For car
    g, n, S, = read_from_file("car.txt")
    S = translate(S, g)
    draw_part1(S, g, "car_1.svg")
    draw_polygon(S, g, "car_2.svg")
    S.sort()
    CH = Convex_Hull(S)
    draw_hull(CH, S, g, "car_3.svg")
    
    # For flower
    g, n, S, = read_from_file("flower.txt")
    S = translate(S, g)
    draw_part1(S, g, "flower_1.svg")
    draw_polygon(S, g, "flower_2.svg")
    S.sort()
    CH = Convex_Hull(S)
    draw_hull(CH, S, g, "flower_3.svg")
   


if __name__ == "__main__":
    main()




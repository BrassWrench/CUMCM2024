from matplotlib.patches import Rectangle

def Intersection_over_rectangle(rectangle1, rectangle2):
    r1 = Rectangle((rectangle1[0], rectangle1[1]), rectangle1[2], rectangle1[3])
    r2 = Rectangle((rectangle2[0], rectangle2[1]), rectangle2[2], rectangle2[3])
    ir = r1.intersection(r2)

    if ir.width <= 0 or ir.height <= 0:
        return 0
    else:
        return ir.width * ir.height

rectangle1 = (1, 1, 3, 3)
rectangle2 = (2, 2, 3, 3)

intersection_area = Intersection_over_rectangle(rectangle1, rectangle2)

print(intersection_area) # 输出结果为4

import turtle

def draw_tree(t, branch_length, angle_left, angle_right, reduction_factor, depth):
    if depth == 0:
        # Draw a leaf
        t.color("green")
        t.begin_fill()
        t.circle(5)  # Draw a small circle to represent the leaf
        t.end_fill()
        t.color("brown")  # Revert color back to the trunk color
        return

    # Draw the current branch
    t.forward(branch_length)

    # Draw the left subtree
    t.left(angle_left)
    draw_tree(t, branch_length * reduction_factor, angle_left, angle_right, reduction_factor, depth - 1)
    t.right(angle_left)

    # Draw the right subtree
    t.right(angle_right)
    draw_tree(t, branch_length * reduction_factor, angle_left, angle_right, reduction_factor, depth - 1)
    t.left(angle_right)

    # Go back to the starting position
    t.backward(branch_length)


# User inputs
angle_left = int(input("Enter left branch angle (degrees): "))
angle_right = int(input("Enter right branch angle (degrees): "))
starting_length = int(input("Enter starting branch length (pixels): "))
reduction_factor = float(input("Enter branch length reduction factor (e.g., 0.7): "))
depth = int(input("Enter recursion depth: "))

# Set up the turtle
screen = turtle.Screen()
screen.title("Recursive Tree with Leaves")
t = turtle.Turtle()
t.speed(0)
t.left(90)  # Point the turtle upwards
t.color("brown")
t.pensize(2)

# Draw the tree
t.up()
t.goto(0, -200)
t.down()
draw_tree(t, starting_length, angle_left, angle_right, reduction_factor, depth)

# Finish
turtle.done()

from pydraw import *;

screen = Screen(800, 600);

screen.toggle_grid();
# screen.clear();
screen.grid(helpers=True);


p1 = Polygon(screen, 5, 150, 50, 50, 50)
poly = Triangle(screen, 50, 50, 50, 50);
image = Image(screen, '../images/pacman.gif', 100, 50, 50, 50);
image.load();

rect = Rectangle(screen, 250, 250, 100, -50, Color('BLUE'))

# poly.width(500, ratio=True)
count = 5

def keydown(key):
    global count;

    if key == 'r':
        p1.rotate(1);
    elif key == 'w':
        p1.width(p1.width() + 10)
    elif key == 'h':
        p1.height(p1.height() + 10)
    elif key == 'x':
        p1.x(p1.x() + 10)
    elif key == 'y':
        p1.y(p1.y() + 10)
    elif key == 'g':
        image.next();
    elif key == 'n':
        poly.forward(3);
    elif key == 'b':
        # poly.backward(3);
        poly.border(Color('red'), width=count)
        count += 3;


def mousedown(button, location):
    print(f'Verties: {rect.vertices()}');
    print(f'Rect Contains: {rect.contains(location)}');

screen.listen();

fps = 30;
running = True;
while running:
    screen.update();
    screen.sleep(1 / fps);

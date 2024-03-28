#include "data.h"

bool square(int height, int width)
{
    return height == width;
}

bool long_rectangle(int height, int width)
{
    return abs(height - width) > 5;
}

int compute_area(int height, int width)
{
    return height * width;
}

int compute_perimeter(int option, int height, int width)
{
    if (option == RECTANGLE)
        return height * 2 + width * 2;
    else
        return height * 2 + width;
}

void rectangle(int height, int width)
{
    if (square(height, width) || long_rectangle(height, width))
    {
        int area = compute_area(height, width);
        std::cout << "Rectangle's area is: " << area << std::endl;
    }
    else
    {
        int perimeter = compute_perimeter(RECTANGLE, height, width);
        std::cout << "Rectangle's perimeter is: " << perimeter << std::endl;
    }
}
#include "data.h"

void print_space(int size)
{
    for (int i = 0; i < size; i++)
    {
        std::cout << " ";
    }
}

void print_first_line(int width)
{
    print_space(width / 2);
    std::cout << "*\n";
}

void print_cur_line(int cur_width)
{
    for (int j = 0; j < cur_width; j++)
    {
        std::cout << '*';
    }
    std::cout << "\n";
}

void print_last_line(int width)
{
    for (int i = 0; i < width; i++)
    {
        std::cout << '*';
    }
    std::cout << "\n";
}

void print_triangle(int height, int width, int num_for_each_width, int rest)
{
    print_first_line(width);
    int cur_width = 3, k = 1;
    while (k < height - 1)
    {
        for (int i = 0; i < num_for_each_width + rest; i++)
        {
            print_space((width - cur_width) / 2);
            print_cur_line(cur_width);
        }
        k += (num_for_each_width + rest); //next group.
        cur_width += 2; //next width/
        rest = 0; //rest is only to the first group.
    }
    print_last_line(width);
}

int compute_diff_lines(int width)
{
    int num_of_diff_lines = (width - 3) / 2;
    if (width == 3)
    {
        num_of_diff_lines = 1;
    }
    return num_of_diff_lines;
}

bool is_even_width(int width)
{
    return width % 2 == 0;
}

bool too_big_width(int height, int width)
{
    return width > height * 2;
}

void check_triangle(int height, int width)
{
    if (is_even_width(width) || too_big_width(height, width))
    {
        std::cout << "Can't print triangle.\n";
    }
    else
    {
        int num_of_diff_lines = compute_diff_lines(width);
        int num_of_all_lines = height - 2;
        int num_for_each_width = num_of_all_lines / num_of_diff_lines;
        int rest = num_of_all_lines % num_of_diff_lines;
        print_triangle(height, width, num_for_each_width, rest);
    }
}

void triangle(int height, int width)
{
    int option = 0;
    std::cout << "Enter your choice.\n1. to compute the triangle's perimeter.\n2. to print the triangle.\nYour choice is: ";
    std::cin >> option;
    if (option == COMPUTE_PERIMETER)
    {
        int perimeter = compute_perimeter(TRIANGLE, height, width);
        std::cout << "Triangles's perimeter is: " << perimeter << std::endl;
    }
    else
    {
        check_triangle(height, width);
    }
}
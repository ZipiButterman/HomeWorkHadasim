#include "data.h"

int main()
{
    int option = 0;
    std::cout << "Enter your choice.\n1. for rectangle tower.\n2. for triangle tower.\n3. to exit.\nYou choice is: ";
    std::cin >> option;
    while (option != EXIT)
    {
        int height = 0, width = 0;
        std::cout << "Enter height of the tower: ";
        std::cin >> height;
        std::cout << "Enter width of the tower: ";
        std::cin >> width;
        if (option == RECTANGLE)
        {
            rectangle(height, width);
        }
        else
        {
            triangle(height, width);
        }
        std::cout << "Enter your choice again: ";
        std::cin >> option;
    }
}

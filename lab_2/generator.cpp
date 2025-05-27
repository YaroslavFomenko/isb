#include <iostream>
#include <random>
#include <bitset>
#include <fstream>

void generate_cpp_sequence(int bits, const char* filename) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);

    std::ofstream out(filename);
    for (int i = 0; i < bits; ++i) {
        out << dis(gen);
    }
    out.close();
}

int main() {
    generate_cpp_sequence(128, "cpp_random_bits.txt");
    return 0;
}
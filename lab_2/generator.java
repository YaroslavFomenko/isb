import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomBitsGenerator {
    public static void generateJavaSequence(int bits, String filename) throws IOException {
        Random rand = new Random();
        FileWriter writer = new FileWriter(filename);

        for (int i = 0; i < bits; i++) {
            writer.write(rand.nextBoolean() ? "1" : "0");
        }

        writer.close();
    }

    public static void main(String[] args) throws IOException {
        generateJavaSequence(128, "java_random_bits.txt");
    }
}
/************************************
Course: cse 251
File: team1.java
Week: week 11 - team activity 1

Instructions:

- Main contains an array of 1,000 random values.  You will be creating
  threads to process this array.  If you find a prime number, display
  it to the console.

- DON'T copy/slice the array in main() for each thread.

Part 1:
- Create a class that is a sub-class of Thread.
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 2:
- Create a class on an interface or Runnable
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 3:
- Modify part1 or part 2 to handle any size array and any number
  of threads.

************************************/
import java.util.Random; 
import java.lang.Math; 

class PrimeThread extends Thread {
  private int[] array;
  private int startIndex;
  private int endIndex;
  private int id;

  public PrimeThread(int[] array, int startIndex, int endIndex, int i) {
    this.array = array;
    this.startIndex = startIndex;
    this.endIndex = endIndex;
    this.id = i + 1;
  }

  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }
  
  public void run() {
    System.out.println("This is thread #" + id + " starting out.");
    for (int i = startIndex; i <= endIndex; i++) {
      if (isPrime(array[i])) {
        System.out.println(array[i]);
      }
    }
    System.out.println("Thread #" + id + " done.");
  }
  
}

class Main {

  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }

  public static void main(String[] args) {
    System.out.println("Hello world!");

    // create instance of Random class 
    Random rand = new Random(); 

    int count = 1000;
    int[] array = new int[count];
    for (int i = 0; i < count; i++) 
    {
      array[i] = Math.abs(rand.nextInt());
    }

  // TODO - this is just sample code. you can remove it.
    int numThreads = 4;
    int segmentSize = array.length / numThreads;
    int remainingElements = array.length % numThreads;
    int startIndex = 0;
    int endIndex = -1;
    for (int i = 0; i < numThreads; i++) {
      startIndex = endIndex + 1;
      endIndex = startIndex + segmentSize - 1;
      if (i < remainingElements) {
        endIndex++;
      }
      PrimeThread thread = new PrimeThread(array, startIndex, endIndex, i);
      thread.start();
    }
  }
}
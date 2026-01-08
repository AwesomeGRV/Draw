"""
Text Evolution Simulator
Demonstrates evolutionary algorithm by generating target text through random mutations
"""

import string
import random
import time
import sys
from datetime import datetime


class TextEvolution:
    """Class to simulate text evolution using random mutations"""
    
    def __init__(self, target_text, mutation_rate=0.1, delay=0.1):
        """
        Initialize the text evolution simulator
        
        Args:
            target_text (str): The target text to evolve towards
            mutation_rate (float): Probability of mutation for each character
            delay (float): Delay between generations in seconds
        """
        self.target = target_text
        self.mutation_rate = mutation_rate
        self.delay = delay
        self.possible_characters = (
            string.ascii_lowercase + 
            string.digits + 
            string.ascii_uppercase + 
            ' .,!?;:-'
        )
        self.generation = 0
        self.start_time = None
        self.history = []
        
    def get_random_character(self):
        """Get a random character from the possible characters"""
        return random.choice(self.possible_characters)
    
    def create_initial_attempt(self):
        """Create the initial random attempt"""
        return ''.join(self.get_random_character() for _ in range(len(self.target)))
    
    def calculate_fitness(self, attempt):
        """
        Calculate fitness score based on correct characters
        
        Args:
            attempt (str): Current attempt string
            
        Returns:
            int: Number of correct characters
        """
        return sum(1 for i, char in enumerate(attempt) if i < len(self.target) and char == self.target[i])
    
    def mutate(self, attempt):
        """
        Mutate the current attempt to create the next generation
        
        Args:
            attempt (str): Current attempt string
            
        Returns:
            str: Mutated attempt string
        """
        next_attempt = list(attempt)
        
        for i in range(len(self.target)):
            if i >= len(next_attempt):
                next_attempt.append(self.get_random_character())
            elif next_attempt[i] != self.target[i]:
                # Mutate incorrect characters
                if random.random() < self.mutation_rate:
                    next_attempt[i] = self.get_random_character()
            else:
                # Keep correct characters
                next_attempt[i] = self.target[i]
        
        return ''.join(next_attempt)
    
    def display_progress(self, attempt, fitness):
        """Display current progress with statistics"""
        progress = (fitness / len(self.target)) * 100
        
        # Clear screen (works on most terminals)
        print('\033[2J\033[H', end='')
        
        print("Text Evolution Simulator")
        print("=" * 50)
        print(f"Target:    {self.target}")
        print(f"Attempt:   {attempt}")
        print(f"Fitness:   {fitness}/{len(self.target)} characters ({progress:.1f}%)")
        print(f"Generation: {self.generation}")
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            print(f"Time:      {elapsed:.1f} seconds")
            
            if self.generation > 0:
                rate = self.generation / elapsed
                print(f"Rate:      {rate:.1f} generations/second")
        
        print("-" * 50)
        
        # Show character comparison
        print("Comparison:")
        for i, (target_char, attempt_char) in enumerate(zip(self.target, attempt)):
            if target_char == attempt_char:
                print(f"{target_char}", end='')
            else:
                print(f"[{attempt_char}]", end='')
        print()
        
    def run(self):
        """Run the evolution simulation"""
        print("Starting text evolution...")
        print(f"Target: '{self.target}'")
        print(f"Mutation rate: {self.mutation_rate}")
        print(f"Delay: {self.delay}s")
        print("\nPress Ctrl+C to stop early\n")
        
        time.sleep(2)  # Give user time to read
        
        self.start_time = time.time()
        current_attempt = self.create_initial_attempt()
        
        try:
            while True:
                self.generation += 1
                fitness = self.calculate_fitness(current_attempt)
                
                # Store in history
                self.history.append({
                    'generation': self.generation,
                    'fitness': fitness,
                    'attempt': current_attempt
                })
                
                # Display progress
                self.display_progress(current_attempt, fitness)
                
                # Check if target is reached
                if fitness == len(self.target):
                    elapsed = time.time() - self.start_time
                    print(f"\nTarget matched!")
                    print(f"Generations: {self.generation}")
                    print(f"Time: {elapsed:.2f} seconds")
                    print(f"Average rate: {self.generation/elapsed:.1f} generations/second")
                    break
                
                # Create next generation
                current_attempt = self.mutate(current_attempt)
                time.sleep(self.delay)
                
        except KeyboardInterrupt:
            print(f"\n\nEvolution stopped by user at generation {self.generation}")
            print(f"Final fitness: {fitness}/{len(self.target)} characters")
            
    def get_statistics(self):
        """Get evolution statistics"""
        if not self.history:
            return None
            
        return {
            'total_generations': len(self.history),
            'final_fitness': self.history[-1]['fitness'],
            'target_length': len(self.target),
            'success_rate': (self.history[-1]['fitness'] / len(self.target)) * 100,
            'elapsed_time': time.time() - self.start_time if self.start_time else 0
        }


def get_user_input():
    """Get user input for evolution parameters"""
    print("Text Evolution Simulator")
    print("=" * 30)
    
    try:
        target = input("Enter target text: ").strip()
        if not target:
            print("Target text cannot be empty. Using default.")
            target = "Hello, World!"
            
        mutation_rate = input("Enter mutation rate (0.0-1.0, default 0.1): ").strip()
        try:
            mutation_rate = float(mutation_rate) if mutation_rate else 0.1
            if not 0 <= mutation_rate <= 1:
                raise ValueError("Mutation rate must be between 0 and 1")
        except ValueError:
            print("Invalid mutation rate. Using default 0.1")
            mutation_rate = 0.1
            
        delay = input("Enter delay between generations in seconds (default 0.1): ").strip()
        try:
            delay = float(delay) if delay else 0.1
            if delay < 0:
                raise ValueError("Delay cannot be negative")
        except ValueError:
            print("Invalid delay. Using default 0.1")
            delay = 0.1
            
        return target, mutation_rate, delay
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)


def main():
    """Main function to run the text evolution simulator"""
    try:
        target, mutation_rate, delay = get_user_input()
        
        # Create and run evolution
        evolution = TextEvolution(target, mutation_rate, delay)
        evolution.run()
        
        # Display final statistics
        stats = evolution.get_statistics()
        if stats:
            print(f"\nFinal Statistics:")
            print(f"Total Generations: {stats['total_generations']}")
            print(f"Final Fitness: {stats['final_fitness']}/{stats['target_length']}")
            print(f"Success Rate: {stats['success_rate']:.1f}%")
            print(f"Total Time: {stats['elapsed_time']:.2f} seconds")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
Multiplication Table Generator
Generates customizable multiplication tables with various output options
"""

def generate_multiplication_table(size=10, start=1):
    """
    Generates a multiplication table
    
    Args:
        size (int): Size of the table (default 10)
        start (int): Starting number (default 1)
    
    Returns:
        str: Formatted multiplication table as string
    """
    if size <= 0 or start <= 0:
        raise ValueError("Size and start must be positive integers")
    
    table_lines = []
    
    # Generate header row
    header = "     "  # Extra space for row numbers
    for col in range(start, start + size):
        header += f"{col:4}"
    table_lines.append(header)
    
    # Generate separator line
    separator = "    " + "-" * (size * 4)
    table_lines.append(separator)
    
    # Generate table rows
    for row in range(start, start + size):
        row_line = f"{row:2} |"
        for col in range(start, start + size):
            product = row * col
            row_line += f"{product:4}"
        table_lines.append(row_line)
    
    return "\n".join(table_lines)


def display_multiplication_table(size=10, start=1, save_to_file=False):
    """
    Displays and optionally saves a multiplication table
    
    Args:
        size (int): Size of the table
        start (int): Starting number
        save_to_file (bool): Whether to save to file
    """
    try:
        table = generate_multiplication_table(size, start)
        
        print(f"\nMultiplication Table ({size}x{size}, starting from {start}):")
        print("=" * 50)
        print(table)
        print("=" * 50)
        
        if save_to_file:
            filename = f"multiplication_table_{size}x{size}_from_{start}.txt"
            with open(filename, 'w') as f:
                f.write(f"Multiplication Table ({size}x{size}, starting from {start})\n")
                f.write("=" * 50 + "\n")
                f.write(table)
                f.write("\n" + "=" * 50 + "\n")
            print(f"Table saved to {filename}")
        
        return table
        
    except ValueError as e:
        print(f"Error: {e}")
        return None


def get_user_input():
    """Gets user input for table parameters"""
    print("Multiplication Table Generator")
    print("=" * 30)
    
    try:
        size = input("Enter table size (default 10): ").strip()
        size = int(size) if size else 10
        
        start = input("Enter starting number (default 1): ").strip()
        start = int(start) if start else 1
        
        save = input("Save to file? (y/n, default n): ").strip().lower()
        save_to_file = save in ['y', 'yes']
        
        return size, start, save_to_file
        
    except ValueError:
        print("Invalid input. Using defaults.")
        return 10, 1, False


def main():
    """Main function to run the multiplication table generator"""
    try:
        size, start, save_to_file = get_user_input()
        display_multiplication_table(size, start, save_to_file)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
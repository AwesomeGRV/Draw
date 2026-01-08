# Draw Programs Collection

A collection of educational Python programs demonstrating various programming concepts including graphics, algorithms, and data processing. Each program has been enhanced with proper error handling, user input validation, and improved user experience.

## Programs Included

### 1. Geometric Pattern Generator (`Turtle.py`)
Creates beautiful circular patterns using Python's turtle graphics library with customizable parameters.

**Features:**
- Customizable iterations, patterns, angles, and colors
- Interactive user input with validation
- Proper screen management and cleanup
- Error handling for graphics operations

**Usage:**
```bash
python Turtle.py
```

### 2. Multiplication Table Generator (`mathstables.py`)
Generates customizable multiplication tables with various output options.

**Features:**
- Customizable table size and starting number
- Formatted output with proper alignment
- Option to save tables to file
- Input validation and error handling

**Usage:**
```bash
python mathstables.py
```

### 3. Snowflake Pattern Generator (`snow.py`)
Creates intricate snowflake patterns using turtle graphics with customizable parameters.

**Features:**
- Customizable number of branches and colors
- Random color variations for visual appeal
- Class-based architecture for better organization
- Proper screen management and cleanup

**Usage:**
```bash
python snow.py
```

### 4. Text Evolution Simulator (`text.py`)
Demonstrates evolutionary algorithms by generating target text through random mutations.

**Features:**
- Configurable mutation rates and delays
- Real-time progress tracking with statistics
- Visual comparison of target vs. current attempt
- Performance metrics and generation history

**Usage:**
```bash
python text.py
```

### 5. Main Launcher (`main.py`)
A unified interface to run all programs individually or in sequence.

**Features:**
- Interactive menu system
- Dependency checking
- Error handling for all programs
- Option to run all programs sequentially

**Usage:**
```bash
python main.py
```

## Requirements

### System Requirements
- Python 3.6 or higher
- Operating System: Windows, macOS, or Linux

### Python Libraries
- `turtle` - For graphics programs (included with Python)
- `random` - For randomization (included with Python)
- `string` - For string operations (included with Python)
- `time` - For timing operations (included with Python)
- `sys` - For system operations (included with Python)

All required libraries are part of the Python standard library, so no additional installation is needed.

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd draw
```

2. Ensure you have Python 3.6+ installed:
```bash
python --version
```

3. Run the main launcher:
```bash
python main.py
```

## Usage Instructions

### Running Individual Programs
Each program can be run individually by executing its Python file directly:

```bash
# Run the geometric pattern generator
python Turtle.py

# Run the multiplication table generator
python mathstables.py

# Run the snowflake pattern generator
python snow.py

# Run the text evolution simulator
python text.py
```

### Using the Main Launcher
The recommended way to use this collection is through the main launcher:

```bash
python main.py
```

This will display an interactive menu where you can:
- Choose any program to run individually
- Run all programs in sequence
- Exit the launcher

### Program-Specific Instructions

#### Geometric Pattern Generator
- Enter the number of iterations (default: 100)
- Enter the number of patterns (default: 5)
- Enter angle multiplier (default: 9)
- Enter turn angle (default: 180)
- The graphics window will open and display the pattern
- Click on the window to close it

#### Multiplication Table Generator
- Enter table size (default: 10)
- Enter starting number (default: 1)
- Choose whether to save to file (optional)
- The table will be displayed in the console

#### Snowflake Pattern Generator
- Enter number of branches (default: 8)
- Enter branch length (default: 30)
- Enter background color (default: grey)
- Optionally specify custom colors
- The snowflake will be drawn in a graphics window

#### Text Evolution Simulator
- Enter target text to evolve towards
- Enter mutation rate (0.0-1.0, default: 0.1)
- Enter delay between generations (default: 0.1 seconds)
- Watch as the text evolves towards the target
- Press Ctrl+C to stop early

## File Structure

```
draw/
├── main.py              # Main launcher program
├── Turtle.py            # Geometric pattern generator
├── mathstables.py       # Multiplication table generator
├── snow.py              # Snowflake pattern generator
├── text.py              # Text evolution simulator
├── README.md            # This documentation file
├── requirements.txt     # Dependencies list
└── venv/               # Virtual environment (if created)
```

## Error Handling

All programs include comprehensive error handling for:
- Invalid user input
- Missing dependencies
- Graphics window operations
- File operations
- Keyboard interrupts

If an error occurs, the program will display a helpful message and either continue with default values or exit gracefully.

## Customization

Each program is designed to be easily customizable:

### Adding New Programs
1. Create a new Python file with a `main()` function
2. Add an entry to the `programs` dictionary in `main.py`
3. Follow the existing code patterns for consistency

### Modifying Existing Programs
- All programs use clear function and variable names
- Documentation is provided for all major functions
- Configuration options are easily accessible at the top of each file

## Educational Value

This collection demonstrates various programming concepts:

### Graphics Programming
- Turtle graphics basics
- Screen management and cleanup
- Color and drawing operations

### Algorithms
- Evolutionary algorithms
- Pattern generation
- Mathematical computations

### Software Engineering
- Error handling and validation
- User input processing
- Code organization and structure
- Documentation practices

### User Experience
- Interactive menus
- Progress tracking
- Visual feedback
- Graceful error recovery

## Troubleshooting

### Common Issues

**Graphics programs don't open:**
- Ensure you're running Python with graphics support
- On some systems, you may need to run from terminal instead of IDE
- Check that tkinter is installed (required for turtle)

**Import errors:**
- Ensure all files are in the same directory
- Check Python version compatibility
- Run from the correct directory

**Performance issues:**
- Reduce iteration counts for pattern generators
- Increase delays for text evolution if needed
- Close other graphics-intensive applications

### Getting Help

If you encounter issues:
1. Check that all files are present and in the correct directory
2. Ensure Python 3.6+ is installed
3. Try running individual programs first
4. Check the error messages for specific guidance

## Contributing

This project is designed for educational purposes. When making changes:
- Follow existing code style and patterns
- Add appropriate error handling
- Update documentation for new features
- Test all changes thoroughly

## License

This project is provided for educational purposes. Feel free to use, modify, and distribute for learning and teaching.

## Version History

- **v2.0** - Enhanced versions with proper error handling, user input validation, and improved user experience
- **v1.0** - Original basic implementations

---

**Note:** This collection is designed to be a learning resource for Python programming concepts. Each program demonstrates different aspects of programming while maintaining clean, readable code and good software engineering practices.

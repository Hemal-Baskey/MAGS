# MCQ Automatic Grading System

This system automatically grades multiple-choice answer sheets using computer vision.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Prepare your answer sheet:
   - The system expects a 5x5 grid (5 questions, 5 choices each)
   - The answer sheet should have two main rectangles:
     - Main answer area
     - Grade display area

## Usage

1. Place your answer sheet image in the project directory
2. Update the `pathImage` variable in `main.py` with your image path
3. Run the program:
```bash
python main.py
```

## Controls

- Press 'q' to quit
- Press 's' to save the processed image
- The saved images will be stored in the 'Scanned' directory

## Features

- Automatic answer sheet detection
- Multiple-choice answer grading
- Real-time processing
- Score calculation and display
- Image saving capability

# MCQ Automatic Grading System

A Python-based Optical Mark Recognition (OMR) system that automatically scans and grades multiple-choice answer sheets using computer vision techniques.

## 🎯 Features

- **Automatic Answer Detection**: Detects marked bubbles on answer sheets using pixel analysis
- **Perspective Correction**: Automatically corrects skewed or rotated answer sheets
- **Real-time Processing**: Live processing with visual feedback
- **Automatic Grading**: Compares detected answers against answer key and calculates scores
- **Visual Results**: Displays processing steps and final results in a clean GUI
- **Save Functionality**: Save processed results as images
- **Error Handling**: Robust error handling for various input conditions

## 📋 Requirements

- Python 3.7+
- OpenCV 4.x
- NumPy

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/omr-scanner.git
   cd omr-scanner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Usage

1. **Prepare your answer sheet image**
   - Place your scanned answer sheet image in the project directory
   - Update the `pathImage` variable in `main.py` to point to your image

2. **Configure the answer key**
   ```python
   # In main.py, update these variables:
   questions = 5        # Number of questions
   choices = 5          # Number of choices per question
   ans = [1, 2, 0, 2, 3]  # Correct answers (0-indexed)
   ```

3. **Run the scanner**
   ```bash
   python main.py
   ```

### Controls

- **'s' key**: Save the current scan result
- **'q' key**: Quit the application

## 🏗️ Project Structure

```
omr-scanner/
├── main.py              # Main OMR scanner application
├── utils.py             # Utility functions for image processing
├── OMR_Main.py          # Alternative main implementation
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── omr_img1.jpg        # Sample answer sheet image
└── Scanned/            # Directory for saved scan results
    ├── myImage0.jpg
    ├── myImage1.jpg
    └── ...
```

## 🔧 Configuration

### Answer Sheet Format

The system is designed for answer sheets with:
- Multiple choice questions (A, B, C, D, E)
- Rectangular answer grid
- Clear bubble markings

### Customization

You can customize the following parameters in `main.py`:

```python
heightImg = 350      # Height of processed image
widthImg = 300       # Width of processed image
questions = 5        # Number of questions
choices = 5          # Number of choices per question
ans = [1, 2, 0, 2, 3]  # Answer key (0-indexed)
```

## 🛠️ How It Works

1. **Image Preprocessing**
   - Load and resize the input image
   - Convert to grayscale and apply Gaussian blur
   - Detect edges using Canny edge detection
   - Apply adaptive thresholding

2. **Contour Detection**
   - Find contours in the processed image
   - Identify rectangular contours (answer grid and grade area)
   - Extract corner points for perspective transformation

3. **Perspective Correction**
   - Apply perspective transformation to get top-down view
   - Separate answer grid and grade area

4. **Answer Detection**
   - Split the answer grid into individual bubbles
   - Count non-zero pixels in each bubble
   - Determine marked answers based on pixel density

5. **Grading**
   - Compare detected answers with the answer key
   - Calculate percentage score
   - Display results with visual indicators

## 📸 Sample Output

The application displays:
- Original image
- Grayscale and edge detection results
- Contour detection visualisation
- Perspective-corrected answer grid
- Final graded result with score

# MPIN Validator

A robust MPIN (Mobile PIN) validation system that checks for common patterns, demographic information, and keypad patterns to ensure strong and secure MPINs.

## Overview

The MPIN Validator is a web application that helps users create strong and secure MPINs by analyzing various patterns and combinations. It provides real-time feedback on MPIN strength and detailed explanations for weak patterns detected.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Key Libraries**:
  - `streamlit`: For web interface
  - `datetime`: For date handling
  - `typing`: For type hints
  - `re`: For regular expressions

## Methodology

The validator uses a comprehensive approach to check MPIN strength:

### 1. Commonly Used Patterns
- Keypad patterns (horizontal, vertical, diagonal, corner)
- Arithmetic progressions
- Geometric progressions
- Repetitive digit
- Repetitive Pair/Sequence
- Ascending sequences
- Descending sequences

### 2. Demographic Patterns
- Self Date of birth patterns
- Spouse's date of birth patterns
- Wedding anniversary patterns
- Combined date patterns
- Year Patterns

### 3. Calculation
- Base strength: 100 points
- Deductions based on detected patterns
- Threshold: 70 points to be a strong MPIN

## Features

### 1. Input Validation
- Support for 4-digit and 6-digit MPINs
- Date format validation

### 2. Pattern Detection
- Comprehensive pattern analysis
- Multiple pattern categories
- Real-time detection

### 3. Visual Feedback
- Color-coded strength meter
- Detailed pattern explanations
- Strength percentage display

### 4. User Interface
- Clean, two-column layout
- Real-time validation
- Responsive design
- Intuitive input fields

## Test Cases

| Test Case | Category | Outcome | Reason / Notes |
|-----------|----------|---------|----------------|
| `123321` | Keypad Horizontal | Weak | Repeating horizontal sequence; visually traceable, easy to guess |
| `123123` | Keypad Horizontal / Repeated Sequence | Weak | Horizontal flow, repeated part (123); very predictable |
| `2580` | Keypad Vertical | Weak | Straight vertical on keypad; used often |
| `147147` | Keypad Vertical / Repeated Sequence | Weak | Repeats vertical pattern; easily guessable |
| `147741` | Keypad Vertical (mirrored) | Weak | Mirrored vertical sequence; predictable keypad pattern |
| `357357` | Keypad Diagonal / Repeated | Weak | Common diagonal pattern repeated; easy to visualize |
| `357753` | Keypad Diagonal / Reversed | Weak | Variation of diagonal pattern; remains guessable |
| `1793` | Keypad Corner | Weak | Uses 4 keypad corners; familiar to attackers |
| `1397` | Keypad Corner | Weak | Another keypad corner path; predictable |
| `1111` | Repetitive | Very Weak | All digits same; most guessed PIN |
| `1234` | Ascending / Arithmetic | Very Weak | Most commonly used PIN worldwide |
| `4321` | Descending / Arithmetic | Very Weak | Reverse of most common PINs; equally weak |
| `8421` | Geometric | Weak | Numeric steps suggest geometric progression |
| `1248` | Geometric | Weak | Follows a multiplying pattern; keyboard visible too |
| `121212` | Repeated Pair/Sequence | Weak | Alternating two-digit repetition is highly guessable |
| `748650` | Strong MPIN (Random) | Strong | Appears random, no pattern or date; hard to guess |
| `2702` | DOB Match (DDMM) | Weak | Likely birthday (27-02-2004); easy to social-engineer |
| `042702` | DOB Pattern Subsequence | Weak | Date format typical in U.S. and systems; common guess |
| `202111` | DOB Pattern (YYYY + MM) | Weak | Easily linked to a year+month date pattern |
| `2102` | Combined Date (DD + MM) | Weak | Matches date combinations; very typical |
| `abcd` | Non-Numeric Input | Invalid | Contains letters; MPIN must be numeric only |
| `123a` | Non-Numeric Input | Invalid | Alphanumeric mix not allowed |
| `` (empty string) | Missing Input | Invalid | No PIN provided |

## Screenshots

### Main Interface
![Main Interface](https://github.com/user-attachments/assets/10db2915-104a-4c67-8f22-8d350ea48b29)

### Validation Results
![Validation Results](https://github.com/user-attachments/assets/d9bd60b2-7428-4b94-bf42-1c40bc344ff1)

### Error Handling
![Error Handling](https://github.com/user-attachments/assets/9e21792a-1415-4c5e-ae48-4f4a3e0ed0d5)


## Research Links
1. [DataGenetics PIN Analysis](http://www.datagenetics.com/blog/september32012/index.html)
2. [Most Common PIN Codes](https://informationisbeautiful.net/visualizations/most-common-pin-codes/)
3. [Common Credentials](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/four-digit-pin-codes-sorted-by-frequency-withcount.csv)

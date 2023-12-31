# Calculus Project

## Introduction
The Calculus project focuses on processing and analyzing raw data from mid-term and final exams.

## Live Demo
Experience the functionality of this project in action! Visit our live demo at [Lavaskiller's Calculus Demo](https://lavaskiller.pythonanywhere.com/). Explore the features and see how it works in real-time.

## File Structure
- `sum_data/`
  - `grade.txt`: Raw mid-term exam scores. Requires header addition.
  - `grade2.txt`: Raw final exam scores. Requires header addition.
  - `final.txt`: The combined score file created by sum.py. Requires header addition.
  - `sum.py`: Script to merge mid-term and final exam scores into `final.txt`.
- `calc.py`: Calculates information from the dataset for web display.
- `sayings.txt`: Stores messages for web display.
- `grade.txt`: Raw mid-term exam scores. Includes headers.
- `grade2.txt`: Raw final exam scores. Includes headers.
- `final.txt`: Combined scores from mid-term and final exams. Includes headers.
- `flask_app.py`: Show results by web page.

## Usage
1. Ensure `grade.txt` and `grade2.txt` in `sum_data/`.
2. Run `sum.py` to create `final.txt` with combined scores.
3. Add header to `grade.txt`, `grade2.txt`, `final.txt` in `sum_data/` and save it local `/`.
4. Use `calc.py` for further data processing and web display preparation.
5. Edit `sayings.txt` to change or add web display messages.
6. run `flask_app.py` to make webpages local on your notebook. For this you need to uncomment 102-103 of `flask_app.py`.

## License
This project is licensed under the [MIT License](https://github.com/lavaskiller/calculus/blob/main/LICENSE).

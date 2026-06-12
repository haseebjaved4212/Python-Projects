# Modern Google Translate GUI

A sleek and modern desktop application for language translation, built using Python. This project utilizes the `customtkinter` library for a beautiful graphical user interface and the `deep-translator` library to interface with Google Translate.

## Features

- **Modern User Interface**: Built with `customtkinter` to provide a clean, modern, and dark/light mode aware application window.
- **Extensive Language Support**: Translates between numerous languages supported by Google Translate.
- **Auto Detect**: Automatically detects the source language of the input text.
- **Quick Controls**: Convenient "Clear" and "Copy" buttons for both source and translated text boxes.
- **Asynchronous Feel**: Displays a "Translating..." state during the translation process to keep the user informed.
- **Error Handling**: Graceful error handling with popup messages if translation fails (e.g., due to no internet connection).

## Prerequisites

Before running the application, ensure you have Python installed on your system. You will also need to install the required dependencies.

The main libraries used are:
- `customtkinter`: For the modern GUI components.
- `deep-translator`: For performing the actual language translation via Google Translate.
- `tkinter`: (Included with standard Python installations)

## Installation

1. **Clone or Download the Repository:**
   Download the source code to your local machine.

2. **Navigate to the Project Directory:**
   ```bash
   cd 08-Google-Translate-With-GUI
   ```

3. **Install Dependencies:**
   Use `pip` to install the required libraries:
   ```bash
   pip install customtkinter deep-translator
   ```

## Usage

To start the application, simply run the `main.py` script from your terminal or command prompt:

```bash
python main.py
```

### How to Translate
1. Select the **Source Language** from the left dropdown (or leave it as "Auto Detect").
2. Select the **Target Language** from the right dropdown.
3. Type or paste the text you want to translate into the left text box.
4. Click the **Translate ➔** button in the middle.
5. The translated text will appear in the right text box.
6. Use the **Clear** or **Copy** buttons below the text boxes as needed.

## Project Structure

- `main.py`: The main entry point of the application containing the GUI layout and translation logic.

## License

This project is open-source and available for educational and personal use.

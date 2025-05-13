# SortMate

📂 SortMate

SortMate is a desktop application that automatically organizes scanned PDFs and image files by reading their content with OCR and sorting them into folders based on user-defined keywords. Whether you're a busy professional, student, or just trying to keep your digital life tidy, SortMate helps eliminate the manual hassle of document management.
🚀 Features

    🔍 OCR-Powered Sorting — Uses Tesseract OCR to read scanned documents and extract text, even from rotated or skewed scans.

    🗂️ Custom Keyword Filters — Create sorting rules by assigning keywords to folder destinations.

    📁 Auto File Organization — Instantly sorts documents into appropriate folders based on matches.

    🧠 Subfolder Support — Add item-level filters to create dynamic subfolders based on specific content.

    💡 Case-Insensitive Matching — Keywords work regardless of letter case (e.g., “Business” = “BUSINESS” = “business”).

    🖼️ Supports PDFs and Images — Works with most image file types and PDF scans.

    ⚙️ User-Friendly GUI — Built with a clean, easy-to-navigate Tkinter interface.

🛠️ Installation & Setup
Step 1: Install Tesseract OCR

To enable text recognition:

    Download the installer from 👉 Tesseract OCR (UB Mannheim)

    Complete the installation.

    Copy the full path to tesseract.exe and paste it into SortMate’s setup field.

Step 2: Select Source Folder

Choose the folder that contains your scanned documents:

    Click the Browse button on the home screen.

    Navigate to and select your folder of PDFs/images.

Step 3: Set Up Sorting Directories

Configure how documents should be sorted:

    Go to Settings.

    Add sorting rules by:

        Naming a category (e.g., "Receipts", "Business").

        Selecting a destination folder.

        Entering keywords that trigger a match.

Step 4: Add Item Filters (Optional)

Create subfolder rules:

    In Settings > Item Filters, add keywords for more specific sorting.

    Files matching these will go into subfolders named after the keyword.

Step 5: Start Sorting

Once setup is complete:

    Click Run.

    SortMate will scan all files, extract text, and move them into folders based on your rules.

💡 Pro Tips

    You can update keywords and folders anytime.

    Works best with clean scans (300 DPI recommended).

    Tesseract can read text in any orientation—no need to rotate files.

    Ensure Tesseract is accessible in your system PATH or manually enter its path.

    Keywords are not case-sensitive.

🧩 Built With

    Python

    Tkinter for GUI

    Tesseract OCR for text extraction

    Pillow for image handling

🧑‍💻 Why I Built It

I archive all my mail and documents digitally, but sorting them manually was eating up 45–60 minutes each week. SortMate is my personal solution—designed to take that task off my plate. Now, anyone can set up easy, customizable rules for organizing files in seconds. It’s practical, efficient, and adaptable for almost any workflow.
📬 Who Is It For?

    Freelancers & business owners managing digital paperwork

    Students organizing coursework and submissions

    Designers keeping track of contracts and invoices

    Everyday users who just want their files in order

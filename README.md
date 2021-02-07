# ParallelOCR
A Python OCR implementation for pdf text extraction using Poppler and Tesseract

Features:
- Supports both text-readable and non text-readable (scanned) documents
- Multiprocessing implemented with three different performance profiles to optimize execution speeds
- Basic text cleaning
- Export data in .docx or .csv format

Requirements:
1) If running on Windows (without Docker), download Poppler from http://blog.alivate.com.au/poppler-windows/ and add the /bin folder to PATH (required for pdftoppm)
2) If running on Windows (without Docker), download Tesseract from https://github.com/UB-Mannheim/tesseract/wiki and add the root folder to PATH (required by pytesseract)

# ParallelOCR
A Python OCR implementation for pdf text extraction using Poppler and Tesseract

Features:
- Supports both text-readable and non text-readable (scanned) documents
- Multiprocessing implemented with three different performance profiles to optimize execution speeds
- Basic text cleaning
- Export data in csv format

Requirements:
1) Download Poppler from http://blog.alivate.com.au/poppler-windows/ and add the /bin folder to env variable "popplerPath"
2) Download Tesseract from https://github.com/UB-Mannheim/tesseract/wiki and add the root folder to env variable "tesseractPath"

# Technical Documentation for the Transcription and Summarization System

## Table of Contents

1. [Introduction](#introduction)
2. [System Workflow](#system-workflow)
   - [Video Processing and Transcription](#video-processing-and-transcription)
   - [PDF Processing and Summarization](#pdf-processing-and-summarization)
3. [Chunking Techniques](#chunking-techniques)
4. [Summarization Process](#summarization-process)
5. [Output Format](#output-format)
6. [Tools and Dependencies](#tools-and-dependencies)

---

## Introduction

This documentation describes a system for processing input files (videos or PDFs) to produce concise summaries. The system integrates multiple workflows, including transcription, PDF creation, text chunking, and summarization, leveraging advanced AI models for efficient processing.

---

## System Workflow

### Overview

The system supports multiple input scenarios:

- Videos (`.mp4` files) requiring transcription and conversion to text before summarization.
- PDFs (`.pdf` files) processed directly for summarization.

The workflow adapts to the input type, ensuring flexibility and compatibility for diverse use cases.

---

### Video Processing and Transcription

1. **Input Handling**  
   Videos are retrieved from the designated folder (`vids` directory). Only files with `.mp4` extensions are processed.

2. **Transcription**  
   The video is transcribed into text using the Whisper model. The transcription is saved as a `.txt` file in the input folder.

3. **PDF Creation**  
   The transcribed text file is converted into a `.pdf` file. This step ensures uniformity in the input format, allowing the system to process video and PDF files using the same summarization logic.

---

### PDF Processing and Summarization

1. **PDF Extraction**  
   Text is extracted from each PDF file using a PDF utility library. The extracted content is passed to the summarization module.

2. **Summarization**  
   The text content is chunked into manageable parts, summarized using a Large Language Model (LLM), and consolidated into a final summary. Detailed chunking and summarization techniques are described in later sections.

3. **Output**  
   The final summary is written to a `.txt` file in the output directory.

---

## Chunking Techniques

To manage large text inputs, the content is divided into smaller chunks based on:

- **Delimiters**: Text is split at logical boundaries, such as sentences or paragraphs, using a specified delimiter (e.g., periods).
- **Token Limit**: Each chunk's size is restricted to the token limit supported by the LLM.
- **Adaptive Resizing**: The number and size of chunks are adjusted dynamically based on the required level of detail in the summary.

Chunks exceeding the token limit are either truncated with an ellipsis or split further to ensure compliance with model constraints.

---

## Summarization Process

### Steps

1. **Instruction Setup**  
   The system uses predefined instructions, including a system message guiding the LLM to generate a concise summary. Optional additional instructions can be provided to customize the summarization.

2. **Iterative Summarization**  
   Each chunk is summarized individually. If recursive summarization is enabled, intermediate summaries are concatenated and summarized again to produce a more concise output.

3. **Model and Parameters**  
   The summarization is performed using the `llama-3.1-70b-versatile` model. Parameters include:
   - **Detail Level**: Controls the output length by adjusting the number of chunks to summarize.
   - **Model Temperature**: Set to `0` for deterministic outputs.

---

## Output Format

The final summaries are saved as plain text files in the output directory. The naming convention appends `_summary` to the original file name. For example:

- Input: `report.pdf`
- Output: `report_summary.txt`

---

## Tools and Dependencies

### Libraries and Tools

1. **Whisper**

   - Transcription of videos into text.
   - Dependency: `whisper` Python library.

2. **PDF Utilities**

   - Text extraction from PDFs and PDF creation from text files.
   - Dependency: `pypdf` and `FPDF` libraries.

3. **Groq API**

   - LLM-based summarization using the `llama-3.1-70b-versatile` model.
   - Requires an API key for authentication.

4. **Environment Variables**
   - Secure API key management using `.env` files and the `dotenv` library.

### Additional Utilities

- **Tokenization and Chunking**: Handles large text inputs and ensures compatibility with model constraints.
- **File Handling**: Manages directories for input (`files/input` and `vids`) and output (`files/output`).

---

## Conclusion

This transcription and summarization system provides a seamless pipeline for processing both videos and PDFs. Its modular design and robust handling of diverse inputs make it suitable for applications requiring efficient text summarization at scale. The integration of cutting-edge tools, such as Whisper and Groq, ensures high accuracy and adaptability.

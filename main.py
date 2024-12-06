import os
from summarizer.pdf_utils import convert_pdf_to_text, create_pdf
from summarizer.summarizer import Summarizer
from dotenv import load_dotenv
from summarizer.transcriber import transcribe_video

load_dotenv()




def main():
    # Load your OpenAI API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Please set the GROQ_API_KEY environment variable.")

    # Initialize the summarizer
    summarizer = Summarizer(api_key=api_key)

    # Directories
    input_dir = os.path.join("files", "input")
    output_dir = os.path.join("files", "output")

    input_dir_vids = os.path.join("vids")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    vids = [f for f in os.listdir(input_dir_vids) if f.lower().endswith(".mp4")]

    if not vids:
        print(f"No video files found in {input_dir_vids}.")
        print("processing pdfs")

    else:
        print("processing videos")
        for vid in vids:
            video_path = os.path.join(input_dir_vids, vid)
            print(f"Processing {vid}...")
            transcribe_video(video_path)
            print(f"Transcription written to 'transcription.txt'\n")
            create_pdf(f"files/input/{vid}", f"files/input/{vid}.pdf")
            print(f"PDF created from transcription.txt\n")

    # Get a list of PDF files in the input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"No PDF files found in {input_dir}.")
        return

    for pdf_filename in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_filename)
        print(f"Processing {pdf_filename}...")

        # Extract text from the PDF
        text = convert_pdf_to_text(pdf_path)

        # Summarize the text
        summary = summarizer.summarize(text, detail=0.2, verbose=True)

        # Output file path
        summary_filename = f"{os.path.splitext(pdf_filename)[0]}_summary.txt"
        output_path = os.path.join(output_dir, summary_filename)

        # Write the summary to a file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"Summary written to {output_path}\n")


if __name__ == "__main__":
    main()

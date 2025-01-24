import os
import tempfile
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyBtpKzAxx2pwMQ1eMO_jtRxk28rRaglVc0")

# Define the prompt template for book analysis
PROMPT_TEMPLATE = """
Analyze the uploaded image to extract details about the book. Provide the following information:
- Title of the book.
- Author(s) of the book.
- ISBN (if available).
- Suggestions for similar books.
- Prices from different platforms.

Ensure the response is structured and easy to read. If the image is not a valid book cover, respond with: "ERROR: Invalid book image."
"""

def analyze_book(image_path):
    """
    Analyze the uploaded book image using the Gemini API.
    """
    try:
        # Upload the image using Gemini API
        uploaded_file = genai.upload_file(path=image_path, display_name="Uploaded Book Image")
        print(f"Uploaded file URI: {uploaded_file.uri}")

        # Generate content using the Gemini API
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        response = model.generate_content([uploaded_file, PROMPT_TEMPLATE])

        if response and response.text:
            print("Analysis Results:")
            print(response.text)
            return response.text
        else:
            print("Error: No response from Gemini API.")
            return "ERROR: Failed to analyze the book image."
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return f"ERROR: {str(e)}"

def main():
    """
    Main function to handle input and analyze the image.
    """
    image_path = input("Enter the path to the book image: ").strip()
    if not os.path.exists(image_path):
        print("ERROR: File does not exist. Please provide a valid path.")
        return

    # Analyze the book image
    result = analyze_book(image_path)
    print("\nFinal Result:\n", result)

if __name__ == "__main__":
    main()

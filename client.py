import argparse
from openai import OpenAI
from termcolor import colored

from src.config import MODEL

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1/",
    api_key="lit",
)

def send_image_for_processing(input_image_path: str, prompt: str, patient_info: str):
    """Send an image to the server to generate a skin care recommendation."""

    image_url = f"file://{input_image_path}"

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"Patient Information: {patient_info}"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image_url": image_url,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        stream=True,
        max_tokens=256,
    )
    print(colored("Processing image and generating skin care recommendation...", "yellow"))
    for chunk in stream:
        print(colored(chunk.choices[0].delta.content or "", "green"), end="")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send an image to DermaTech for skin care recommendation."
    )
    parser.add_argument("-i", "--image", required=True, help="Path to the input image")
    parser.add_argument(
        "-p", "--prompt", help="Specific skin concern or question", default="Analyze this skin image and provide recommendations."
    )
    parser.add_argument(
        "--age", type=int, required=True, help="Patient's age"
    )
    parser.add_argument(
        "--gender", choices=["Male", "Female", "Other"], required=True, help="Patient's gender"
    )
    parser.add_argument(
        "--skin-type", choices=["Normal", "Dry", "Oily", "Combination", "Sensitive"], required=True, help="Patient's skin type"
    )

    args = parser.parse_args()
    patient_info = f"Age: {args.age}, Gender: {args.gender}, Skin Type: {args.skin_type}"
    send_image_for_processing(args.image, args.prompt, patient_info)
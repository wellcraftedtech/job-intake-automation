import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def load_prompt():
    """Reads the system prompt from file."""
    try:
        with open("extraction_prompt.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        print("Error: extraction_prompt.txt not found.")
        return None

def load_email(filepath):
    """Reads the email content from a file."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return None

def extract_with_gpt(email_text, api_key):
    """Sends the email text to GPT for extraction."""
    client = OpenAI(api_key=api_key)
    
    system_prompt = load_prompt()
    if not system_prompt:
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_text}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return None

def calculate_quote(job_data):
    """Calculates a quote based on the extracted job data."""
    if not job_data:
        return None

    # Base Rates
    rates = {
        "Court Filing": 150,
        "Process Service": 120,
        "Occupancy Check": 180,
        "Enforcement": 350,
        "Lockout": 350,
        "Field Call": 150,
        "Other": 0
    }

    job_type = job_data.get("job_type", "Other")
    base_price = rates.get(job_type, 0)
    
    # Surcharges
    urgency_mult = 1.5 if job_data.get("urgency") == "Urgent" else 1.0
    
    surcharges = 0
    
    # Complexity Surcharge
    if job_data.get("complexity") == "High":
        surcharges += 100
    
    # Address check (Simplified: if postcode is valid and outside metro ranges)
    # This is a mock rule for the POC
    address = job_data.get("service_address")
    if address and address.get("postcode"):
        try:
            pc = int(address["postcode"])
            # Rough Metro Ranges for Syd/Mel
            is_metro = (2000 <= pc <= 2234) or (3000 <= pc <= 3207)
            if not is_metro:
                surcharges += 80 # Regional/Extended
        except ValueError:
            pass # Invalid postcode, ignore

    total = (base_price * urgency_mult) + surcharges
    
    return {
        "base_price": base_price,
        "urgency_multiplier": urgency_mult,
        "surcharges": surcharges,
        "total": round(total, 2),
        "currency": "AUD"
    }

def save_results(job_data, quote_data, original_filename, output_folder="extracted_jobs"):
    """Saves the result to a JSON file."""
    if not job_data:
        return

    os.makedirs(output_folder, exist_ok=True)
    
    output_data = {
        "source_file": original_filename,
        "extraction_timestamp": datetime.now().isoformat(),
        "job_details": job_data,
        "auto_quote": quote_data
    }
    
    # Create output filename based on input filename
    base_name = os.path.basename(original_filename).replace(".txt", ".json")
    output_path = os.path.join(output_folder, base_name)
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Saved extracted data to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Extract job details from email.")
    parser.add_argument("--email", help="Path to email text file")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return

    if args.email:
        print(f"Processing {args.email}...")
        email_text = load_email(args.email)
        if email_text:
            json_response = extract_with_gpt(email_text, api_key)
            if json_response:
                try:
                    job_data = json.loads(json_response)
                    quote_data = calculate_quote(job_data)
                    save_results(job_data, quote_data, args.email)
                except json.JSONDecodeError:
                    print("Error: Failed to parse JSON response from Claude.")
                    print("Raw response:", json_response)

if __name__ == "__main__":
    main()

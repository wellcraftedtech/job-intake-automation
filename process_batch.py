import os
import json
import pandas as pd
import argparse
from extract_job import load_email, extract_with_gpt, calculate_quote, save_results
from dotenv import load_dotenv

load_dotenv()

def process_batch(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print(f"Input folder {input_folder} not found.")
        return

    os.makedirs(output_folder, exist_ok=True)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        return

    files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    results_list = []

    print(f"Found {len(files)} emails to process.")

    for i, filename in enumerate(files):
        print(f"[{i+1}/{len(files)}] Processing {filename}...")
        filepath = os.path.join(input_folder, filename)
        
        email_text = load_email(filepath)
        if not email_text:
            continue
            
        json_response = extract_with_gpt(email_text, api_key)
        
        if json_response:
            try:
                job_data = json.loads(json_response)
                quote_data = calculate_quote(job_data)
                
                # Save individual JSON
                save_results(job_data, quote_data, filepath, output_folder)
                
                # Add to summary list
                flat_record = {
                    "File": filename,
                    "Client": job_data.get("client_name"),
                    "Job Type": job_data.get("job_type"),
                    "Due Date": job_data.get("due_date"),
                    "Urgency": job_data.get("urgency"),
                    "Quote Total": quote_data["total"] if quote_data else 0,
                    "Status": "Processed"
                }
                results_list.append(flat_record)
                
            except json.JSONDecodeError:
                print(f"Failed to parse extract for {filename}")
                results_list.append({
                    "File": filename,
                    "Status": "Error - JSON Parse"
                })
        else:
            print(f"Failed to get response for {filename}")
            results_list.append({
                "File": filename,
                "Status": "Error - API"
            })

    # Save summary CSV
    if results_list:
        df = pd.DataFrame(results_list)
        csv_path = os.path.join(output_folder, "batch_summary.csv")
        df.to_csv(csv_path, index=False)
        print(f"\nBatch processing complete. Summary saved to {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="sample_emails", help="Input folder of text files")
    parser.add_argument("--output", default="extracted_jobs", help="Output folder for JSON/CSV")
    args = parser.parse_args()
    
    process_batch(args.input, args.output)

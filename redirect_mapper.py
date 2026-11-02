import csv

def generate_redirect_map(old_urls_file, new_urls_file, output_file):
    """
    Generates a 301 redirect map from old and new URL lists.

    Args:
        old_urls_file (str): Path to a CSV file with old URLs (column 'old_url').
        new_urls_file (str): Path to a CSV file with new URLs (column 'new_url').
        output_file (str): Path to save the generated redirect map CSV.
    """
    old_urls = {}
    new_urls = {}

    # Read old URLs from CSV
    try:
        with open(old_urls_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                if 'old_url' in row and row['old_url']:
                    # Simple mapping: assume order or a common identifier if available
                    # For a real-world scenario, you'd need a more robust matching logic
                    old_urls[row['old_url']] = None # Placeholder for new URL mapping
    except FileNotFoundError:
        print(f"Error: Old URLs file not found at {old_urls_file}")
        return
    except Exception as e:
        print(f"Error reading {old_urls_file}: {e}")
        return

    # Read new URLs from CSV
    try:
        with open(new_urls_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for i, row in enumerate(reader):
                if 'new_url' in row and row['new_url']:
                    # Assuming new URLs are in the same order as old URLs for this example
                    # In a real scenario, you'd match based on content, slug, or ID
                    if i < len(old_urls):
                        old_key = list(old_urls.keys())[i]
                        old_urls[old_key] = row['new_url']
    except FileNotFoundError:
        print(f"Error: New URLs file not found at {new_urls_file}")
        return
    except Exception as e:
        print(f"Error reading {new_urls_file}: {e}")
        return

    # Generate redirect map and write to CSV
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['old_url', 'new_url', 'redirect_type'])

            for old_url, new_url in old_urls.items():
                if new_url:
                    # If a new URL is found, create a 301 redirect
                    writer.writerow([old_url, new_url, '301'])
                else:
                    # If no new URL mapping, consider it a broken link or a page to be removed
                    # For this example, we'll mark it as 'no_redirect' or you could log it
                    writer.writerow([old_url, '', 'no_redirect'])
        print(f"Redirect map generated successfully to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    # Create dummy CSV files for demonstration
    with open('old_urls.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['old_url'])
        writer.writerow(['/old-page-1'])
        writer.writerow(['/old-category/item-a'])
        writer.writerow(['/about-us'])
        writer.writerow(['/old-blog/post-xyz'])

    with open('new_urls.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['new_url'])
        writer.writerow(['/new-page-one'])
        writer.writerow(['/products/item-a'])
        writer.writerow(['/about'])
        # Note: '/old-blog/post-xyz' will not have a mapping in this example

    # Generate the redirect map
    generate_redirect_map('old_urls.csv', 'new_urls.csv', 'redirect_map.csv')

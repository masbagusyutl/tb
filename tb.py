import time
import requests
import re

# Function to read account data from data.txt
def read_account_data(file_path='data.txt'):
    with open(file_path, 'r') as file:
        data = file.read().strip().split('\n')
    return data

# Function to extract username from auth_data
def extract_username(auth_data):
    match = re.search(r'username%22:%22(.*?)%22', auth_data)
    return match.group(1) if match else 'unknown'

# Function to perform the spin task
def spin_lottery(auth_data, spins):
    url = f"https://api.tonboost.app/wheels/spin?auth_data={auth_data}"
    headers = {
        'Accept': 'application/json; indent=2',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Origin': 'https://app.tonboost.app',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Referer': 'https://app.tonboost.app/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    for _ in range(spins):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Spin successful for {extract_username(auth_data)}")
        else:
            print(f"Spin failed for {extract_username(auth_data)}")
        time.sleep(1)  # 1 second delay between spins

# Main function to execute the spin task
def main():
    account_data = read_account_data()
    total_accounts = len(account_data)

    print(f"Total accounts: {total_accounts}")

    user_choice = input("Single account or all accounts? (single/all): ").strip().lower()
    spins = int(input("Enter the number of spins: "))

    if user_choice == 'single':
        print("Available accounts:")
        for idx, auth_data in enumerate(account_data):
            username = extract_username(auth_data)
            print(f"{idx + 1}. {username}")

        selected_account_idx = int(input("Select the account number you want to run: ")) - 1
        if 0 <= selected_account_idx < total_accounts:
            selected_auth_data = account_data[selected_account_idx]
            print(f"Processing account {extract_username(selected_auth_data)}...")
            spin_lottery(selected_auth_data, spins)
        else:
            print("Invalid account selection!")
    elif user_choice == 'all':
        for idx, auth_data in enumerate(account_data):
            username = extract_username(auth_data)
            print(f"Processing account {idx + 1}/{total_accounts}: {username}...")
            spin_lottery(auth_data, spins)
            print(f"Waiting for 5 seconds before switching to the next account...")
            time.sleep(5)
    else:
        print("Invalid choice! Please enter 'single' or 'all'.")

    print("All accounts processed. Task completed.")

if __name__ == "__main__":
    main()

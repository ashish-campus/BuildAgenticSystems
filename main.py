import sys
from src.request_handler import create_request, get_all_requests
from src.analytics import run_analytics

def display_menu():
    print("\n--- SDLC Phase-Aware Agent ---")
    print("1. Add feature request")
    print("2. View all requests")
    print("3. Run analytics") # NEW OPTION
    print("4. Exit")
    return input("Select an option (1-4): ")

def handle_add_request():
    print("\n-- New Feature Request --")
    project = input("Project Name: ")
    client = input("Client Name: ")
    description = input("Feature Description (10-500 chars): ")
    
    if create_request(description, client, project):
        print("✅ Request successfully stored!")
    else:
        print("❌ Failed to store request.")

def handle_view_requests():
    requests = get_all_requests()
    if not requests:
        print("\nNo requests found.")
        return
        
    print(f"\n-- Stored Requests ({len(requests)}) --")
    for req in requests:
        print(f"\nID: {req['id']} | Date: {req['timestamp'][:10]}")
        print(f"Project: {req['project']} | Client: {req['client']}")
        print(f"Description: {req['description']}")
        print("-" * 30)

def handle_run_analytics():
    print("\nRunning analytics...")
    report = run_analytics()
    print(report)

def main():
    while True:
        choice = display_menu()
        if choice == '1':
            handle_add_request()
        elif choice == '2':
            handle_view_requests()
        elif choice == '3':
            handle_run_analytics() # CALL NEW FUNCTION
        elif choice == '4':
            print("Exiting system. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
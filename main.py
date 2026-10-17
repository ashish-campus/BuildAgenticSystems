from src.request_handler import create_request, get_all_requests
from src.dashboard import generate_dashboard

def main():
    print("Welcome to the SDLC Phase-Aware Agent")
    while True:
        print("\nOptions:")
        print("1. Submit a Feature Request")
        print("2. View All Requests (Raw)")
        print("3. View Analytics Dashboard")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            client = input("Client Name: ")
            project = input("Project Name: ")
            desc = input("Feature Description (10-500 chars): ")
            
            if create_request(desc, client, project):
                print("✅ Request successfully stored!")
            else:
                print("❌ Failed to process request.")
                
        elif choice == '2':
            requests = get_all_requests()
            print(f"\n--- Total Requests: {len(requests)} ---")
            for req in requests:
                print(f"[{req['phase'].upper()}] {req['description'][:50]}... (Confidence: {req['confidence']}%)")
                
        elif choice == '3':
            generate_dashboard()
            
        elif choice == '4':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
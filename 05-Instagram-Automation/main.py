import sys
import getpass
from instabot import Bot

def get_credentials():
    print("=== Instagram Automation Login ===")
    username = input("Enter Instagram Username: ").strip()
    password = getpass.getpass("Enter Instagram Password: ")
    return username, password

def main():
    username, password = get_credentials()
    
    print("\nInitializing bot...")
    bot = Bot()
    
    try:
        bot.login(username=username, password=password)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)
        
    while True:
        print("\n=== Choose a task to perform ===")
        print("1. Follow a user")
        print("2. Unfollow a user")
        print("3. Send a direct message (DM)")
        print("4. Upload a photo")
        print("5. Like posts of a user")
        print("6. Logout & Exit")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            target = input("Enter target username to follow: ").strip()
            if target:
                print(f"Following {target}...")
                bot.follow(target)
            else:
                print("Username cannot be empty.")
                
        elif choice == "2":
            target = input("Enter target username to unfollow: ").strip()
            if target:
                print(f"Unfollowing {target}...")
                bot.unfollow(target)
            else:
                print("Username cannot be empty.")
                
        elif choice == "3":
            target = input("Enter target username to message: ").strip()
            message = input("Enter your message: ").strip()
            if target and message:
                print(f"Sending message to {target}...")
                bot.send_message(message, [target])
            else:
                print("Target username and message cannot be empty.")
                
        elif choice == "4":
            photo_path = input("Enter absolute path to the photo (JPG format): ").strip()
            caption = input("Enter caption: ").strip()
            if photo_path:
                print(f"Uploading photo from {photo_path}...")
                bot.upload_photo(photo_path, caption=caption)
            else:
                print("Photo path cannot be empty.")
                
        elif choice == "5":
            target = input("Enter target username to like posts: ").strip()
            if target:
                print(f"Liking posts of {target}...")
                bot.like_user(target)
            else:
                print("Username cannot be empty.")
                
        elif choice == "6":
            print("Logging out...")
            bot.logout()
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()

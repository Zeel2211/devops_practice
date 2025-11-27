import time

def main():
    print("======================================")
    print("   Hello from Python inside Docker!   ")
    print("   This app was built by Jenkins :)   ")
    print("======================================")
    
    # Simulate small runtime
    for i in range(5):
        print(f"Running step {i+1}/5...")
        time.sleep(1)

    print("Done! Pipeline is working successfully.")
    print("Testing the build")

if __name__ == "__main__":
    main()

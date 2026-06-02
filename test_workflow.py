import requests

def test_home():
    try:
        response = requests.get('http://127.0.0.1:8000/')
        print(f"Test Home: {'SUCCESS' if response.status_code == 200 else 'FAILED'}")
    except:
        print("Test Home: FAILED (Server not running)")

def test_catalog():
    try:
        response = requests.get('http://127.0.0.1:8000/store/')
        print(f"Test Catalogo: {'SUCCESS' if response.status_code == 200 else 'FAILED'}")
    except:
        print("Test Catalogo: FAILED")

if __name__ == "__main__":
    print("--- Avvio Workflow di Test ---")
    test_home()
    test_catalog()
    print("-------------------------------")

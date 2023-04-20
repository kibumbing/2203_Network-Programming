import requests

if __name__ == '__main__':
    key = input("Input key: ")
    r = requests.post('http://127.0.0.1:8000/', data=key)
    print(f"The definition of {key}:\n{r.text}")
    assert r.status_code == 200
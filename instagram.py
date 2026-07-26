import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-IG-App-ID": "936619743392459"
}


def hesap_durumu(username):
    username = username.replace("@", "").strip()

    try:
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        print("STATUS:", r.status_code)

        if r.status_code == 404:
            return "kapali"

        if r.status_code != 200:
            return "hata"

        data = r.json()

        if data.get("data") and data["data"].get("user"):
            return "aktif"

        return "kapali"

    except Exception as e:
        print(e)
        return "hata"

import requests

def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def lookup_barcode(barcode: str):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Jedzomko/0.1 contact@piotrpiechowski.pl"
            }
        )
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        print("Open Food Facts zwrócił nie-JSON:")
        print(response.status_code)
        print(response.text[:300])
        return None

    if data.get("status") != 1:
        return None

    product = data.get("product", {})
    nutriments = product.get("nutriments", {})

    return {
    "name": product.get("product_name") or product.get("generic_name") or "Nieznany produkt",
    "brand": product.get("brands"),
    "kcal_100g": number(nutriments.get("energy-kcal_100g")),
    "protein_100g": number(nutriments.get("proteins_100g")),
    "fat_100g": number(nutriments.get("fat_100g")),
    "carbs_100g": number(nutriments.get("carbohydrates_100g")),
}
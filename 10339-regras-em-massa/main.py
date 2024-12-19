import pandas as pd
import requests

# spit dos zip_code
def process_zip_codes(zip_codes):
    result = []
    if isinstance(zip_codes, str) and zip_codes.strip():
        ranges = zip_codes.split(";")
        for range_pair in ranges:
            start, end = map(int, range_pair.split("-"))
            result.append({
                "id": None,
                "zip_code_start": start,
                "zip_code_end": end
            })
    return result

#split dos origin_zip
def process_origin_zip_codes(origin_zip_codes):
    result = []
    if isinstance(origin_zip_codes, str) and origin_zip_codes.strip():
        ranges = origin_zip_codes.split(";")
        for range_pair in ranges:
            start, end = map(int, range_pair.split("-"))
            result.append({
                "id": None,
                "zip_code_start": start,
                "zip_code_end": end
            })
    return result

def create_rules_from_excel(file_path, api_url, bearer_token):
    # load planilhinha
    df = pd.read_excel(file_path)

    # le cada linha para montar a req
    for _, row in df.iterrows():
        body = {
            "id": None,
            "name": row['name'],
            "client_id": None,
            "user_id": None,
            "states": [],
            "zip_codes": process_zip_codes(row.get('zip_codes', '')),
            "origin_zip_codes": process_origin_zip_codes(row.get('origin_zip_codes', '')),
            "order_value_from": None,
            "order_value_to": None,
            "provider_value_from": None,
            "provider_value_to": None,
            "logistic_provider_id": None,
            "delivery_method_ids": [],
            "valid_from": None,
            "valid_to": None,
            "platform": None,
            "platforms": [],
            "client_type": None,
            "sales_channels": [],
            "product_category": [],
            "order_weight_from": float(row['order_weight'].split("-")[0]),
            "order_weight_to": float(row['order_weight'].split("-")[1]),
            "week_days": [],
            "sku_group_ids": [],
            "order_cubic_weight_from": None,
            "order_cubic_weight_to": None,
            "cubic_volume_from": None,
            "cubic_volume_to": None,
            "quote_area_type": [],
            "delivery_method_comparisons": [],
            "warehouse_ids": [],
            "quote_tags": [],
            "action": "CHANGE_PRICE_TO",
            "price": float(row['price']),
            "enabled": False,
            "sort_order": 1456,
        }

        # monta req
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, json=body, headers=headers)
        
        if response.status_code == 201:
            print(f"Regra criada com sucesso: {row['name']}")
        else:
            print(f"Erro ao criar regra: {row['name']} - {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Solicitar informações ao usuário
    api_url = "https://api.intelipost.com.br/api/v1/quote_rule_old"
    bearer_token = input("Digite o Bearer Token: ")
    file_path = input("Digite o caminho do arquivo Excel: ")

    create_rules_from_excel(file_path, api_url, bearer_token)

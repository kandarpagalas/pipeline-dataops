import pandas as pd


def transform(orders):
    full_dataset = []
    for order in orders:
        customer = order.get("customer", "")
        charges = order.get("charges", "")
        items = order.get("items", "")
        shipping = order.get("shipping", "")

        charge = charges[0]
        # Transformar cada item em uma linha
        for item in items:

            data = {
                # "obj_key": key,
                "order_id": order["id"],
                "customer_id": customer["id"],
                "charge_id": charge["id"],
                "item_id": item["reference_id"],
                "item_price": item["unit_price"],
                "item_qtd": item["quantity"],
                "shipping_region_code": shipping["region_code"],
                "charge_paid": round(charge["amount"]["summary"]["paid"], 2),
                "charge_payment_method": charge["payment_method"]["type"],
            }

            full_dataset.append(data)

    return pd.DataFrame(full_dataset)

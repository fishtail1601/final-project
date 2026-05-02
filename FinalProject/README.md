### Installing necessary packages:  
* `pip install fastapi`
* `pip install "uvicorn[standard]"`  
* `pip install sqlalchemy`  
* `pip install pymysql`
* `pip install pytest`
* `pip install pytest-mock`
* `pip install httpx`
* `pip install cryptography`
### Run the server:
`uvicorn api.main:app --reload`
### Test API by built-in docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Endpoints
# Documents for how to run each endpoint and how they work

## Orders

## Order Details

## Customers

## Promotions
Promotions run mostly independent from everything else, it doesn't need a matching order id or anything like that so those fields are optional but still there in case promotion is tied to something specific.

GET:
In this case the promotion, here is one of the promotions already in the database. Gets all promotion entries
[
  {
    "order_id": null,
    "menu_item_id": null, 
    "promotion_code": "SUMMER10",
    "discount_percentage": "10.50",
    "discount_amount": null,
    "expiration_date": "2026-12-31",
    "id": 2
  }
]

POST
{
  "order_id": null,
  "menu_item_id": null,
  "promotion_code": "SUMMER10",
  "discount_percentage": 10.50,
  "discount_amount": null,
  "expiration_date": "2026-12-31"
}

Sample GET
This just gets one promo code depending on what the code is. Gets one promotion entry
Promotion Code: SUMMER10

Sample PUT
This gets the entry with the designated promo code and updates it
promo_code: SUMMER10
{
  "order_id": null,
  "menu_item_id": null,
  "promotion_code": "SPRING26",
  "discount_percentage": 20.50,
  "discount_amount": null,
  "expiration_date": "2026-05-02"
}

Sample DELETE
This deletes an entry depending on what the designated promo code is
promo_code: SPRING26

## Analytics

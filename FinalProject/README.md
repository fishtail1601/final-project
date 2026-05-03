# Sandwich Maker API

This project is a FastAPI backend for a sandwich/food ordering system. It supports customers, menu items, orders, order details, promotions, and analytics data for orders, customers, and reviews.

The easiest way to use the API is through FastAPI's built-in Swagger page:

```text
http://127.0.0.1:8000/docs
```

## Setup

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Or install them one at a time:

```powershell
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install pymysql
pip install pytest
pip install pytest-mock
pip install httpx
pip install cryptography
```

## Database

The database connection is configured in `api/dependencies/config.py`.

Current defaults:

```python
db_host = "localhost"
db_name = "sandwich_maker_api"
db_port = 3306
db_user = "root"
```

Make sure MySQL is running and that the database exists:

```sql
CREATE DATABASE sandwich_maker_api;
```

The app calls SQLAlchemy `create_all()` at startup. This creates missing tables, but it does not update existing tables when model fields change. If you see an error like `Unknown column ...`, check your table:

```sql
DESCRIBE customers;
DESCRIBE orders;
DESCRIBE menu_items;
```

Then add only the columns that are missing. For example:

```sql
ALTER TABLE customers
ADD COLUMN customer_phone_number VARCHAR(100);
```

## Run The Server

From the `FinalProject` folder:

```powershell
uvicorn api.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

If the server is configured to use port `8000`, the base URL is:

```text
http://127.0.0.1:8000
```

## Common Request Rules

JSON field names must match the schema exactly. For example, use `customer_phone_number`, not `phone_number`.

Dates use this format:

```json
"2026-05-03"
```

Date-times are returned by the API automatically. You usually do not need to send them when creating records.

Decimal and price fields can be sent as normal numbers:

```json
8.99
```

For optional fields, you can either omit them or send `null`.

## Customers

### Create Customer

```http
POST /customers/
```

Request body:

```json
{
  "customer_name": "Jane Doe",
  "customer_email": "jane@example.com",
  "customer_phone_number": "555-123-4567",
  "customer_address": "123 Main St",
  "password": "password123"
}
```

Notes:

- `customer_email` must be unique.
- The model stores the password in `hashed_password`. The current code maps `password` into that field.
- If you get an `Unknown column` error, your MySQL table does not match the SQLAlchemy model.

## Menu Items

Menu items are the foods available on the menu.

### Create Menu Item

```http
POST /menu/
```

Request body:

```json
{
  "dish_name": "Turkey Sandwich",
  "dish_ingredients": "Turkey, lettuce, tomato, mayo",
  "dish_price": 8.99,
  "dish_calories": 520,
  "dish_category": "Sandwich"
}
```

### Read All Menu Items

```http
GET /menu/
```

### Read One Menu Item

```http
GET /menu/{item_id}
```

Example:

```http
GET /menu/1
```

### Update Menu Item

```http
PUT /menu/{item_id}
```

You can send only the fields you want to change:

```json
{
  "dish_price": 9.49,
  "dish_calories": 540
}
```

### Delete Menu Item

```http
DELETE /menu/{item_id}
```

## Orders

Orders can be created for an existing customer or as a guest order.

### Create Order With Existing Customer

```http
POST /orders/with-account
```

Request body:

```json
{
  "customer_id": 1,
  "description": "Lunch order",
  "order_status": "Pending",
  "order_price": 15.98,
  "tracking_number": "ABC123",
  "order_details": [
    {
      "sandwich_id": 1,
      "amount": 2
    }
  ],
  "promo_code": null
}
```

Important:

- `customer_id` must already exist in the `customers` table.
- `sandwich_id` must already exist in the `sandwiches` table.
- `order_details` inside a new order should include `sandwich_id` and `amount`. Do not include `order_id`; the API creates the order first.

### Create Guest Order

```http
POST /orders/guest
```

Request body:

```json
{
  "customer_name": "Guest Customer",
  "customer_email": "guest@example.com",
  "customer_phone_number": "555-222-3333",
  "customer_address": "456 Side St",
  "description": "Guest lunch order",
  "order_status": "Pending",
  "order_price": 12.5,
  "tracking_number": "GUEST123",
  "order_details": [
    {
      "sandwich_id": 1,
      "amount": 1
    }
  ],
  "promo_code": null
}
```

### Read All Orders

```http
GET /orders/
```

### Read One Order

```http
GET /orders/{item_id}
```

### Update Order

```http
PUT /orders/{item_id}
```

Example body:

```json
{
  "order_status": "In Progress",
  "tracking_number": "ABC123"
}
```

### Mark Order Complete

```http
PATCH /orders/{item_id}/complete
```

This sets `order_status` to `Completed` and records `actual_completion_time`.

### Delete Order

```http
DELETE /orders/{item_id}
```

## Order Details

Order details represent individual sandwich line items for an order.

### Create Order Detail

```http
POST /orderdetails/
```

Request body:

```json
{
  "order_id": 1,
  "sandwich_id": 1,
  "amount": 2
}
```

Use this endpoint when the order already exists. When creating a new order with `/orders/with-account` or `/orders/guest`, put line items in the `order_details` list instead.

### Read All Order Details

```http
GET /orderdetails/
```

Use this endpoint to read all details of every order

### Read One Order Detail

```http
GET /orderdetails/{item_id}
```

Use this endpoint to read all the details of just one order using the item_id

### Update Order Detail

```http
PUT /orderdetails/{item_id}
```

Use this endpoint to update any details of an order using the item_id

Example:

```json
{
  "order_id": 1,
  "sandwich_id": 2,
  "amount": 3
}
```

### Delete Order Detail

```http
DELETE /orderdetails/{item_id}
```

Use this endpoint to delete any order detail

## Promotions

Promotions can apply a percentage discount or a fixed discount amount. Use only one discount type at a time.

### Create Promotion

```http
POST /promotions/
```

Percentage discount example:

```json
{
  "order_id": null,
  "menu_item_id": null,
  "promotion_code": "SAVE10",
  "discount_percentage": 10.0,
  "discount_amount": null,
  "expiration_date": "2026-12-31"
}
```

Fixed discount example:

```json
{
  "order_id": null,
  "menu_item_id": null,
  "promotion_code": "SAVE5",
  "discount_percentage": null,
  "discount_amount": 5.0,
  "expiration_date": "2026-12-31"
}
```

Bad request example:

```json
{
  "promotion_code": "BADPROMO",
  "discount_percentage": 10.0,
  "discount_amount": 5.0,
  "expiration_date": "2026-12-31"
}
```

This fails because both discount fields are set.

### Read Promotions

```http
GET /promotions/
GET /promotions/{promo_code}
```

Use this to just read either all promotions in your database or just one depending on the promo_code

### Update Promotion

```http
PUT /promotions/{promo_code}
```

Use this if you want to update an existing promo code

Example:

```json
{
  "discount_percentage": 15.0,
  "discount_amount": null,
  "expiration_date": "2026-12-31"
}
```

### Delete Promotion

```http
DELETE /promotions/{promo_code}
```

Use this if you want to delete a promo code

## Analytics

Analytics endpoints return reporting data for revenue, orders, customers, menu popularity, and reviews. 

### Daily Revenue

```http
GET /analytics/revenue/daily?target_date=2026-05-03
```

### Orders In Date Range

```http
GET /analytics/orders/range?start_date=2026-05-01&end_date=2026-05-03
```

### All Order Analytics Data

```http
GET /analytics/orders
```

### Customer Analytics

```http
GET /analytics/customers
```

Returns customers with their related orders and reviews.

### Sandwich Popularity

```http
GET /analytics/sandwiches/popularity
```

### All Reviews

```http
GET /analytics/reviews
```

### Negative Reviews

```http
GET /analytics/reviews/negative?threshold=3.0
```

### Combined Analytics Data

```http
GET /analytics/data
```

Returns:

```json
{
  "orders": [],
  "customers": [],
  "reviews": []
}
```

## Troubleshooting Bad Requests

### 422 Unprocessable Entity

This means the JSON body or query parameters do not match the schema.

Common causes:

- Missing required field.
- Wrong field name, such as `phone_number` instead of `customer_phone_number`.
- Wrong type, such as `"dish_price": "cheap"` instead of `"dish_price": 8.99`.
- Invalid date format. Use `YYYY-MM-DD`.

### 400 Bad Request From The Database

This usually means MySQL rejected the operation.

Common causes:

- A foreign key ID does not exist.
- A unique field already exists, such as duplicate `promotion_code` or duplicate customer email.
- The table schema is out of date.

### Unknown Column Error

Example:

```text
Unknown column 'customers.customer_phone_number'
```

Your SQLAlchemy model expects a column that your actual MySQL table does not have. Run:

```sql
DESCRIBE customers;
```

Then add the missing column, or rename the existing column to match the model.

### Duplicate Column Error

Example:

```text
Duplicate column name 'customer_address'
```

That means the column already exists. Run `DESCRIBE table_name;` and only add columns that are missing.

## Testing

Run tests from the project folder:

```powershell
python -m pytest api/tests
```

If that says `No module named pytest`, install test dependencies:

```powershell
pip install pytest pytest-mock httpx
```
=======
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

## Endpoints
#### Documents for how to run each endpoint and how they work

### Orders

### Order Details

### Customers

### Promotions
Promotions run mostly independent from everything else, it doesn't need a matching order id or anything like that so those fields are optional but still there in case promotion is tied to something specific.

GET:
In this case the promotion, here is one of the promotions already in the database. Gets all promotion entries
[{"order_id": null,"menu_item_id": null, "promotion_code": "SUMMER10","discount_percentage": "10.50","discount_amount": null,"expiration_date": "2026-12-31", "id": 2}]

POST
{
  "order_id": null,
  "menu_item_id": null,
  "promotion_code": "SUMMER10",
  "discount_percentage": 10.50,
  "discount_amount": null,
  "expiration_date": "2026-12-31"
}

GET
This just gets one promo code depending on what the code is. Gets one promotion entry
promo_code Code: SUMMER10

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
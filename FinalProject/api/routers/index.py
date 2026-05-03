from . import orders, order_details, customers, promotions, analytics, menu_items


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(promotions.router)
    app.include_router(analytics.router)
    app.include_router(menu_items.router)

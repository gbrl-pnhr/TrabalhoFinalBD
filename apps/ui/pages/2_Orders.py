from apps.ui.core.ioc import DIContainer
from apps.ui.views.orders_view import OrdersView


def main():
    vm = DIContainer.get_orders_viewmodel()
    view = OrdersView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
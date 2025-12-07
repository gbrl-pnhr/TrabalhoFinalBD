from apps.ui.core.ioc import DIContainer
from apps.ui.views.customers_view import CustomersView


def main():
    vm = DIContainer.get_customers_viewmodel()
    view = CustomersView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
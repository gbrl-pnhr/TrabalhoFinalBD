from apps.ui.core.ioc import DIContainer
from apps.ui.views.tables_view import TablesView


def main():
    vm = DIContainer.get_table_viewmodel()
    view = TablesView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
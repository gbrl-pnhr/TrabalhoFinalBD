from apps.ui.core.ioc import DIContainer
from apps.ui.views.menu_view import MenuView


def main():
    vm = DIContainer.get_menu_viewmodel()
    view = MenuView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
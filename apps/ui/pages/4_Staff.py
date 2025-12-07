from apps.ui.core.ioc import DIContainer
from apps.ui.views.staff_view import StaffView


def main():
    vm = DIContainer.get_staff_viewmodel()
    view = StaffView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
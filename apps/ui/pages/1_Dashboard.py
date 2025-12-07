from apps.ui.core.ioc import DIContainer
from apps.ui.views.dashboard_view import DashboardView


def main():
    vm = DIContainer.get_dashboard_viewmodel()
    view = DashboardView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
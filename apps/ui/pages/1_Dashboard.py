import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from apps.ui.core.ioc import DIContainer
from apps.ui.views.dashboard_view import DashboardView


def main():
    vm = DIContainer.get_dashboard_viewmodel()
    view = DashboardView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
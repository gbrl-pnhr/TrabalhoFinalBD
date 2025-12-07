from apps.ui.core.ioc import DIContainer
from apps.ui.views.kitchen_view import KitchenView

def main():
    vm = DIContainer.get_kitchen_viewmodel()
    view = KitchenView(view_model=vm)
    view.render()

if __name__ == "__main__":
    main()
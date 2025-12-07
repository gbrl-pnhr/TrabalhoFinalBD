from apps.ui.core.ioc import DIContainer
from apps.ui.views.reviews_view import ReviewsView


def main():
    vm = DIContainer.get_reviews_viewmodel()
    view = ReviewsView(view_model=vm)
    view.render()


if __name__ == "__main__":
    main()
class DataMixin:
    title_page = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.title_page:
            context['title_page'] = self.title_page

        return context

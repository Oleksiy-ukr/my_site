from .models import *
from django.core.cache import cache

menu = [{'title':'Про сайт', 'url_name': 'about'},
        {'title':'Додати статтю', 'url_name': 'addpage'},
        {'title':'Зворотній зв\'язок', 'url_name': 'contact'},
        # {'title':'Увійти', 'url_name': 'login'}
]


class DataMixin:
    paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.all()
            cache.set('cats', cats, 60)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

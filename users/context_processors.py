from events.models import Category
from wallet.models import Balance


def site_info(request):

    categorys = Category.objects.all().values()

    balance = None

    if request.user.is_authenticated:
        balance_obj = Balance.objects.filter(user=request.user).first()
        if balance_obj:
            balance = balance_obj.balance

    return {
        "category": categorys,
        "balance": balance
    }
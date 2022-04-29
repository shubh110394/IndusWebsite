from django import template
from store.models.customer import Customer

register = template.Library()

@register.filter(name="multiply")
def multiply(number,number1):
    return number * number1




# @register.filter(name="user")
# def user(customer):
#     # keys = cart.keys()
#     # for id in keys:
#     #     # print(id,product.id)
#     #     if int(id) == product.id:
#     #         return True
#     # return False
#     # Customer.user_name(customer)
#     ans = Customer.objects.get(id)
#     print(ans)
#     if Customer.objects.get(id) == customer:
#         return Customer.objects.get("first_name")
#     else:
#         return "New User"
    
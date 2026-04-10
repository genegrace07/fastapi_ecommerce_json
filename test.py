import json

orders = 'order.json'

try:
    with open(orders,'r') as f:
        view_total = json.load(f)
    view_list = [v['total'] for v in view_total[0]['items']]
    print(view_list)
    print(sum(view_list))
except:
    print('empty order')

# orders = 'order.json'
#
# with open(orders,'r') as f:
#     view_total = json.load(f)
#
# grand_total = [v for v in view_total[0]['grand_total']]
#
# print(grand_total)


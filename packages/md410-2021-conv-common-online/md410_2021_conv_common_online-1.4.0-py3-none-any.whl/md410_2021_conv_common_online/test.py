from db import DB, Registree

from datetime import datetime

dbh = DB(debug=False)

if 1:
    n = 0
    dbh._clear()
    for details in (
        [
            "Kim",
            "van Wyk",
            "0833844260",
            "vanwykk@gmail.com",
            "North Durban",
            "District E",
            False,
            True,
            True,
            False,
        ],
        [
            "Cliff",
            "Hocking",
            "0833844260",
            "vanwykk@gmail.com",
            "Midrand",
            "District W",
            1,
            0,
            0,
            1,
        ],
    ):
        n += 1
        details.insert(0, n)
        details.append(datetime.now())
        dbh.save_registree(Registree(*details))

registrees = dbh.get_registrees()
for registree in registrees:
    print(registree)

registree = dbh.get_registree(1)
print(registree)
print(registree.name)

dbh._clear()

# registree_set = dbh.get_registrees(14)
# print(registree_set.events)
# print(registree_set.events.cost, registree_set.events.get_costs_per_item())
# print(registree_set.payments)
# print(registree_set.cost)
# print(registree_set.extras)
# print(registree_set.extras.cost, registree_set.extras.get_costs_per_item())
# for reg in registree_set.registrees:
#     print(reg)
# print(registree_set.registree_names)
# print(registree_set.registree_first_names)
# print(registree_set.file_name)
# print(registree_set.paid, registree_set.paid_in_full, registree_set.still_owed)
# print(registree_set.deposit)

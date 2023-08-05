from db import DB
import pyperclip

dbh = DB(debug=False)

(pairs, registrees) = dbh.get_2020_payee_emails()

with open("email_msg.txt", "r") as fh:
    MSG = fh.read()

people = []
pairs_seen = []
seen = []
for (k, r) in registrees.items():
    for pair in pairs:
        if (k in pair) and (pair not in pairs_seen):
            pairs_seen.append(pair)
            seen.extend(pair)
            r1 = registrees[pair[0]]
            r2 = registrees[pair[1]]
            people.append(
                (
                    f"{r1.name.strip()} and {r2.name.strip()}",
                    r1.total + r2.total,
                    "; ".join(list(set([r1.email, r2.email]))),
                )
            )
            continue
    else:
        if k not in seen:
            seen.append(k)
            people.append((r.name, r.total, r.email))

for (name, total, emails) in people:
    pyperclip.copy(emails)
    print(f"To: addresses copied to clipboard: {emails}")
    input()
    pyperclip.copy("liontrevorhobbs@gmail.com")
    print(f"CC: addresses copied to clipboard: {emails}")
    input()
    pyperclip.copy("Bank details for 2020/2021 MD410 Convention refund")
    print(f"Subject copied to email")
    input()
    pyperclip.copy(MSG % {"name": name, "total": f"{total:0.2f}"})
    print("Body copied to email")
    input()

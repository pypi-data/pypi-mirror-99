from db import DB, Registree

dbh = DB(debug=False)

proceed = input("Enter 'yes' to clear DB:  ")
if proceed.strip() == "yes":
    dbh._clear()
    print("DB cleared")

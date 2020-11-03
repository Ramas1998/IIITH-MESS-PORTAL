from app import app

#app level data
#e.g. no of cancellations

app.no_of_cancellations_allowed=5
app.static_salt="#ANTS@!%"

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.run(debug = True)
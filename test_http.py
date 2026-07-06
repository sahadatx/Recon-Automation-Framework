from modules.http.helpers import (
    create_session,
)

session = create_session()

print(session.headers)

print(session.verify)

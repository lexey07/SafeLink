from app.database.database import engine, Base
from app.models.user import User
from app.models.url_check import UrlCheck

Base.metadata.create_all(bind=engine)

print("Таблицы успешно созданы!")
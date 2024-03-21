import random
import peewee

from database_manager import DatabaseManager

import local_settings

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)


class City(peewee.Model):
    title = peewee.CharField(max_length=255, null=False, verbose_name='Title')

    class Meta:
        database = database_manager.db


class Phone(peewee.Model):
    first_name = peewee.CharField(
        max_length=255, null=False, verbose_name='FirstName')
    last_name = peewee.CharField(
        max_length=255, null=False, verbose_name='LastName')
    mobile = peewee.CharField(
        max_length=11, null=False, verbose_name='Mobile')
    city = peewee.ForeignKeyField(model=City, null=False, verbose_name='City')

    class Meta:
        database = database_manager.db


if __name__ == "__main__":
    try:
        database_manager.create_tables(models=[City, Phone])

        cities = ['Tehran', 'Mashhad', 'Shiraz', 'Tabriz', 'Ahvaz']

        for i in range(5):
            City.create(title=cities[i])

        for _ in range(20):
            rand_int = random.randint(1, 99)
            rand_int_mobile = random.randint(10000000, 99999999)
            Phone.create(first_name=f'first_name_{rand_int}', last_name=f'last_name_{rand_int}', mobile=f'091{rand_int_mobile}',
                         city=random.randint(1, 5))

        # print last_name where city=Shiraz
        phones = Phone.select().where(Phone.city == 3)
        for phone in phones:
            print(phone.last_name)

    except Exception as error:
        print("Error", error)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")

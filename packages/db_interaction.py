from datetime import timedelta, datetime, date
import psycopg2
import environs


users = {"id_user: int": "DBInteraction_instance"}
Env = environs.Env()
Env.read_env()


class DBInteraction:
    conn = psycopg2.connect(
                    database=Env("Database"),
                    host=Env("Host"),
                    user=Env("User"),
                    password=Env("Password"),
                    port=int(Env("Port")))
    flag = None

    def __init__(self, id_user: int, phone_number: int, name: str) -> None:
        self.id_user = id_user
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT id FROM users WHERE id={id_user}")
            flag = cur.fetchone()
            if not flag:
                cur.execute(f"INSERT INTO users VALUES ({id_user}, {phone_number}, '{name}')")
        except psycopg2.Error as ex:
            self.conn.rollback()
            print(ex)
            print("EXCEPTION WHILE INSERTING NEW USER")

    @classmethod
    def select_free_time(cls, id_room: int, date_order: datetime) -> list[str] | psycopg2.Error:
        lst_dates = (repr((date_order + timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S')),
                 repr((date_order + timedelta(hours=16)).strftime('%Y-%m-%d %H:%M:%S')),
                 repr((date_order + timedelta(hours=20)).strftime('%Y-%m-%d %H:%M:%S')))
        try:
            cursor = cls.conn.cursor()
            cursor.execute(
                f'''SELECT * FROM reservations WHERE to_time in ({', '.join(lst_dates)})
                    AND room_id={id_room} AND user_id IS NOT NULL'''
            )
            lst_dates, dates = map(lambda x: x.replace("'", ''),
                                    lst_dates), list(
                 map(lambda x: x[3].strftime('%Y-%m-%d %H:%M:%S'), cursor.fetchall()))
            lst_dates = list(filter(lambda x: x not in dates, lst_dates))
            return lst_dates

        except psycopg2.Error as ex:
            print(ex)
            print("EXCEPTION WHILE SELECTING FREE TIME")

    @classmethod
    def fill_columns(cls):
        try:
            year = date.today().year
            date_temp: datetime = datetime(year=year, month=1, day=1)
            print(date_temp)
            cursor = cls.conn.cursor()
            cursor.execute("SELECT * FROM reservations LIMIT 1")
            value = cursor.fetchone()
            if not value:
                dates = [(j + timedelta(hours=12), j + timedelta(hours=16), j + timedelta(hours=20))
                        for j in [(date_temp + timedelta(days=i))
                                    for i in range(365)]]
                dates = [(elem[0].strftime('%Y-%m-%d %H:%M:%S'), elem[1].strftime('%Y-%m-%d %H:%M:%S'),
                            elem[2].strftime('%Y-%m-%d %H:%M:%S'))
                            for elem in dates]
                for i in range(1, 4):
                    for elem in dates:
                        for res in elem:
                            print(i, res)
                            cursor.execute(f"INSERT INTO reservations (room_id, to_time) VALUES ({i}, '{res}')")
                cls.conn.commit()
        except psycopg2.Error as ex:
            cls.conn.rollback()
            print(ex)
            print('EXCEPTION WHILE INSERTING DATES')

    def insert_reservation(self, date_res: str, index: int):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"UPDATE reservations SET user_id={self.id_user}, created_at='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE to_time='{date_res}' AND room_id={index}"
            )
            self.conn.commit()
        except psycopg2.Error as ex:
            self.conn.rollback()
            print(ex)
            print("EXCEPTION WHILE MAKING NEW RESERVATION")

    def check_reservations(self):
        try:
            cursor = self.conn.cursor()
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                F"SELECT to_time, room_id FROM reservations WHERE to_time > '{date_now}' AND user_id={self.id_user}")
            values = cursor.fetchone()
            return values
        except psycopg2.Error as ex:
            self.conn.rollback()
            print(ex)
            print('EXCEPTION WHILE SELECTING EXISTING RESERVATIONS')

    @classmethod
    def start_bot(cls):
        cursor = cls.conn.cursor()
        cursor.execute("SELECT * FROM users")
        values = cursor.fetchall()
        for id_u, number, name in values:
            users[id_u] = DBInteraction(id_u, number, name)
        DBInteraction.fill_columns()

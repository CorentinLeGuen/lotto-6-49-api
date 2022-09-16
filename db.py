import os
import sqlite3


class LottoDB:
    def __init__(self):
        self.filename = '/db.sqlite3'
        self.path_directory = os.path.dirname(os.path.abspath(__file__))
        self.con = sqlite3.connect(self.path_directory + self.filename)

    def get_all(self) -> list:
        cur = self.con.cursor()
        cur.execute("SELECT * FROM draw ORDER BY draw_date DESC")
        l = cur.fetchall()
        result = []
        for d in l:
            r = {'draw_date': d[0], 'number_1': d[1], 'number_2': d[2], 'number_3': d[3], 'number_4': d[4], 'number_5': d[5], 'number_6': d[6], 'number_c': d[7]}

            result.append(r)

        return result

    def get_by_number(self, n: int) -> list:
        cur = self.con.cursor()
        cur.execute("""SELECT * FROM draw WHERE number_1 == (?) 
                            OR number_2 == (?) 
                            OR number_3 == (?) 
                            OR number_4 == (?) 
                            OR number_5 == (?) 
                            OR number_6 == (?) 
                            OR number_c == (?) ORDER BY draw_date DESC
                        """, (n, n, n, n, n, n, n))
        l = cur.fetchall()
        result = []
        for d in l:
            r = {'draw_date': d[0], 'number_1': d[1], 'number_2': d[2], 'number_3': d[3], 'number_4': d[4], 'number_5': d[5], 'number_6': d[6], 'number_c': d[7]}

            result.append(r)

        return result

    def get_by_complementary_number(self, n: int) -> list:
        cur = self.con.cursor()
        cur.execute("""SELECT * FROM draw WHERE number_c == ? ORDER BY draw_date DESC""", (n,))
        l = cur.fetchall()
        result = []
        for d in l:
            r = {'draw_date': d[0], 'number_1': d[1], 'number_2': d[2], 'number_3': d[3], 'number_4': d[4], 'number_5': d[5], 'number_6': d[6], 'number_c': d[7]}

            result.append(r)

        return result

    def get_total_records(self) -> int:
        cur = self.con.cursor()
        cur.execute("SELECT COUNT(*) FROM draw")
        return int(cur.fetchone()[0])

    def get_stats(self):
        cur = self.con.cursor()
        cur.execute("SELECT draw_date FROM draw ORDER BY draw_date DESC LIMIT 1")
        date_last = str(cur.fetchone()[0])
        cur.execute("SELECT draw_date FROM draw ORDER BY draw_date LIMIT 1")
        date_first = str(cur.fetchone()[0])
        total = self.get_total_records()
        draws = {}
        for i in range(1, 50):
            draws[i] = len(self.get_by_number(i))

        return date_last, date_first, total, draws

    def get_by_date(self, date: str):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM draw WHERE draw_date == ?", (date,))
        d = cur.fetchone()
        if d:
            return {'draw_date': d[0], 'number_1': d[1], 'number_2': d[2], 'number_3': d[3], 'number_4': d[4], 'number_5': d[5], 'number_6': d[6], 'number_c': d[7]}
        return None

    def get_by_date_wc(self, year: str):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM draw WHERE draw_date LIKE ?", (year + '%',))
        l = cur.fetchall()
        result = []
        for d in l:
            r = {'draw_date': d[0], 'number_1': d[1], 'number_2': d[2], 'number_3': d[3], 'number_4': d[4], 'number_5': d[5], 'number_6': d[6], 'number_c': d[7]}

            result.append(r)

        return result

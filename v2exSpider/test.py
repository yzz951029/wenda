from pyquery import PyQuery
import pymysql
import random


class test:
    def __init__(self):
        self.db = pymysql.connect('localhost','root','ying1206','wenda',charset='utf8')

    def add_quesion(self,title,content):
        try:
            cur = self.db.cursor();
            sql = 'insert into  question (title,content,user_id,created_date,comment_count) values ("%s","%s",%d,now(),0)' % (title, content, random.randint(1, 20))
            print(sql)
            cur.execute(sql)
            self.db.commit()
        except Exception:
            print ("Exception Here")
            self.db.rollback()
            raise Exception



def main():
  s = "/t/477741#reply23";
  print(s.find("reply"))
  a =test()
  a.add_quesion("hello","this is a test")


if __name__ == "__main__":
    main()
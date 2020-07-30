import pymysql


class TableConnect():
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def dbConnect(self):
        connection = pymysql.connect(
            host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = connection.cursor()
        return connection, cursor

    def insertTask(self, task, description, due_date):
        try:
            connection, cursor = self.dbConnect()
            query = "insert into todolist (task, description, due_date) values (%s, %s, %s)"
            values = (task, description, due_date)
            cursor.execute(query, values)
            connection.commit()
            return True
        except pymysql.OperationalError as e:
            print(e)
        except pymysql.InternalError as e:
            print(e)
        except pymysql.ProgrammingError as e:
            print(e)
        finally:
            try:
                connection.close()
            except:
                pass

    def viewTasks(self):
        try:
            connection, cursor = self.dbConnect()
            query = "select * from todolist"
            cursor.execute(query)
            data = cursor.fetchall()
            connection.commit()
            return data
        except pymysql.OperationalError as e:
            print(e)
        except pymysql.InternalError as e:
            print(e)
        except pymysql.ProgrammingError as e:
            print(e)
        finally:
            try:
                connection.close()
            except:
                pass
    
    def selectTask(self, id):
        try:
            connection, cursor = self.dbConnect()
            query = "select * from todolist where id = %s"
            values = id
            cursor.execute(query, values)
            data = cursor.fetchall()
            connection.commit()
            return data
        except pymysql.OperationalError as e:
            print(e)
        except pymysql.InternalError as e:
            print(e)
        except pymysql.ProgrammingError as e:
            print(e)
        finally:
            try:
                connection.close()
            except:
                pass

    def deleteTask(self, id):
        try:
            connection, cursor = self.dbConnect()
            query = "delete from todolist where id = %s"
            values = (id)
            cursor.execute(query, values)
            connection.commit()
        except pymysql.OperationalError as e:
            print(e)
        except pymysql.InternalError as e:
            print(e)
        except pymysql.ProgrammingError as e:
            print(e)
        finally:
            try:
                connection.close()
            except:
                pass

    def updateTask(self, id, description, due_date):
        try:
            connection, cursor = self.dbConnect()
            query = "update todolist set description = %s, due_date = %s where id = %s"
            values = (description, due_date, id)
            cursor.execute(query, values)
            connection.commit()
            return True
        except pymysql.OperationalError as e:
            print(e)
        except pymysql.InternalError as e:
            print(e)
        except pymysql.ProgrammingError as e:
            print(e)
        finally:
            try:
                connection.close()
            except:
                pass

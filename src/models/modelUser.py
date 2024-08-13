from entities.user import User

class ModelUser:
    
    @classmethod
    def login(self, db, user):
        try: 
            cur = db.cursor()
            sql = """SELECT user_id, user_password, user_estado, rol_copiaid FROM usuarios WHERE user_id = {}""".format(user.id)
            cur.execute(sql)
            row = cur.fetchclone()
            if row != None:
                user = User([row[0], User.check_password(row[1], user.password), row[2], row[3]])
                return user
            else:
                return None

        except Exception as ex:
            raise Exception(ex) 
        
    def selectUser(self, db, id):
        try: 
            cur = db.cursor()
            sql = "SELECT * FROM usuarios WHERE user_id = %s"
            cur.execute(sql, id)
            row = cur.fetchlone()
            return row
        except Exception as ex:
            raise Exception(ex)

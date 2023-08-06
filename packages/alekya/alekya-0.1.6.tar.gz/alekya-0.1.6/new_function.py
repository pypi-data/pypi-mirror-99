def jsonsql(dfjson,tname,sqlstr):
    sqlstr=""
    for x in dfjson.columns:
        for y in dfjson.take(1):
            y=dfjson.select("`"+x+"`").take(1)[0][0]
            try:
                if isfloat(y):
                    sqlstr+="  "+x+"  INTEGER NOT NULL,"+"\n"
                else:
                    try:
                        (datetime.datetime.strptime(str(y), '%Y-%m-%d'))==True
                        sqlstr+="  "+x+"  timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),"+"\n"
                    except:
                        sqlstr+="  "+x+"  VARCHAR,"+"\n"
            except:
                #sqlstr+="  "+x+"  VARCHAR,"+"\n"
                print("Unkown")

    finalsql="CREATE TABLE " + tname + "("+sqlstr+")"
    return finalsql

import os,django
from django.conf import settings
# 加载django配置
current_dir=os.getcwd()
setting_model_str=current_dir.split("\\")[-1]+".settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_model_str)
django.setup()
# your imports, e.g. Django models
from c_mssql import DB_Config
from c_mssql.mssql_conn import Mssql_Conn

import io,json,os




def add_sql_description(table_name,description,column_name=None):
    table_str="INNER JOIN sys.columns AS c ON t.object_id = c.object_id" if bool(column_name) else ""
    join_str=" AND ep.minor_id = c.column_id " if bool(column_name) else " and ep.minor_id=0 "
    where_str=f"AND C.name= '{column_name}'" if bool(column_name) else ""
    update_str=f""",@level2type = N'Column', @level2name = '{column_name}'""" if bool(column_name) else ""

    sql_str=f"""
IF EXISTS(
SELECT top 1 1
FROM sys.tables AS t
{table_str}
inner JOIN sys.extended_properties AS ep
ON ep.major_id = t.object_id  {join_str} and ep.class =1
WHERE 1=1
AND t.name='{table_name}' 
{where_str}
AND EP.class=1
)
BEGIN
EXEC sp_updateextendedproperty   
@name = N'MS_Description',   
@value = '{description}',  
@level0type = N'Schema', @level0name = 'dbo',  
@level1type = N'Table',  @level1name = '{table_name}'  
{update_str};
END
ELSE
BEGIN
EXEC sp_addextendedproperty   
@name = N'MS_Description',   
@value = '{description}',  
@level0type = N'Schema', @level0name = 'dbo',  
@level1type = N'Table',  @level1name = '{table_name}'
{update_str};
END
 
"""
    # print(sql_str)
    server=settings.DATABASES["default"]["HOST"]
    database=settings.DATABASES["default"]["NAME"]
    username=settings.DATABASES["default"]["USER"]
    password=settings.DATABASES["default"]["PASSWORD"]
    conn=Mssql_Conn(DB_Config(server,database,username,password))
    conn.open()
    conn.execute(sql_str)
    conn.commit()
    conn.close()


def update_MS_Description(models,modelname="project.models"):
    data_list=[]
    for key in dir(models):
        model=getattr(models,key)
        try:
            if model.__module__==modelname:
                model_name=key
                model=model
                table_name=model._meta.db_table
                row_dict={"table_name":model._meta.db_table,"field_name":None,"verbose_name":model._meta.verbose_name}
                data_list.append(row_dict)
                filed_str=model.__doc__
                filed_str=filed_str[len(model_name)+1:len(filed_str)-1]
                for field in filed_str.split(","):
                    field=field.strip()
                    filed_tmp=getattr(model,field)
                    field_name=filed_tmp.field.db_column if bool(filed_tmp.field.db_column) else field
                    verbose_name=filed_tmp.field.verbose_name
                    if field_name!=verbose_name:
                        row_dict={"table_name":table_name,"field_name":field_name,"verbose_name":verbose_name}
                        if row_dict not in data_list:
                            data_list.append(row_dict)
        except:
            pass

    for row_dict in data_list:
        print("正在更新:",row_dict)
        add_sql_description(row_dict["table_name"],row_dict["verbose_name"],row_dict["field_name"])
    print("更新成功")
    

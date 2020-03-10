import logging
import re
import time
import traceback
import simplejson
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.db import connection
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
from sql.engines import get_engine
from sql.utils.resource_group import  user_instances
from dataxweb.models import DataXJob, DataXJobWriterColumn
import simplejson as json
from common.utils.extend_json_encoder import ExtendJSONEncoder
from sql.models import Users, Instance
# Create your views here.
logger = logging.getLogger('default')

def addDataxJob(request):
    """
    任务维护界面
    """
    return render(request, 'adddataxjob.html')

def dataxJob(request):
    """job管理界面"""
    return render(request, 'dataxjob.html')


def dataxJoblist(request):
    """
    任务明细界面
    """
    # 获取用户信息
    user = request.user
    print(user)
    #search = request.POST.get('search', '')
    #dataxJob = serializers.serialize("json", DataXJob.objects.all())
    sql = f"""select
	       datax_job.job_id ,
	       datax_job.job_name,
	       datax_job.job_description,
	       a.instance_name as read_instance,
	       datax_job.read_database,
	       datax_job.read_sql,
	       b.instance_name  as writer_instance,
	       datax_job.writer_database,
	       datax_job.writer_table,
	       datax_job.writer_preSql,
	       datax_job.writer_postSql,
	       datax_job.create_time,
	       datax_job.update_time,
	       datax_job.crate_user
           from
	       datax_job , sql_instance a , sql_instance b 
           where read_instance_id= a.id
           and writer_instance_id=b.id;"""
    # print(job_detail)
    # serializers.serialize("json", job_detail)
    # #job_detail = json.loads(job_detail)
    job_count = DataXJob.objects.all().count()
    cursor = connection.cursor()
    sql_result=cursor.execute(sql,None)
    col_names = [desc[0] for desc in cursor.description]
    print(col_names)
    sql_result = dictfetchall(cursor)
    result = {"total": job_count,"rows": sql_result}
    print(result)
    #result = {dataxJob}
    return HttpResponse(json.dumps(result,cls=ExtendJSONEncoder), content_type='application/json')

















def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
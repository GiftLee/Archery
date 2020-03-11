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
from sql.utils.resource_group import user_instances
from dataxweb.models import DataXJob, DataXJobWriterColumn
import simplejson as json
from common.utils.extend_json_encoder import ExtendJSONEncoder
from sql.models import Users, Instance
# Create your views here.
logger = logging.getLogger('default')


def dataxJob(request):
    """job管理界面"""
    read_instance_id = DataXJob.objects.values("read_instance_id")
    writer_instance_id = DataXJob.objects.values("writer_instance_id")
    read_instance_name = Instance.objects.filter(
        id__in=read_instance_id).values("id", "instance_name")
    writer_instance_name = Instance.objects.filter(
        id__in=writer_instance_id).values("id", "instance_name")

    return render(request, 'dataxjob.html', {'read_instance': read_instance_name, 'writer_instance': writer_instance_name})


def dataxJoblist(request):
    """
    任务明细界面
    """
    # 获取用户信息
    user = request.user
    read_instance = request.POST.getlist('read_instance[]')
    writer_instance = request.POST.getlist('writer_instance[]')
    search = request.POST.get('search', '')

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
    and writer_instance_id=b.id
    """

    if read_instance:
        read_sql = """ 
        and read_instance_id in (%s)
        """
        args = ', '.join(list(map(lambda x: "'%s'" % x, read_instance)))
        sql = sql + read_sql % args

    if writer_instance:
        writer_sql = """ 
        and writer_instance_id in (%s)
        """
        args = ', '.join(list(map(lambda x: "'%s'" % x, writer_instance)))
        sql = sql + writer_sql % args
    if search:
        search_sql = """
        and job_name like '%%%s%%'
        """
        sql = sql + search_sql % search
    sql = sql + ";"

    job_count = DataXJob.objects.all().count()
    cursor = connection.cursor()
    sql_result = cursor.execute(sql, None)
    col_names = [desc[0] for desc in cursor.description]
    sql_result = dictfetchall(cursor)
    result = {"total": job_count, "rows": sql_result}
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder), content_type='application/json')


def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def addDataxJob(request):
    """
    任务维护界面
    """
    return render(request, 'adddataxjob.html')


def saveDataxJob(request):
    job_name = request.Post.get('job_name')
    description = request.Post.get('description')
    read_instance_id = request.Post.get('read_instance_id')
    read_database = request.Post.get('read_database')
    read_sql = request.Post.get('read_sql')
    writer_instance_id = request.Post.get('writer_instance_id')
    writer_database = request.Post.get('writer_database')
    writer_table = request.Post.get('writer_table')
    writer_column = request.Post.getlist('writer_column[]')
    writer_preSql = request.Post.get('writer_preSql')
    writer_postSql = request.Post.get('writer_postSql')

    savejob = DataXJob()
    savejob.job_name = job_name
    savejob.job_description = description
    savejob.read_instance_id = read_instance_id
    savejob.read_database = read_database
    savejob.writer_instance_id=writer_instance_id
    savejob.writer_database=writer_database
    savejob.writer_table=writer_table
    savejob.writer_preSql=writer_preSql
    savejob.writer_postSql=writer_postSql
    savejob.crate_user = request.user
    try:
        savejob.save()
    except:
        savejob.close()
        savejob.save()
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

def dataxJoblist(request):
    """
    任务明细界面
    """
       # 获取用户信息
    user = request.user
    print(user)
    search = request.POST.get('search', '')
    job_detail = DataXJob.objects.all()
    serializers.serialize("json",job_detail)
    print(job_detail)
    job_detail = json.loads(job_detail)
    result = { "rows": job_detail}
    # # 查询个人记录，超管查看所有数据s
    # if user.is_superuser:
    #     job_detail = DataXJob.objects.all().filter(
    #       #  Q(sqllog__contains=search) | Q(user_display__contains=search)).count()
    #     #sql_log_list = UpdateLog.objects.all().filter(
    #      #   Q(sqllog__contains=search) | Q(user_display__contains=search)).order_by(
    #      #   '-id')
    # else:
    #     sql_log_count = UpdateLog.objects.filter(username=user.username).filter(sqllog__contains=search).count()
    #     sql_log_list = UpdateLog.objects.filter(username=user.username).filter(sqllog__contains=search).order_by('-id')
    # # QuerySet 序列化
    # sql_log_list = serializers.serialize("json", sql_log_list)
    # sql_log_list = json.loads(sql_log_list)
    # sql_log = [log_info['fields'] for log_info in sql_log_list]

    # result = {"total": sql_log_count, "rows": sql_log}
    # 返回查询结果
    return HttpResponse(json.dumps(result), content_type='application/json')
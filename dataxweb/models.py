from django.db import models
from sql.models import Instance

class DataXJob(models.Model):
    """
    数据同步任务
    """
    job_id = models.AutoField('任务ID', primary_key=True)
    job_name = models.CharField('任务名称', max_length=100, unique=True)
    job_description = models.CharField('任务描述', max_length=255,null=True,blank=True)
    read_instance_id  = models.IntegerField(verbose_name='读取实例ID')
    read_database = models.CharField('读数据库名', max_length=255,null=False,blank=True)
    read_sql = models.TextField('读取sql内容')
    writer_instance_id = models.IntegerField(verbose_name='写实例ID')
    writer_database = models.CharField('写数据库名', max_length=255,null=False,blank=True)
    writer_table = models.CharField('写入表名',max_length=255,null=False,blank=True)
    writer_preSql = models.TextField('写入数据前执行的SQL语句',null=True)
    writer_postSql = models.TextField('写入数据后执行的SQL语句',null=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    crate_user = models.CharField('创建人', max_length=100)

    def __str__(self):
        return self.job_name

    class Meta:
        managed = True
        db_table = 'datax_job'
        verbose_name = u'数据同步任务'
        verbose_name_plural = u'数据同步任务'


class DataXJobWriterColumn(models.Model):
    """
    写入表的列信息  
    """
    column_name = models.TextField('列名')
    job = models.ForeignKey(DataXJob,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    def __str__(self):
        return self.column_name

    class Meta:
        managed = True
        db_table = 'datax_job_writer_column'
        verbose_name = u'写入表列信息'
        verbose_name_plural = u'写入表列信息'



# /*
# * 数据同步任务实例
# */
# drop table if exists `datax_job_instance`;
# CREATE TABLE `datax_job_instance` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `instance_id` bigint(20) NOT NULL COMMENT '任务实例ID',
#   `name` varchar(255) DEFAULT NULL COMMENT '名称',
#   `description` varchar(255) DEFAULT NULL COMMENT '描述',
#   `querySql` longtext COLLATE utf8_bin NOT NULL COMMENT '查询SQL语句',
#   `reader_databaseinfo_host` varchar(255) NOT NULL COMMENT '读取数据库IP',
#   `reader_databaseinfo_description` varchar(255) NOT NULL COMMENT '读取数据库描述',
#   `writer_table` varchar(255) DEFAULT NULL COMMENT '写入表名',
#   `writer_databaseinfo_host` varchar(255) NOT NULL COMMENT '写入数据库IP',
#   `writer_databaseinfo_description` varchar(255) NOT NULL COMMENT '写入数据库描述',
#   `writer_preSql` longtext COLLATE utf8_bin NOT NULL COMMENT '写入数据前执行的SQL语句',
#   `writer_postSql` longtext COLLATE utf8_bin NOT NULL COMMENT '写入数据后执行的SQL语句',
#   `trigger_mode` int(2) DEFAULT '1' COMMENT '触发模式 1 自动 2 手动（默认自动）',
#   `status` int(2) DEFAULT '0' COMMENT '状态 0 正在执行 1 执行完成',
#   `result` int(2) DEFAULT '2' COMMENT '执行结果 0 成功 1 失败 2 未知',
#   `start_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
#   `end_time` datetime DEFAULT NULL COMMENT '结束时间',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `datax_job_instance_id_uniq` (`instance_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8 COMMENT='datax数据同步任务实例';


# /*
# * 批处理作业
# */
# drop table if exists `batch_job`;
# CREATE TABLE `batch_job` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(255) DEFAULT NULL COMMENT '名称',
#   `description` varchar(255) DEFAULT NULL COMMENT '描述',
#   `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `batch_job_name_uniq` (`name`)
# ) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8 COMMENT='批处理作业';


# /*
# * 批处理作业详情
# */
# drop table if exists `batch_job_details`;
# CREATE TABLE `batch_job_details` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `batch_job_id` int(11) NOT NULL COMMENT '批处理作业ID',
#   `subjob_id` int(11) NOT NULL COMMENT '子作业ID',
#   `type` int(2) NOT NUll COMMENT '类型 1 数据同步 2 SQL脚本 3 备份。 主要用于后期扩展',
#   `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8 COMMENT='批处理作业详情';


# /*
# * 批处理作业执行实例
# */
# drop table if exists `batch_job_instance`;
# CREATE TABLE `batch_job_instance` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `instance_id` bigint(20) NOT NULL COMMENT '实例ID',
#   `name` varchar(255) DEFAULT NULL COMMENT '名称',
#   `description` varchar(255) DEFAULT NULL COMMENT '描述',
#   `trigger_mode` int(2) DEFAULT '1' COMMENT '触发模式 1 自动 2 手动（默认自动）',
#   `status` int(2) DEFAULT '0' COMMENT '状态 0 正在执行 1 执行完成',
#   `result` int(2) DEFAULT '2' COMMENT '执行结果 0 成功 1 失败 2 未知',
#   `start_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
#   `end_time` datetime DEFAULT NULL COMMENT '结束时间',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `batch_job_instance_id_uniq` (`instance_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8 COMMENT='批处理作业执行实例';


# /*
# * 批处理作业执行实例详情
# */
# drop table if exists `batch_job_instance_details`;
# CREATE TABLE `batch_job_instance_details` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `instance_id` bigint(20) NOT NULL COMMENT '实例ID',
#   `subjob_instance_id` bigint(20) NOT NULL COMMENT '子作业实例ID',
#   `type` int(2) NOT NUll COMMENT '类型 1 数据同步 2 SQL脚本 3 备份。 主要用于后期扩展',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8 COMMENT='批处理作业执行实例详情';


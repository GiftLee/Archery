--  删除Themis权限
set @perm_id=(select id from auth_permission where codename='menu_themis');
delete from auth_group_permissions where permission_id=@perm_id;
delete from sql_users_user_permissions where permission_id=@perm_id;
delete from auth_permission where codename='menu_themis';

-- 添加钉钉user id
alter table sql_users
  add ding_user_id varchar(50) default null comment '钉钉user_id';

insert into django_q_schedule(func,schedule_type,repeats,task,name) values
  ('sql.tasks.ding.sync_ding_user_id','D',-2,'31144b2144724d7b81fe663e0211094b','同步钉钉用户ID');

-- 增加实例账号表
CREATE TABLE `instance_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(16) NOT NULL COMMENT '账号',
  `host` varchar(64) NOT NULL COMMENT '主机',
  `password` varchar(32) NULL COMMENT '密码',
  `remark` varchar(255) NOT NULL COMMENT '备注',
  `sys_time` datetime(6) NOT NULL COMMENT '系统时间',
  `instance_id` int(11) NOT NULL COMMENT '实例',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_instance_id_user_host` (`instance_id`,`user`,`host`),
  CONSTRAINT `fk_account_sql_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `sql_instance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

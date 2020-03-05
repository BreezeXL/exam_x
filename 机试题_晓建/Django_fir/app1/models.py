from django.db import models


# Create your models here.
class Article(models.Model):
    # id(主键\自增长)
    article_id = models.AutoField(primary_key=True)
    # 标题(文本类型)
    title = models.TextField()
    # 摘要,简介(文本类型)
    brief_content = models.TextField()
    # 内容(文本类型)
    content = models.TextField()
    # 发布日期(时间类型)
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
"""
 创建迁移文件
python manage.py makemigrations

执行上面的代码,并生成数据库中的表
python manage.py migrate

sqllite3
"""

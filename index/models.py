from django.db import models

# Create your models here.
#用户类
class User(models.Model):
    uphone = models.CharField(max_length=11,verbose_name='手机号',unique=True)
    upwd = models.CharField(max_length=32,verbose_name='密码')
    uname = models.CharField(max_length=20,verbose_name='用户名')
    uemail = models.EmailField(verbose_name='邮箱')
    isActive = models.BooleanField(verbose_name='是否激活',default=True)

    def __str__(self):
        return self.uname

    class Meta:
        # 当前User类对应的数据表表名
        db_table = 'User'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

#商品类型类
class GoodsType(models.Model):
    title = models.CharField(max_length=20,verbose_name='品类名称')
    desc = models.CharField(max_length=200,verbose_name='品类描述')

    def __str__(self):
        return self.title

    class Meta:
        # 当前GoodsType类对应的数据表表名
        db_table = 'goods_type'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

#商品类
class Goods(models.Model):
    title = models.CharField(max_length=20,verbose_name='商品名称')
    price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='价格')
    spec = models.CharField(max_length=11,verbose_name='规格')
    picture = models.ImageField(upload_to='static/upload/goods',verbose_name='商品图片')
    goodsType = models.ForeignKey(GoodsType)
    isActive = models.BooleanField(verbose_name='是否上架',default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # 当前Goods类对应的数据表表名
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name




## uv 相关
1. `uv add Django` 来保证环境中有 django 可以使用


## django 相关
### django 常用命令
1. 在 folder_name 文件夹下创建 project_name 项目：`django-admin startproject project_name folder_name`
2. 创建名为 app_name 的app ：uv run manage.py startapp app_name（注意 manage.py 处于创建的项目文件夹下）
3. 执行 app_name 下的测试用例：`uv run manage.py test app_name`
4. 生成 app_name 的迁移脚本：`uv run manage.py makemigrations app_name`
5. 执行迁移：`uv run manage.py migrate`


### django.db.models
1. db_index=True：为该字段自身创建索引（除去自动添加索引的情况），也可以使用 Meta 类下的 indexes
2. Meta.indexes ：自定义索引，在对应的 Model 类下的 META 类中指定 indexes，可以设定单列索引也可以设置多列索引，比 db_index 更加灵活
    1. fields：必选，字段列表（遵循最左前缀原则：查询条件必须从复合索引的最左边字段开始，连续匹配，才能有效利用索引）
    2. name：非必选，索引名称
    3. condition：部分索引条件（PostgreSQL）
    4. opclasses：操作符类（PostgreSQL）
3. auto_now_add 与 auto_now： DateField、DateTimeField、TimeField 设定字段，auto_now_add 记录创建时间，auto_now 记录最后修改时间
4. on_delete：约束一个记录与其关联对象之间的关系。关联对象删除时，当前对象该如何？
    1. 必须一起删除（强归属）   → CASCADE。例：订单项、评论、附件
    2. 必须保留，但可无主       → SET_NULL。例：文章作者、操作日志用户（需要搭配 null=True 使用）
    3. 必须保留，且有默认归属   → SET_DEFAULT。例：未分类文章、待定部门员工
    4. 阻止删除（保护数据）     → PROTECT（不能删） / RESTRICT（要删一起删）。例：有商品的分类、有员工的部门
    5. 自定义逻辑               → SET(callable)。例：归档到特定用户、随机分配
    6. 数据库处理               → DO_NOTHING

### django 交互式数据库 Api
1. save 方法：对实例 a 使用 `a.save()` 可以将该实例存入对应类所代表的数据表中，创建或是对已存在的记录都可以使用该方法进行保存
2. objects：每个模型（Django 数据库类）中默认存在的 Manager，通过它可以对数据库进行操作
    1. all()：`SampleClass.objects.all()` 会返回所有在 `SampleClass` 数据表中的数据，通过修改 `SampleClass` 中的 `get_queryset` 方法可以自定义该方法的行为
    2. filter()：`SampleClass.objects.filter(condition)` 会返回所有在 `SampleClass` 数据表中满足 condition 的数据

### django 属性名
django 中有许多的固定的属性名，不能随便更改
1. 通用视图： 
    1. `context_object_name`：指定在模板中使用的上下文变量的名称
2. ModeAdmin：
    1. `fields` 列表用于简单的显示字段，如：```fields = ["question_text", "pub_date"]```
    2. `fieldsets` 列表用于分组显示字段，如：
        ```python
        fieldsets = [
            (None, {"fields": ["question_text"]}),
            ("时间信息", {"fields": ["pub_date"]}),
        ]
        ```

### django 使用方法记录
1. 在修改 css 后发现网页端未生效：可能是因为浏览器缓存的原因，使用 Ctrl+Shift+R 来硬刷新
2. 通过 django shell 来查看记录，如：`Question.objects.first()` 取出记录，然后可以用点语法来查看属性
3. BASE_DIR 指的是与 manage.py 同级别的路径

## Python 相关
### import
1. `from . import views` 与 `import views` 的搜索起点不同，前者从当前文件的目录开始，后者从项目根目录（和 `sys.path`、PYTHONPATH 等）开始搜索
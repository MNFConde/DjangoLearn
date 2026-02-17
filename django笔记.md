
## uv 相关
1. uv add Django 来保证环境中有 django 可以使用
2. uv run django-admin startproject projectname 来创建环境
3. uv run manage.py test app_name 来执行 app 下的测试用例

## django 相关
### django 常用命令
1. 创建项目：`django-admin startproject project名称 文件夹名称`
2. 创建app ：uv run manage.py startapp app_name（注意 manage.py 处于创建的项目文件夹下）


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
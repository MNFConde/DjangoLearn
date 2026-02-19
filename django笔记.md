
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
2. Meta.indexes ：自定义索引，在对应的 Model 类下的 META 类中指定 indexes，可以设定单列索引也可以设置多列索引，比 db_index 更加灵活；每一个 indexes 列表中的元素都由 `models.Index` 生成， 参数如下：
    1. fields：必选，字段列表（遵循 `最左前缀原则` ：查询条件必须从复合索引的最左边字段开始，连续匹配，才能有效利用索引）
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
3. ManyToManyField 会自动创建中间表并处理索引，所以不需要手动为它创建索引
4. 应当优先使用通用视图来实现需求：[基于类的视图](https://docs.djangoproject.com/zh-hans/6.0/topics/class-based-views/)、[内置类视图 API](https://docs.djangoproject.com/en/6.0/ref/class-based-views/)

### django.core.paginator
1. Paginator 分页器可以将查询数据按照指定的个数进行分组，如 `paginator = Paginator(article_list, 10)`
2. 获取指定页码对象：`page_obj = paginator.get_page(page_number)`
3. 页码对象常用属性与方法：
    ```python
    # 当前页数据
    page_obj.object_list      # 当前页的 10 篇文章（QuerySet）
    page_obj.number           # 当前页码（整数）

    # 导航判断
    page_obj.has_previous()   # 是否有上一页（Bool）
    page_obj.has_next()       # 是否有下一页（Bool）
    page_obj.has_other_pages() # 是否有多页（Bool）

    # 页码获取
    page_obj.previous_page_number()  # 上一页页码
    page_obj.next_page_number()      # 下一页页码

    # 总信息
    page_obj.paginator        # 关联的 Paginator 对象
    page_obj.paginator.count  # 总记录数
    page_obj.paginator.num_pages  # 总页数
    ```

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

### django Pytest 测试
#### pytest 注意事项
1. pytest 更加推荐使用纯函数而非类方法来编写测试用例
#### FactoryBoy 生成数据
1. 定义工厂
    ```python
    # factories.py
    import factory
    from django.contrib.auth.models import User

    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = User  # 指定该工厂对应的 Django 模型

        username = factory.Faker("user_name")           # 使用 Faker 生成随机用户名
        email = factory.Faker("email")                  # 随机邮箱
        first_name = factory.Faker("first_name")        # 随机名
        last_name = factory.Faker("last_name")          # 随机姓
        is_active = True                                # 固定值
    ```
2. 使用工厂创建对象
    ```python
    # 在测试中
    from myapp.factories import UserFactory

    # .build() - 创建对象但不保存到数据库（速度快，适合单元测试）
    user = UserFactory.build()
    assert user.pk is None  # 没有主键，未保存

    # .create() - 创建并保存对象到数据库（默认策略，适合需要数据库交互的测试）
    saved_user = UserFactory.create()  # 等同于 UserFactory()
    assert saved_user.pk is not None

    # .stub() - 创建存根对象，只包含属性，没有任何方法（最轻量）
    stub_user = UserFactory.stub()

    # 批量创建
    users = UserFactory.create_batch(5, is_active=False)  # 创建5个非活跃用户
    ```
3. 字段声明
    1. 静态值：直接赋值
    2. Faker：
        1. 传入指定的生成器名称
            ```python
            from faker import Faker

            fake = Faker('zh_CN')  # 指定中文

            # 按类别整理
            categories = {
                '基础': ['boolean', 'random_int', 'random_digit', 'pystr', 'pyint', 'pyfloat', 'pydecimal', 'pybool'],
                '个人': ['name', 'first_name', 'last_name', 'email', 'phone_number', 'ssn', 'date_of_birth'],
                '地址': ['address', 'street_address', 'city', 'state', 'country', 'postcode', 'latitude', 'longitude'],
                '文本': ['text', 'sentence', 'paragraph', 'word', 'words', 'slug', 'catch_phrase'],
                '日期': ['date', 'date_time', 'time', 'future_date', 'past_date', 'iso8601'],
                '网络': ['url', 'domain_name', 'ipv4', 'ipv6', 'mac_address', 'user_agent', 'email'],
                '商业': ['company', 'job', 'catch_phrase', 'bs'],
                '编码': ['uuid4', 'ean', 'ean13', 'isbn10', 'isbn13'],
                '文件': ['file_name', 'file_path', 'mime_type', 'image_url'],
                '金融': ['credit_card_number', 'iban', 'currency'],
            }

            # 验证并打印
            for cat, methods in categories.items():
                print(f"\n【{cat}】")
                for method in methods:
                    try:
                        result = getattr(fake, method)()
                        # 截断长输出
                        result_str = str(result)[:50]
                        print(f"  {method:20s} → {result_str}")
                    except Exception as e:
                        print(f"  {method:20s} → 错误: {e}")
            ```
        2. 可能存在的额外参数
            | 参数名                         | 用途    | 示例                      |
            | :-------------------------- | :---- | :---------------------- |
            | `min` / `max`               | 整数范围  | `random_int`            |
            | `min_value` / `max_value`   | 数值范围  | `pyfloat`, `pydecimal`  |
            | `length` / `max_nb_chars`   | 文本长度  | `pystr`, `text`         |
            | `nb_words` / `nb_sentences` | 词/句数量 | `sentence`, `paragraph` |
            | `start_date` / `end_date`   | 日期范围  | `date_between`          |
            | `tzinfo`                    | 时区    | `date_time`             |
            | `locale`                    | 语言    | 全局或实例设置                 |
            | `pattern`                   | 格式字符串 | `date`, `time`          |
        3. 自定义，需要自定义 `Provider`：
            ```python
            from faker.providers import BaseProvider

            class MyProvider(BaseProvider):
                def status_code(self):
                    """自定义 HTTP 状态码"""
                    return self.random_element([200, 201, 400, 401, 404, 500])
                
                def http_method(self):
                    """自定义 HTTP 方法"""
                    return self.random_element(['GET', 'POST', 'PUT', 'DELETE'])

            # 注册
            fake = Faker()
            fake.add_provider(MyProvider)

            # 现在可以用了
            print(fake.status_code())   # 200
            print(fake.http_method())   # "POST"
            ```
    3. Sequence：生成唯一值，常用于邮箱、用户名等字段
        ```python
        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User

            username = factory.Sequence(lambda n: f"user_{n:03d}")  # 生成 user_001, user_002...
            email = factory.Sequence(lambda n: f"user{n}@example.com")
        ```
    4. 懒属性（LazyAttribute）：根据对象其他属性动态计算值（需要别的属性赋值了才能计算出来的属性）
        ```python
        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User

            first_name = factory.Faker("first_name")
            last_name = factory.Faker("last_name")
            # 根据 first_name 和 last_name 生成邮箱
            email = factory.LazyAttribute(lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.com")
        ```
    5. 懒函数（LazyFunction）：延迟执行函数的工具，在对象创建时才调用函数获取值，而非定义时立即执行，常用于生成时间。
        ```python
        import datetime

        class SessionFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Session

            expires_at = factory.LazyFunction(lambda: datetime.datetime.now() + datetime.timedelta(days=7))
        ```
4. 处理模型关联
    1. 外键关系（使用 SubFactory）：当 Book 属于一个 Author 时
        ```python
        # models.py
        class Author(models.Model):
            name = models.CharField(max_length=100)

        class Book(models.Model):
            title = models.CharField(max_length=100)
            author = models.ForeignKey(Author, on_delete=models.CASCADE)

        # factories.py
        class AuthorFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Author
            name = factory.Faker("name")

        class BookFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Book
            title = factory.Faker("catch_phrase")
            author = factory.SubFactory(AuthorFactory)  # 自动创建关联的 Author
        ```
        使用时，BookFactory() 会自动创建并关联一个 Author 实例。也可以在创建时覆盖关联对象的属性
        ```python
        # 传递参数给 SubFactory（使用双下划线语法）
        book = BookFactory(author__name="Jane Smith")
        print(book.author.name)  # 输出 "Jane Smith"
        ```
    2. 反向关系（使用 RelatedFactory）：当一个 Author 有多个 Book 时，可以在 AuthorFactory 中创建关联的 Book
        ```python
        class AuthorFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Author
            name = factory.Faker("name")

            # 创建一个关联的 Book 实例，并自动将当前 author 对象传递给 book 的 author 字段
            book = factory.RelatedFactory(BookFactory, factory_related_name='author')
        ```
        > 注意：RelatedFactory 通常与 SubFactory 配合使用，用于在创建主对象时顺便创建从属对象。
    3. 多对多关系：可以通过 post_generation 钩子来添加关联
        ```python
        class BookWithAuthorsFactory(BookFactory):
            @factory.post_generation
            def authors(self, create, extracted, **kwargs):
                if not create:
                    return
                if extracted:  # 如果传入了 authors 列表
                    for author in extracted:
                        self.authors.add(author)
                else:  # 默认添加一个作者
                    self.authors.add(AuthorFactory())
        ```
5. 高级特性
    1. 特性（Traits）：定义一组命名的属性组合，指定该组合为 true，就能将实例的参数修改为指定的组合
        ```python
        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User

            username = factory.Faker("user_name")
            is_active = True
            is_staff = False
            is_superuser = False

            class Params:
                admin = factory.Trait(is_staff=True, is_superuser=True)
                inactive = factory.Trait(is_active=False)
        
        admin_user = UserFactory(admin=True)          # 创建管理员用户
        inactive_user = UserFactory(inactive=True)    # 创建非活跃用户
        ```
    2. 后生成钩子（Post-generation hooks）：在对象创建后执行自定义逻辑，如处理多对多关系或触发副作用
        ```python
        class ProductFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Product

            name = factory.Faker("word")
            price = factory.Faker("pydecimal", left_digits=3, right_digits=2)

            @factory.post_generation
            def set_sale_price(self, create, extracted, **kwargs):
                """如果 extracted 为 True，则应用折扣"""
                if extracted:
                    self.price = self.price * 0.85  # 15% off
        ```
        
        

## Python 相关
### import
1. `from . import views` 与 `import views` 的搜索起点不同，前者从当前文件的目录开始，后者从项目根目录（和 `sys.path`、PYTHONPATH 等）开始搜索
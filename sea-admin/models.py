from exp import db


# 用户表
class User(db.Model):
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(128), nullable=False)  # 密码
    role = db.Column(db.Integer, nullable=False)  # 角色: 1-管理员, 2-科研人员, 3-普通用户
    full_name = db.Column(db.String(100), nullable=True)  # 姓名
    phone_number = db.Column(db.String(15), unique=True, nullable=True)  # 手机号
    imageUrl = db.Column(db.String(200), nullable=True)  # 图像
    status = db.Column(db.Integer, nullable=False)  # 状态: 1-正常, 2-禁用

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'status': self.status,
            'imageUrl': self.imageUrl,

        }


# 海洋区域特征表
class OceanRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)  # 区域名称
    location = db.Column(db.String(200), nullable=False)  # 地理位置
    temperature = db.Column(db.Float, nullable=False)  # 海水温度
    salinity = db.Column(db.Float, nullable=False)  # 盐度
    status = db.Column(db.Integer, nullable=False)  # 状态
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<OceanRegion %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'temperature': self.temperature,
            'salinity': self.salinity,
            'status': self.status,
            'time': self.time,
        }


# 海洋区域特征评论表
class OceanRegionFeatureComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ocean_region_id = db.Column(db.Integer, nullable=False)  # 海洋区域表ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    comment = db.Column(db.Text, nullable=False)  # 评论
    status = db.Column(db.Integer, nullable=False)  # 状态
    comment_time = db.Column(db.DateTime, nullable=False)  # 评论时间
    likes = db.Column(db.Integer, nullable=True)  # 状态
    score = db.Column(db.Float, nullable=True)
    user_id_like = db.Column(db.Integer, nullable=True)  # 点赞用户ID

    def __repr__(self):
        return '<OceanRegionFeatureComment %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'ocean_region_id': self.ocean_region_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'status': self.status,
            'comment_time': self.comment_time,
        }


# 海洋区域特征评论表
class OceanRegionFeatureCommentNew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ocean_region_feather_comment_id = db.Column(db.Integer, nullable=False)  # 海洋区域表ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    comment = db.Column(db.Text, nullable=False)  # 评论
    status = db.Column(db.Integer, nullable=False)  # 状态
    comment_time = db.Column(db.DateTime, nullable=False)  # 评论时间

    def __repr__(self):
        return '<OceanRegionFeatureCommentNew %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'ocean_region_feather_comment_id': self.ocean_region_feather_comment_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'status': self.status,
            'comment_time': self.comment_time,
            'likes': self.likes
        }


# 海洋生物表
class MarineLife(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)  # 生物名称 scientificname

    originalscientificname = db.Column(db.String(255), nullable=False)  # 原学名 2

    species = db.Column(db.String(255), nullable=False)  # 种类
    habitat_region = db.Column(db.String(255), nullable=False)  # 栖息区域 family
    quantity = db.Column(db.Integer, nullable=False)  # 数量

    kingdom = db.Column(db.String(255), nullable=True)  # 2  族群
    # family = db.Column(db.String(255), nullable=True)
    date_year = db.Column(db.Integer, nullable=True)  # 2  年份
    decimallongitude = db.Column(db.Float, nullable=False)  # 2  经度
    decimallatitude = db.Column(db.Float, nullable=False)  # 2  纬度

    status = db.Column(db.Integer, nullable=False)  # 状态
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<MarineLife %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'habitat_region': self.habitat_region,
            'quantity': self.quantity,
            'status': self.status,
            'time': self.time,
        }


# 海洋生物评论表
class MarineLifeComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marine_life_id = db.Column(db.Integer, nullable=False)  # 海洋生物表ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    comment = db.Column(db.Text, nullable=False)  # 评论
    status = db.Column(db.Integer, nullable=False)  # 状态
    comment_time = db.Column(db.DateTime, nullable=False)  # 评论时间
    likes = db.Column(db.Integer, nullable=True)  # 状态
    score = db.Column(db.Float, nullable=True)
    user_id_like = db.Column(db.Integer, nullable=True)  # 点赞用户ID

    def __repr__(self):
        return '<MarineLifeComment %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'marine_life_id': self.marine_life_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'status': self.status,
            'comment_time': self.comment_time,
            'likes': self.likes
        }


# 海洋生物评论表
class MarineLifeCommentNew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marine_life_comment_id = db.Column(db.Integer, nullable=False)  # 海洋生物表ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    comment = db.Column(db.Text, nullable=False)  # 评论
    status = db.Column(db.Integer, nullable=False)  # 状态
    comment_time = db.Column(db.DateTime, nullable=False)  # 评论时间

    def __repr__(self):
        return '<MarineLifeCommentNew %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'marine_life_comment_id': self.marine_life_comment_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'status': self.status,
            'comment_time': self.comment_time,
        }


# 论坛表,包含普通帖子，信息，新闻，section:1普通帖子，2信息，3新闻
class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    status = db.Column(db.Integer, nullable=False)  # 状态
    time = db.Column(db.DateTime, nullable=False)
    section = db.Column(db.Integer, nullable=False)  # 帖子类型

    def __repr__(self):
        return '<Forum %r>' % self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'status': self.status,
            'time': self.time,
        }


# 论坛评论表
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, nullable=False)  # 论坛ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    content = db.Column(db.Text, nullable=False)  # 评论内容
    status = db.Column(db.Integer, nullable=False)  # 状态
    comment_time = db.Column(db.DateTime, nullable=False)  # 评论时间
    likes = db.Column(db.Integer, nullable=True)  # 状态
    score = db.Column(db.Float, nullable=True)
    user_id_like = db.Column(db.Integer, nullable=True)  # 点赞用户ID

    def __repr__(self):
        return '<Comment %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'forum_id': self.forum_id,
            'user_id': self.user_id,
            'content': self.content,
            'status': self.status,
            'comment_time': self.comment_time,
            'likes': self.likes
        }


# 论坛评论表
class CommentNew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, nullable=False)  # 论坛ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    content = db.Column(db.Text, nullable=False)  # 评论内容
    status = db.Column(db.Integer, nullable=False)  # 状态
    comment_time = db.Column(db.DateTime, nullable=False)  # 评论时间

    def __repr__(self):
        return '<CommentNew %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'comment_id': self.comment_id,
            'user_id': self.user_id,
            'content': self.content,
            'status': self.status,
            'comment_time': self.comment_time,
        }

# 创建表格
# db.create_all()

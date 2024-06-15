import calendar
import datetime
import json
import os
import time
import predict

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import func, distinct

from models import User, Forum, OceanRegion, MarineLife, Comment, OceanRegionFeatureComment, MarineLifeComment, \
    CommentNew, OceanRegionFeatureCommentNew, MarineLifeCommentNew
import config
from exp import db
from PIL import Image

app = Flask(__name__)
# 允许跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# 配置数据库连接地址，这里使用 MySQL 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_mysql
# 配置数据库追踪修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = 'static'
app.config['STATIC_URL_PATH'] = 'static'

db.init_app(app)


# 注册接口
@app.route('/api/register', methods=['POST'])
def index():
    rdata = json.loads(request.data)
    user = db.session.query(User).filter_by(username=rdata['account']).all()
    if user:
        # print(request.data)
        return jsonify({'code': 1, 'msg': '账号已存在，换个账号吧'})
    else:
        user1 = User(username=rdata['account'],
                     password=rdata['password'],
                     role=3,
                     full_name=rdata['name'],
                     phone_number=rdata['phone'],
                     imageUrl=rdata['img'],
                     status=1)
        db.session.add(user1)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '注册成功'})

# 登录接口
@app.route('/api/login', methods=['POST'])
def add_user():
    rdata = json.loads(request.data)
    user = db.session.query(User).filter_by(username=rdata['accountLogin'], password=rdata['passwordLogin']).first()
    # print(user)
    if user:
        if user.status == 2:
            return jsonify({'code': 1, 'msg': '账号已禁用，请联系管理员'})
        else:
            return jsonify({'code': 0, 'msg': '登录成功', 'data': user.to_dict()})
    else:
        return jsonify({'code': 1, 'msg': '用户名或密码错误'})

# 修改个人信息接口
@app.route('/api/update_info', methods=['POST'])
def update_info():
    rdata = json.loads(request.data)
    print('rdata=', rdata)

    user_id = rdata['id']
    password = rdata['password']

    print('img=', rdata['img'])
    if password:
        db.session.query(User).filter_by(id=user_id) \
            .update({'imageUrl': rdata['img'],
                     'username': rdata['account'],
                     'full_name': rdata['name'],
                     'phone_number': rdata['phone'],
                     'password': rdata['confirmPassword']
                     })
        db.session.commit()
        db.session.close()
        return jsonify({'code': 0, 'msg': '用户名或密码错误'})
    else:
        db.session.query(User).filter_by(id=user_id) \
            .update({'imageUrl': rdata['img'],
                     'username': rdata['account'],
                     'full_name': rdata['name'],
                     'phone_number': rdata['phone'],
                     })
        db.session.commit()
        db.session.close()
        return jsonify({'code': 0, 'msg': '用户名或密码错误'})

# 新增帖子接口
@app.route('/api/add_papers', methods=['POST'])
def add_papers():
    rdata = json.loads(request.data)

    section = rdata['section']

    content = rdata['content'].replace('&lt;', '<').replace('&gt;', '>')
    if 'general' == section or 'info' == section or 'news' == section:
        # print(datetime.datetime.now())
        section_self = 1
        if 'info' == section:
            section_self = 2
        if 'news' == section:
            section_self = 3
        forum = db.session.query(Forum).filter_by(title=rdata['title']).first()
        if forum:
            return jsonify({'code': 1, 'msg': '标题已存在'})
        else:
            forum1 = Forum(title=rdata['title'], content=content, user_id=rdata['userid'], status=1,
                           section=section_self, time=datetime.datetime.now())
            db.session.add(forum1)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '发帖成功'})
    elif 'ocean' == section:
        oceanRegion = db.session.query(OceanRegion).filter_by(title=rdata['title']).first()
        if oceanRegion:
            return jsonify({'code': 1, 'msg': '标题已存在'})
        else:
            oceanRegion1 = OceanRegion(title=rdata['title'], content=content, user_id=rdata['userid'],
                                       status=1, time=datetime.datetime.now())
            db.session.add(oceanRegion1)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '发帖成功'})
    elif 'marine-life' == section:
        marineLife = db.session.query(MarineLife).filter_by(title=rdata['title']).first()
        if marineLife:
            return jsonify({'code': 1, 'msg': '标题已存在'})
        else:
            marineLife1 = MarineLife(title=rdata['title'], content=content, user_id=rdata['userid'],
                                     status=1, time=datetime.datetime.now())
            db.session.add(marineLife1)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '发帖成功'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})

# 获取帖子标题接口
@app.route('/api/paper_list', methods=['POST'])
def paper_list():
    rdata = json.loads(request.data)

    section = rdata['section']
    keyword = rdata['keyword']
    if 'general' == section or 'info' == section or 'news' == section:
        section_self = 1
        if 'info' == section:
            section_self = 2
        if 'news' == section:
            section_self = 3

        if keyword:
            forum = db.session.query(Forum.id, Forum.title, Forum.time, Forum.section, Forum.content, User.imageUrl,
                                     User.username, User.role).join(User, Forum.user_id == User.id) \
                .filter(Forum.status == 1, Forum.section == section_self, Forum.title.like('%' + keyword + '%')) \
                .order_by(Forum.time).all()
        else:
            forum = db.session.query(Forum.id, Forum.title, Forum.time, Forum.section, Forum.content, User.imageUrl,
                                     User.username, User.role).join(User, Forum.user_id == User.id) \
                .filter(Forum.status == 1, Forum.section == section_self).order_by(Forum.time).all()

        forums = [
            {'id': f.id, 'title': f.title, 'time': f.time.strftime('%Y/%m/%d %H:%M:%S'),
             'section': f.section, 'imageUrl': f.imageUrl,
             'content': f.content, 'username': f.username, 'role': f.role} for f in forum]

        if forum:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': forums})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'ocean' == section:
        if keyword:
            oceanRegion = db.session.query(OceanRegion.id,
                                           OceanRegion.name,
                                           OceanRegion.location,
                                           OceanRegion.temperature,
                                           OceanRegion.salinity,
                                           OceanRegion.time,
                                           User.imageUrl,
                                           User.username, User.role).join(User, OceanRegion.user_id == User.id) \
                .filter(OceanRegion.status == 1, OceanRegion.name.like('%' + keyword + '%')) \
                .order_by(OceanRegion.time).all()
        else:
            oceanRegion = db.session.query(OceanRegion.id,
                                           OceanRegion.name,
                                           OceanRegion.location,
                                           OceanRegion.temperature,
                                           OceanRegion.salinity,
                                           OceanRegion.time,
                                           User.imageUrl,
                                           User.username, User.role).join(User, OceanRegion.user_id == User.id) \
                .filter(OceanRegion.status == 1).order_by(OceanRegion.time).all()

        oceanRegions = [
            {'id': f.id, 'name': f.name, 'time': f.time.strftime('%Y/%m/%d %H:%M:%S'),
             'username': f.username, 'role': f.role, 'imageUrl': f.imageUrl,
             'location': f.location, 'temperature': f.temperature, 'salinity': f.salinity} for f in oceanRegion]

        if oceanRegion:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': oceanRegions})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'marine-life' == section:
        if keyword:
            marineLife = db.session.query(MarineLife.id,
                                          MarineLife.name,
                                          MarineLife.species,
                                          MarineLife.time,
                                          MarineLife.habitat_region,
                                          MarineLife.quantity,
                                          MarineLife.originalscientificname,
                                          MarineLife.kingdom,
                                          MarineLife.date_year,
                                          MarineLife.decimallongitude,
                                          MarineLife.decimallatitude,
                                          User.imageUrl,
                                          User.username, User.role).join(User, MarineLife.user_id == User.id) \
                .filter(MarineLife.status == 1, MarineLife.name.like('%' + keyword + '%')) \
                .order_by(MarineLife.time).all()
        else:
            marineLife = db.session.query(MarineLife.id,
                                          MarineLife.name,
                                          MarineLife.species,
                                          MarineLife.time,
                                          MarineLife.habitat_region,
                                          MarineLife.quantity,
                                          MarineLife.originalscientificname,
                                          MarineLife.kingdom,
                                          MarineLife.date_year,
                                          MarineLife.decimallongitude,
                                          MarineLife.decimallatitude,
                                          User.imageUrl,
                                          User.username, User.role).join(User, MarineLife.user_id == User.id) \
                .filter(MarineLife.status == 1).order_by(MarineLife.time).all()

        marineLifes = [
            {'id': f.id, 'name': f.name, 'species': f.species, 'time': f.time.strftime('%Y/%m/%d %H:%M:%S'),
             'originalscientificname': f.originalscientificname, 'kingdom': f.kingdom, 'date_year': f.date_year,
             'decimallongitude': f.decimallongitude, 'decimallatitude': f.decimallatitude,
             'username': f.username, 'role': f.role, 'imageUrl': f.imageUrl,
             'habitat_region': f.habitat_region, 'quantity': f.quantity} for f in marineLife]

        if marineLife:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 获取帖子所有评论接口
@app.route('/api/paper_content', methods=['POST'])
def paper_content():
    rdata = json.loads(request.data)

    paper_id = rdata['paper_id']  # forum_id
    section = rdata['section']
    user_id = rdata['user_id']
    if 'general' == section or 'info' == section or 'news' == section:
        comment = db.session.query(Comment.id,
                                   Comment.forum_id,
                                   Comment.comment_time,
                                   Comment.content,
                                   Comment.likes,
                                   Comment.user_id_like,
                                   User.username,
                                   User.role,
                                   User.imageUrl
                                   ).join(User, Comment.user_id == User.id) \
            .filter(Comment.status == 1, Comment.forum_id == paper_id).order_by(Comment.comment_time).all()

        # 获取分数
        score = db.session.query(func.count(Comment.id), func.sum(Comment.score)) \
            .filter(Comment.score > 0, Comment.forum_id == paper_id).first()

        if score[0] > 0:
            if score[1]:
                sc = round(score[1] / score[0], 2)
            else:
                sc = 0
        else:
            sc = 0

        comments = [
            {'id': f.id, 'forum_id': f.forum_id, 'likes': f.likes, 'sc': sc, 'user_id_like': f.user_id_like,
             'comment_time': f.comment_time.strftime('%Y/%m/%d %H:%M:%S'),
             'content': f.content, 'username': f.username, 'role': f.role, 'imageUrl': f.imageUrl} for f in comment]

        for com in comments:
            uil = com['user_id_like']
            if uil:
                ui = uil.split(',')
                if user_id in ui:
                    com['liked'] = 1
                else:
                    com['liked'] = 0
            else:
                com['liked'] = 0
            newComment = db.session.query(CommentNew.content,
                                          CommentNew.comment_time,
                                          User.username) \
                .join(User, CommentNew.user_id == User.id) \
                .filter(CommentNew.status == 1, CommentNew.comment_id == com['id']) \
                .order_by(CommentNew.comment_time).all()
            if newComment:
                newc = [{'content': n.content, 'usernamen': n.username,
                         'ctime': n.comment_time.strftime('%Y/%m/%d %H:%M:%S')} for n in newComment]
                com['newComments'] = newc
            else:
                com['newComments'] = []

        if comment:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': comments})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})

    elif 'ocean' == section:
        oceanRegionFeatureComment = db.session.query(OceanRegionFeatureComment.id,
                                                     OceanRegionFeatureComment.ocean_region_id,
                                                     OceanRegionFeatureComment.comment_time,
                                                     OceanRegionFeatureComment.comment,
                                                     OceanRegionFeatureComment.likes,
                                                     OceanRegionFeatureComment.user_id_like,
                                                     User.username,
                                                     User.imageUrl,
                                                     User.role).join(User, OceanRegionFeatureComment.user_id == User.id) \
            .filter(OceanRegionFeatureComment.status == 1,
                    OceanRegionFeatureComment.ocean_region_id == paper_id).order_by(
            OceanRegionFeatureComment.comment_time).all()

        # 获取分数
        score = db.session.query(func.count(OceanRegionFeatureComment.id), func.sum(OceanRegionFeatureComment.score)) \
            .filter(OceanRegionFeatureComment.score > 0, OceanRegionFeatureComment.ocean_region_id == paper_id).first()

        # print('score=', score)

        if score[0] > 0:
            if score[1]:
                sc = round(score[1] / score[0], 2)
            else:
                sc = 0
        else:
            sc = 0

        oceanRegionFeatureComments = [
            {'id': f.id, 'forum_id': f.ocean_region_id, 'likes': f.likes, 'sc': sc, 'user_id_like': f.user_id_like,
             'comment_time': f.comment_time.strftime('%Y/%m/%d %H:%M:%S'),
             'content': f.comment, 'username': f.username, 'role': f.role, 'imageUrl': f.imageUrl} for f in
            oceanRegionFeatureComment]

        for com in oceanRegionFeatureComments:
            uil = com['user_id_like']
            if uil:
                ui = uil.split(',')
                if user_id in ui:
                    com['liked'] = 1
                else:
                    com['liked'] = 0
            else:
                com['liked'] = 0
            # print('com', com)
            # print('com["id"]', com['id'])
            newComment = db.session.query(OceanRegionFeatureCommentNew.comment,
                                          OceanRegionFeatureCommentNew.comment_time,
                                          User.username) \
                .join(User, OceanRegionFeatureCommentNew.user_id == User.id) \
                .filter(OceanRegionFeatureCommentNew.status == 1,
                        OceanRegionFeatureCommentNew.ocean_region_feather_comment_id == com['id']) \
                .order_by(OceanRegionFeatureCommentNew.comment_time).all()

            if newComment:
                newc = [{'content': n.comment, 'usernamen': n.username,
                         'ctime': n.comment_time.strftime('%Y/%m/%d %H:%M:%S')} for n in newComment]
                com['newComments'] = newc
            else:
                com['newComments'] = []

        if oceanRegionFeatureComment:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': oceanRegionFeatureComments})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'marine-life' == section:
        marineLifeComment = db.session.query(MarineLifeComment.id,
                                             MarineLifeComment.marine_life_id,
                                             MarineLifeComment.comment_time,
                                             MarineLifeComment.comment,
                                             MarineLifeComment.likes,
                                             MarineLifeComment.user_id_like,
                                             User.username,
                                             User.imageUrl,
                                             User.role).join(User, MarineLifeComment.user_id == User.id) \
            .filter(MarineLifeComment.status == 1, MarineLifeComment.marine_life_id == paper_id).order_by(
            MarineLifeComment.comment_time).all()

        # 获取分数
        # score = db.session.query(func.count(MarineLifeComment.id).label('cid'),
        #                          func.count(MarineLifeComment.score).label('scount')) \
        #     .filter(MarineLifeComment.score > 0,
        #             MarineLifeComment.marine_life_id == paper_id).first()
        #
        # if score['cid'] > 0:
        #     sc = round(score['scount'] / score['cid'], 2)
        # else:
        #     sc = 0

        # 获取分数
        score = db.session.query(func.count(MarineLifeComment.id),
                                 func.sum(MarineLifeComment.score)) \
            .filter(MarineLifeComment.score > 0,
                    MarineLifeComment.marine_life_id == paper_id).first()

        # print('score=', score)

        if score[0] > 0:
            if score[1]:
                sc = round(score[1] / score[0], 2)
            else:
                sc = 0
        else:
            sc = 0

        marineLifeComments = [
            {'id': f.id, 'forum_id': f.marine_life_id, 'likes': f.likes, 'sc': sc, 'user_id_like': f.user_id_like,
             'comment_time': f.comment_time.strftime('%Y/%m/%d %H:%M:%S'),
             'content': f.comment, 'username': f.username, 'role': f.role, 'imageUrl': f.imageUrl} for f in
            marineLifeComment]

        for com in marineLifeComments:
            uil = com['user_id_like']
            if uil:
                ui = uil.split(',')
                if user_id in ui:
                    com['liked'] = 1
                else:
                    com['liked'] = 0
            else:
                com['liked'] = 0
            # print('com', com)
            # print('com["id"]', com['id'])
            newComment = db.session.query(MarineLifeCommentNew.comment,
                                          MarineLifeCommentNew.comment_time,
                                          User.username) \
                .join(User, MarineLifeCommentNew.user_id == User.id) \
                .filter(MarineLifeCommentNew.status == 1,
                        MarineLifeCommentNew.marine_life_comment_id == com['id']) \
                .order_by(MarineLifeCommentNew.comment_time).all()

            if newComment:
                newc = [{'content': n.comment, 'usernamen': n.username,
                         'ctime': n.comment_time.strftime('%Y/%m/%d %H:%M:%S')} for n in newComment]
                com['newComments'] = newc
            else:
                com['newComments'] = []

        if marineLifeComment:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifeComments})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 评论接口
@app.route('/api/add_comment', methods=['POST'])
def add_comment():
    rdata = json.loads(request.data)

    paper_id = rdata['paper_id']  # forum_id or comment_id
    user_id = rdata['user_id']
    section = rdata['section']
    newComment = rdata['newComment']
    # score = rdata['score']
    # print('section==', section)
    if 'general' == section or 'info' == section or 'news' == section:
        comment = Comment(forum_id=paper_id,
                          user_id=user_id,
                          content=newComment,
                          comment_time=datetime.datetime.now(),
                          likes=0,
                          score=rdata['score'],
                          status=1)
        db.session.add(comment)
        db.session.commit()

        if comment:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    elif 'general_new' == section or 'info_new' == section or 'news_new' == section:
        commentNew = CommentNew(comment_id=paper_id,
                                user_id=user_id,
                                content=newComment,
                                comment_time=datetime.datetime.now(),
                                status=1)
        db.session.add(commentNew)
        db.session.commit()

        if commentNew:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    elif 'ocean' == section:
        oceanRegionFeatureComment = OceanRegionFeatureComment(ocean_region_id=paper_id,
                                                              user_id=user_id,
                                                              comment=newComment,
                                                              comment_time=datetime.datetime.now(),
                                                              likes=0,
                                                              score=rdata['score'],
                                                              status=1)
        db.session.add(oceanRegionFeatureComment)
        db.session.commit()

        if oceanRegionFeatureComment:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    elif 'ocean_new' == section:
        oceanRegionFeatureCommentNew = OceanRegionFeatureCommentNew(ocean_region_feather_comment_id=paper_id,
                                                                    user_id=user_id,
                                                                    comment=newComment,
                                                                    comment_time=datetime.datetime.now(),
                                                                    status=1)
        db.session.add(oceanRegionFeatureCommentNew)
        db.session.commit()

        if oceanRegionFeatureCommentNew:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    elif 'marine-life' == section:
        marineLifeComment = MarineLifeComment(marine_life_id=paper_id,
                                              user_id=user_id,
                                              comment=newComment,
                                              comment_time=datetime.datetime.now(),
                                              likes=0,
                                              score=rdata['score'],
                                              status=1)
        db.session.add(marineLifeComment)
        db.session.commit()

        if marineLifeComment:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    elif 'marine-life_new' == section:
        marineLifeCommentNew = MarineLifeCommentNew(marine_life_comment_id=paper_id,
                                                    user_id=user_id,
                                                    comment=newComment,
                                                    comment_time=datetime.datetime.now(),
                                                    status=1)
        db.session.add(marineLifeCommentNew)
        db.session.commit()

        if marineLifeCommentNew:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 点赞接口
@app.route('/api/clickLike', methods=['POST'])
def click_like():
    rdata = json.loads(request.data)

    comment_id = rdata['comment_id']
    user_id = rdata['user_id']
    section = rdata['section']
    if 'general' == section or 'info' == section or 'news' == section:
        number = 1
        comment = db.session.query(Comment.likes, Comment.user_id_like).filter(Comment.id == comment_id).first()
        # print('comment.likes==', comment.likes)
        if comment.likes == '' or comment.likes is None:
            pass
        else:
            number = comment.likes + 1

        # print('comment.user_id_like=', comment.user_id_like)
        if comment.user_id_like is None:
            user_id_like = str(user_id)
        else:
            user_id_like = comment.user_id_like + ',' + str(user_id)

        comment1 = db.session.query(Comment).filter_by(id=comment_id) \
            .update({Comment.likes: number, Comment.user_id_like: user_id_like})
        db.session.commit()
        db.session.close()

        if comment1:
            return jsonify({'code': 0, 'msg': '点赞成功'})
        else:
            return jsonify({'code': 1, 'msg': '点赞失败'})

    elif 'ocean' == section:
        number = 1
        oceanRegionFeatureComment = db.session.query(OceanRegionFeatureComment.likes,
                                                     OceanRegionFeatureComment.user_id_like).filter(
            OceanRegionFeatureComment.id == comment_id).first()
        if oceanRegionFeatureComment.likes == '' or oceanRegionFeatureComment.likes is None:
            pass
        else:
            number = oceanRegionFeatureComment.likes + 1

        if oceanRegionFeatureComment.user_id_like is None:
            user_id_like = user_id
        else:
            user_id_like = oceanRegionFeatureComment.user_id_like + ',' + user_id

        oceanRegionFeatureComment1 = db.session.query(OceanRegionFeatureComment).filter_by(id=comment_id) \
            .update({OceanRegionFeatureComment.likes: number, OceanRegionFeatureComment.user_id_like: user_id_like})
        db.session.commit()
        db.session.close()

        if oceanRegionFeatureComment1:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})

    elif 'marine-life' == section:
        number = 1
        marineLifeComment = db.session.query(MarineLifeComment.likes,
                                             MarineLifeComment.user_id_like).filter(
            MarineLifeComment.id == comment_id).first()
        if marineLifeComment.likes:
            pass
        else:
            number = marineLifeComment.likes + 1

        if marineLifeComment.user_id_like is None:
            user_id_like = user_id
        else:
            user_id_like = marineLifeComment.user_id_like + ',' + user_id

        marineLifeComment1 = db.session.query(MarineLifeComment).filter_by(id=comment_id) \
            .update({MarineLifeComment.likes: number, MarineLifeComment.user_id_like: user_id_like})
        db.session.commit()
        db.session.close()

        if marineLifeComment1:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 取消点赞接口
@app.route('/api/clickLikeCancel', methods=['POST'])
def click_like_cancel():
    rdata = json.loads(request.data)

    comment_id = rdata['comment_id']
    user_id = rdata['user_id']
    section = rdata['section']
    if 'general' == section or 'info' == section or 'news' == section:
        number = 0
        comment = db.session.query(Comment.likes,
                                   Comment.user_id_like).filter(Comment.id == comment_id).first()
        # print('comment.likes==', comment.likes)
        if comment.likes == 0:
            pass
        else:
            number = comment.likes - 1

        ulist = comment.user_id_like.split(',')
        if user_id in ulist:
            ulist.remove(user_id)

        user_id_like = ','.join(ulist)

        comment1 = db.session.query(Comment).filter_by(id=comment_id) \
            .update({Comment.likes: number, Comment.user_id_like: user_id_like})
        db.session.commit()
        db.session.close()

        if comment1:
            return jsonify({'code': 0, 'msg': '点赞成功'})
        else:
            return jsonify({'code': 1, 'msg': '点赞失败'})

    elif 'ocean' == section:
        number = 0
        oceanRegionFeatureComment = db.session.query(OceanRegionFeatureComment.likes,
                                                     OceanRegionFeatureComment.user_id_like).filter(
            OceanRegionFeatureComment.id == comment_id).first()
        if oceanRegionFeatureComment.likes == 0:
            pass
        else:
            number = oceanRegionFeatureComment.likes - 1

        ulist = oceanRegionFeatureComment.user_id_like.split(',')
        if user_id in ulist:
            ulist.remove(user_id)

        user_id_like = ','.join(ulist)

        oceanRegionFeatureComment1 = db.session.query(OceanRegionFeatureComment).filter_by(id=comment_id) \
            .update({OceanRegionFeatureComment.likes: number, OceanRegionFeatureComment.user_id_like: user_id_like})
        db.session.commit()
        db.session.close()

        if oceanRegionFeatureComment1:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})

    elif 'marine-life' == section:
        number = 0
        marineLifeComment = db.session.query(MarineLifeComment.likes,
                                             MarineLifeComment.user_id_like).filter(
            MarineLifeComment.id == comment_id).first()
        if marineLifeComment.likes == 0:
            pass
        else:
            number = marineLifeComment.likes - 1

        ulist = marineLifeComment.user_id_like.split(',')
        if user_id in ulist:
            ulist.remove(user_id)

        user_id_like = ','.join(ulist)

        marineLifeComment1 = db.session.query(MarineLifeComment).filter_by(id=comment_id) \
            .update({MarineLifeComment.likes: number, MarineLifeComment.user_id_like: user_id_like})
        db.session.commit()
        db.session.close()

        if marineLifeComment1:
            return jsonify({'code': 0, 'msg': '评论成功'})
        else:
            return jsonify({'code': 1, 'msg': '评论失败'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# ------------------管理员端--------------------------------------------
# 用户列表接口
@app.route('/api/user_list', methods=['POST'])
def user_list():
    rdata = json.loads(request.data)

    keyword = rdata['keyword']

    user = ''
    if keyword:
        user = db.session.query(User).filter(User.role.in_([2, 3]),
                                             User.username.like('%' + keyword + '%')).all()
    else:
        user = db.session.query(User).filter(User.role.in_([2, 3])).all()

    # print(user)

    users = [
        {'id': u.id, 'username': u.username, 'full_name': u.full_name, 'phone_number': u.phone_number,
         'role': u.role, 'status': u.status}
        for u in user]

    # print(users)

    if users:
        return jsonify({'code': 0, 'msg': '查询成功', 'data': users})
    else:
        return jsonify({'code': 1, 'msg': '暂无数据'})


# 升级用户为科学家接口
@app.route('/api/user_change', methods=['POST'])
def user_change():
    rdata = json.loads(request.data)

    user_id = rdata['id']
    user = db.session.query(User).filter_by(id=user_id).update({'role': 2})
    db.session.commit()
    db.session.close()

    if user:
        return jsonify({'code': 0, 'msg': '修改成功'})
    else:
        return jsonify({'code': 1, 'msg': '暂无数据'})


# 降科学家为用户接口
@app.route('/api/user_change_down', methods=['POST'])
def user_change_down():
    rdata = json.loads(request.data)

    user_id = rdata['id']
    user = db.session.query(User).filter_by(id=user_id).update({'role': 3})
    db.session.commit()
    db.session.close()

    if user:
        return jsonify({'code': 0, 'msg': '修改成功'})
    else:
        return jsonify({'code': 1, 'msg': '暂无数据'})


# 解禁禁用用户接口
@app.route('/api/user_disable', methods=['POST'])
def user_disable():
    rdata = json.loads(request.data)

    user_id = rdata['id']
    status = rdata['status']
    user = db.session.query(User).filter_by(id=user_id).update({'status': status})
    db.session.commit()
    db.session.close()

    if user:
        return jsonify({'code': 0, 'msg': '用户更新成功'})
    else:
        return jsonify({'code': 1, 'msg': '暂无数据'})


# 帖子列表接口
@app.route('/api/forum_list', methods=['POST'])
def forum_list():
    rdata = json.loads(request.data)

    keyword = rdata['keyword']
    section = rdata['section']

    if 'general' == section or 'info' == section or 'news' == section:
        section_self = 1
        if 'info' == section:
            section_self = 2
        if 'news' == section:
            section_self = 3

        if keyword:
            forum = db.session.query(Forum.id, Forum.title, Forum.time, Forum.section, Forum.content, Forum.status,
                                     User.username, User.role).join(User, Forum.user_id == User.id) \
                .filter(Forum.section == section_self, Forum.title.like('%' + keyword + '%')) \
                .order_by(Forum.time).all()
        else:
            forum = db.session.query(Forum.id, Forum.title, Forum.time, Forum.section, Forum.content, Forum.status,
                                     User.username, User.role).join(User, Forum.user_id == User.id) \
                .filter(Forum.section == section_self).order_by(Forum.time).all()

        forums = [
            {'id': f.id, 'title': f.title, 'time': f.time.strftime('%Y/%m/%d %H:%M:%S'),
             'section': f.section, 'status': f.status,
             'content': f.content, 'username': f.username, 'role': f.role} for f in forum]

        if forum:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': forums})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'ocean' == section:
        if keyword:
            oceanRegion = db.session.query(OceanRegion.id,
                                           OceanRegion.name,
                                           OceanRegion.location,
                                           OceanRegion.temperature,
                                           OceanRegion.salinity,
                                           OceanRegion.time,
                                           OceanRegion.status,
                                           User.username, User.role).join(User, OceanRegion.user_id == User.id) \
                .filter(OceanRegion.name.like('%' + keyword + '%')) \
                .order_by(OceanRegion.time).all()
        else:
            oceanRegion = db.session.query(OceanRegion.id,
                                           OceanRegion.name,
                                           OceanRegion.location,
                                           OceanRegion.temperature,
                                           OceanRegion.salinity,
                                           OceanRegion.time,
                                           OceanRegion.status,
                                           User.username, User.role).join(User, OceanRegion.user_id == User.id) \
                .order_by(OceanRegion.time).all()

        oceanRegions = [
            {'id': f.id, 'name': f.name, 'time': f.time.strftime('%Y/%m/%d %H:%M:%S'),
             'username': f.username, 'role': f.role, 'status': f.status,
             'location': f.location, 'temperature': f.temperature, 'salinity': f.salinity} for f in oceanRegion]

        if oceanRegion:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': oceanRegions})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'marine-life' == section:
        if keyword:
            marineLife = db.session.query(MarineLife.id,
                                          MarineLife.name,
                                          MarineLife.species,
                                          MarineLife.time,
                                          MarineLife.habitat_region,
                                          MarineLife.quantity,
                                          MarineLife.originalscientificname,
                                          MarineLife.kingdom,
                                          MarineLife.date_year,
                                          MarineLife.decimallongitude,
                                          MarineLife.decimallatitude,
                                          MarineLife.status,
                                          User.username, User.role).join(User, MarineLife.user_id == User.id) \
                .filter(MarineLife.name.like('%' + keyword + '%')) \
                .order_by(MarineLife.time).all()
        else:
            marineLife = db.session.query(MarineLife.id,
                                          MarineLife.name,
                                          MarineLife.species,
                                          MarineLife.time,
                                          MarineLife.habitat_region,
                                          MarineLife.quantity,
                                          MarineLife.originalscientificname,
                                          MarineLife.kingdom,
                                          MarineLife.date_year,
                                          MarineLife.decimallongitude,
                                          MarineLife.decimallatitude,
                                          MarineLife.status,
                                          User.username, User.role).join(User, MarineLife.user_id == User.id) \
                .order_by(MarineLife.time).all()

        marineLifes = [
            {'id': f.id, 'name': f.name, 'species': f.species, 'time': f.time.strftime('%Y/%m/%d %H:%M:%S'),
             'originalscientificname': f.originalscientificname, 'kingdom': f.kingdom, 'date_year': f.date_year,
             'decimallongitude': f.decimallongitude, 'decimallatitude': f.decimallatitude, 'status': f.status,
             'username': f.username, 'role': f.role,
             'habitat_region': f.habitat_region, 'quantity': f.quantity} for f in marineLife]

        if marineLife:
            return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 解禁禁用帖子接口
@app.route('/api/forum_disable', methods=['POST'])
def forum_disable():
    rdata = json.loads(request.data)

    forum_id = rdata['id']
    section = rdata['section']
    status = rdata['status']
    if 'general' == section or 'info' == section or 'news' == section:
        user = db.session.query(Forum).filter_by(id=forum_id).update({'status': status})
        db.session.commit()
        db.session.close()

    elif 'ocean' == section:
        user = db.session.query(OceanRegion).filter_by(id=forum_id).update({'status': status})
        db.session.commit()
        db.session.close()

    elif 'marine-life' == section:
        user = db.session.query(MarineLife).filter_by(id=forum_id).update({'status': status})
        db.session.commit()
        db.session.close()
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})
    if status == 1:
        return jsonify({'code': 0, 'msg': '解禁成功'})
    else:
        return jsonify({'code': 0, 'msg': '禁用成功'})


# 修改帖子接口
@app.route('/api/forum_change', methods=['POST'])
def forum_change():
    rdata = json.loads(request.data)

    print('rdata=', rdata)
    forum_id = rdata['rowid']
    section = rdata['section']
    if 'ocean' == section:
        user = db.session.query(OceanRegion).filter_by(id=forum_id) \
            .update({'name': rdata['name'], 'location': rdata['location'], 'temperature': rdata['temperature'],
                     'salinity': rdata['salinity']})
        db.session.commit()
        db.session.close()

        if user:
            return jsonify({'code': 0, 'msg': '禁用成功'})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'marine-life' == section:

        user = db.session.query(MarineLife).filter_by(id=forum_id) \
            .update({'name': rdata['name'], 'species': rdata['species'], 'habitat_region': rdata['habitat_region'],
                     'quantity': rdata['quantity'], 'originalscientificname': rdata['originalscientificname'],
                     'kingdom': rdata['kingdom'], 'date_year': rdata['date_year'],
                     'decimallongitude': rdata['decimallongitude'], 'decimallatitude': rdata['decimallatitude']
                     })
        db.session.commit()
        db.session.close()

        if user:
            return jsonify({'code': 0, 'msg': '修改成功'})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 新增帖子接口
@app.route('/api/forum_add', methods=['POST'])
def forum_add():
    rdata = json.loads(request.data)

    section = rdata['section']
    if 'ocean' == section:
        oceanRegion = OceanRegion(name=rdata['name'], user_id=rdata['id'], location=rdata['location'],
                                  temperature=rdata['temperature'],
                                  salinity=rdata['salinity'], status=1, time=datetime.datetime.now())
        db.session.add(oceanRegion)
        db.session.commit()
        db.session.close()

        if oceanRegion:
            return jsonify({'code': 0, 'msg': '新增成功'})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    elif 'marine-life' == section:

        marineLife = MarineLife(name=rdata['name'], user_id=rdata['id'], species=rdata['species'],
                                habitat_region=rdata['habitat_region'], quantity=rdata['quantity'],
                                status=1, time=datetime.datetime.now(),
                                originalscientificname=rdata['originalscientificname'],
                                kingdom=rdata['kingdom'], date_year=rdata['date_year'],
                                decimallongitude=rdata['decimallongitude'], decimallatitude=rdata['decimallatitude']
                                )
        db.session.add(marineLife)
        db.session.commit()
        db.session.close()

        if marineLife:
            return jsonify({'code': 0, 'msg': '新增成功'})
        else:
            return jsonify({'code': 1, 'msg': '暂无数据'})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 编辑器图片上传接口
@app.route('/api/file_upload', methods=['POST'])
def file_upload():
    # print(request.files)
    file = request.files['file']
    file_name = file.filename
    suffix = os.path.splitext(file_name)[-1]
    basePath = os.path.dirname(__file__)
    nowTime = calendar.timegm(time.gmtime())
    upload_path = os.path.join(basePath, 'static/upload', str(nowTime))
    upload_path = os.path.abspath(upload_path)
    # file.save(upload_path + suffix)

    image = Image.open(file.stream)
    height = image.height
    width = image.width

    print('height=', height)
    print('width=', width)

    if height > config.height or width > config.width:
        print('height / config.height=', height / config.height)
        print('width / config.width=', width / config.width)

        if width / config.width > height / config.height:
            print('222')
            print('width=', int(width / (height / config.height)))
            print('config.width=', config.width)
            img = image.resize((config.width, int(height / (width / config.width))))  # 宽*高
        else:
            print('333')
            print('config.height=', config.height)
            print('height=', int(height / (width / config.width)))
            img = image.resize((int(width / (height / config.height)), config.height))
        img.save(upload_path + suffix)
    else:
        image.save(upload_path + suffix)

    # print('111=', upload_path + str(nowTime) + suffix)
    # http 路径
    url = config.server_url + '/static/upload/' + str(nowTime) + suffix
    # print('url=', url)
    return jsonify({'code': 0, 'msg': '新增成功', 'data': url})


# 个人信息图片上传接口
@app.route('/api/info_upload', methods=['POST'])
def info_upload():
    # print(request.files)
    file = request.files['file']
    file_name = file.filename
    suffix = os.path.splitext(file_name)[-1]
    basePath = os.path.dirname(__file__)
    nowTime = calendar.timegm(time.gmtime())
    upload_path = os.path.join(basePath, 'static/upload', str(nowTime))
    upload_path = os.path.abspath(upload_path)
    file.save(upload_path + suffix)
    # print('111=', upload_path + str(nowTime) + suffix)
    # http 路径
    url = '/static/upload/' + str(nowTime) + suffix
    # print('url=', url)
    return jsonify({'code': 0, 'msg': '新增成功', 'data': url})


# 获取所有海洋生物接口
@app.route('/api/life_list', methods=['POST'])
def life_list():
    rdata = json.loads(request.data)

    selectType = rdata['selectType']
    if 'kingdom' == selectType:
        marineLife = db.session.query(distinct(MarineLife.kingdom).label('kingdom')).filter(
            MarineLife.status == 1).all()

        marineLifes = [{'name': f.kingdom} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    elif 'habitat_region' == selectType:
        marineLife = db.session.query(distinct(MarineLife.habitat_region).label('habitat_region')).filter(
            MarineLife.status == 1).all()

        marineLifes = [{'name': f.habitat_region} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    elif 'species' == selectType:
        marineLife = db.session.query(distinct(MarineLife.species).label('species')) \
            .filter(MarineLife.status == 1, MarineLife.species != '').all()

        marineLifes = [{'name': f.species} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    elif 'originalscientificname-' == selectType:
        marineLife = db.session.query(
            distinct(MarineLife.originalscientificname).label('originalscientificname')).filter(
            MarineLife.status == 1).all()

        marineLifes = [{'name': f.originalscientificname} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 获取所有海洋生物接口
@app.route('/api/life_selectedOption', methods=['POST'])
def life_selectedOption():
    rdata = json.loads(request.data)

    selectType = rdata['selectType']
    selectedOption = rdata['selectedOption']
    if 'kingdom' == selectType:
        marineLife = db.session.query(distinct(MarineLife.date_year).label('date_year')).filter(
            MarineLife.status == 1, MarineLife.kingdom == selectedOption, MarineLife.date_year > 0) \
            .order_by(MarineLife.date_year).all()

        marineLifes = [{'date_year': f.date_year} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    elif 'habitat_region' == selectType:
        marineLife = db.session.query(distinct(MarineLife.date_year).label('date_year')).filter(
            MarineLife.status == 1, MarineLife.habitat_region == selectedOption, MarineLife.date_year > 0) \
            .order_by(MarineLife.date_year).all()

        marineLifes = [{'date_year': f.date_year} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    elif 'species' == selectType:
        marineLife = db.session.query(distinct(MarineLife.date_year).label('date_year')) \
            .filter(MarineLife.status == 1, MarineLife.species == selectedOption, MarineLife.date_year > 0) \
            .order_by(MarineLife.date_year).all()

        marineLifes = [{'date_year': f.date_year} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    elif 'originalscientificname-' == selectType:
        marineLife = db.session.query(
            distinct(MarineLife.date_year).label('date_year')).filter(
            MarineLife.status == 1, MarineLife.originalscientificname == selectedOption, MarineLife.date_year > 0) \
            .order_by(MarineLife.date_year).all()

        marineLifes = [{'date_year': f.date_year} for f in marineLife]

        return jsonify({'code': 0, 'msg': '查询成功', 'data': marineLifes})
    else:
        return jsonify({'code': 1, 'msg': '你点错了'})


# 获取所有海洋生物接口
@app.route('/api/life_predict', methods=['POST'])
def life_predict():
    rdata = json.loads(request.data)

    code, data = predict.start(rdata)

    if code == 0:
        return jsonify({'code': 0, 'msg': '预测成功', 'data': config.server_url + data.replace("./", '/')})
    else:
        return jsonify({'code': 1, 'msg': '预测失败'})


@app.route('/api/filter_marine_life', methods=['POST'])
def filter_marine_life():
    rdata = json.loads(request.data)
    species = rdata.get('species', '')
    year = rdata.get('year', '')

    query = db.session.query(MarineLife, User.username, User.role, User.imageUrl).join(User, MarineLife.user_id == User.id).filter(MarineLife.status == 1)

    if species:
        query = query.filter(MarineLife.species == species)
    if year:
        query = query.filter(MarineLife.date_year == year)

    marineLifes = query.order_by(MarineLife.time).all()

    result = [
        {'id': f.MarineLife.id, 'name': f.MarineLife.name, 'species': f.MarineLife.species, 'time': f.MarineLife.time.strftime('%Y/%m/%d %H:%M:%S'),
         'originalscientificname': f.MarineLife.originalscientificname, 'kingdom': f.MarineLife.kingdom, 'date_year': f.MarineLife.date_year,
         'decimallongitude': f.MarineLife.decimallongitude, 'decimallatitude': f.MarineLife.decimallatitude,
         'username': f.username, 'role': f.role, 'imageUrl': f.imageUrl,
         'habitat_region': f.MarineLife.habitat_region, 'quantity': f.MarineLife.quantity} for f in marineLifes]

    return jsonify({'code': 0, 'msg': '查询成功', 'data': result}) if marineLifes else jsonify({'code': 1, 'msg': '暂无数据'})

if __name__ == '__main__':
    # 生成数据库表
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

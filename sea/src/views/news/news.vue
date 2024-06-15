<template>
	<!-- 左侧帖子部分 -->
	<div class="left-content" v-if="lists">
		<div class="post-list" style="min-height: 500px;">
			<!-- 查询输入框 -->
			<div class="input-with-button">
				<el-input v-model="keyword" placeholder="请输入查询关键字" class="input"></el-input>
				<el-button type="primary" @click="handleForSearch" class="input_button">查询</el-button>
			</div>

			<div class="forum-table">
				<el-table :data="filteredData" class="custom-table" header-cell-class-name="custom-header">
					<el-table-column prop="title" style="padding: 10px 15px;" label="帖子标题">
						<template #default="{ row }">
							<div @click="handlePostTitleClick(row)" class="post-title">{{ row.title }}</div>
						</template>
					</el-table-column>
					<el-table-column prop="role" label="发帖人角色">
						<template #default="{ row }">
							<span v-if="row.role == 1" class="role admin">管理员</span>
							<span v-if="row.role == 2" class="role scientist">科学家</span>
							<span v-if="row.role == 3" class="role user">用户</span>
						</template>
					</el-table-column>
					<el-table-column prop="time" label="发帖时间">
						<template #default="{ row }">{{ row.time }}</template>
					</el-table-column>
					<el-table-column prop="username" label="发帖人">
						<template #default="{ row }">{{ row.username }}</template>
					</el-table-column>
				</el-table>
			</div>
		</div>

		<!-- 分页器 -->
		<div class="pagination">
			<el-pagination v-model:currentPage="currentPage" :page-size="pageSize" :total="posts.length"
				layout="prev, pager, next" @current-change="handlePageChange" />
		</div>
	</div>

	<!-- 帖子内容 -->
	<div class="forum-detail" v-if="content">
		<!-- 帖子标题 -->
		<div class="post-header">
			<h1 class="post-title">帖子标题：{{ title }}</h1>
			<el-button type="primary" @click="backto" class="back-button">返回帖子列表</el-button>
		</div>
		<div class="forum-table">
			<el-table :data="paperData" border class="custom-table-detail" :show-header="false">
				<el-table-column prop="paperUsername" min-width="15%">
					<template #default="{ row }">
						<div class="post-user">
							<div v-if='row.imageUrl'><img :src="baseUrl + row.imageUrl" class="avatar" /></div>
							<div v-else>
								<div v-if="row.role == 1"><img :src="researcherpng" class="avatar" /></div>
								<div v-if="row.role == 2"><img :src="researcherpng" class="avatar" /></div>
								<div v-if="row.role == 3"><img :src="userpng" class="avatar" /></div>
							</div>

							<div>{{ row.paperUsername }}</div>
							<div v-if="row.role == 1" class="role admin">管理员</div>
							<div v-if="row.role == 2" class="role scientist">科学家</div>
						</div>
					</template>
				</el-table-column>
				<el-table-column prop="paperContent" min-width="85%">
					<template #default="{ row }">
						<div class="post-content-detail">
							<div v-html="row.paperContent"></div>
							<div class="post-meta">
								<div>评分:{{ currentScore }}</div>
								<div>发表于:{{ row.time }}</div>
							</div>
						</div>
					</template>
				</el-table-column>
			</el-table>
			<div class="comment-section-title">评论区</div>
			<el-table :data="tableData" border class="custom-table-detail" :show-header="false">
				<el-table-column prop="username" min-width="15%">
					<template #default="{ row }">
						<div class="post-user">
							<div v-if='row.imageUrl'><img :src="baseUrl + row.imageUrl" class="avatar" /></div>
							<div v-else>
								<div v-if="row.role == 1"><img :src="researcherpng" class="avatar" /></div>
								<div v-if="row.role == 2"><img :src="researcherpng" class="avatar" /></div>
								<div v-if="row.role == 3"><img :src="userpng" class="avatar" /></div>
							</div>
							<div>{{ row.username }}</div>
							<div v-if="row.role == 1" class="role admin">管理员</div>
							<div v-if="row.role == 2" class="role scientist">科学家</div>
						</div>
					</template>
				</el-table-column>
				<el-table-column prop="content" min-width="85%">
					<template #default="{ row }">
						<div class="post-content-detail">
							<div>{{ row.content }}</div>

							<el-table v-if="row.newComments.length != 0" :data="row.newComments" border style="width: 100%;"
								:show-header="false" empty-text=' '>
								<el-table-column min-width="100%">
									<template #default="{ row }">
										<div class="nested-comments">
											<div>{{ row.usernamen }} 的评论：</div>
											<div class="nested-comment-content">{{ row.content }}</div>
										</div>
										<div class="post-meta">
											<div>发表于:{{ row.ctime }}</div>
										</div>
									</template>
								</el-table-column>
							</el-table>

							<div class="post-actions">
								<div @click="pinglun(row)">
									<u class="comment-icon"><el-icon :size="20">
											<ChatRound />
										</el-icon></u>
								</div>
								<div v-if="userid">
									<el-icon v-if="row.liked == 1" :size='24' class="like-icon liked" title="取消点赞"
										@click="clickLikeCancel(row)">
										<StarFilled />
									</el-icon>
									<el-icon v-if="row.liked == 0" :size='24' class="like-icon" title="点赞"
										@click="clickLike(row)">
										<Star />
									</el-icon>
								</div>
								<div v-else>
									<el-icon :size='24' class="like-icon" title="点赞" @click="clickLike(row)">
										<Star />
									</el-icon>
								</div>
								<div v-if="row.likes == null" class="like-count">点赞数：0</div>
								<div v-if="row.likes != null" class="like-count">点赞数：{{ row.likes }}</div>
								<div class="post-time">发布于：{{ row.comment_time }}</div>
							</div>
						</div>
					</template>
				</el-table-column>
			</el-table>
		</div>

		<!-- 分页 -->
		<el-pagination v-model:currentPage="currentPage1" :page-size="pageSize1" :total="totalComments1"
			layout="prev, pager, next" @current-change="handlePageChange1" />

		<!-- 发表评论 -->
		<div class="comment-submit" style="margin-top: 20px;margin-bottom: 10px;">发表评论：</div>
		<el-input v-model="newComment" type="textarea" :rows="5" placeholder="请输入评论内容" class="comment-input"></el-input>
		<h5>评分：</h5>
		<el-rate v-model="score" :max="5" show-text allow-half @change="handleScoreChange"></el-rate>
		<p>您的评分是: {{ score }}</p>
		<el-button type="primary" @click="submitComment" style="margin-top: 10px;">发 表</el-button>
	</div>

	<el-dialog :visible.sync="dialogVisible" v-model="dialogVisible" title=" 评 论 " width="45%" center
		:close-on-click-modal="false">
		<el-input v-model="sendNewComment" type="textarea" :rows="3" placeholder="请输入评论内容" class="comment-input"></el-input>

		<div slot="footer" class="dialog-footer" style="text-align: center

;margin-top: 10px;">
			<el-button @click="dialogVisible = false">取消</el-button>
			<el-button type="primary" @click="sendComment"> 发 表 </el-button>
		</div>
	</el-dialog>
</template>

<script>
import axios from '@/api/index.js'
import { ElMessageBox, ElNotification } from 'element-plus'
import adminpng from '@/assets/admin.jpg'
import researcherpng from '@/assets/researcher.jpg'
import userpng from '@/assets/user.png'
import { baseUrl } from '@/api/index.js'

export default {
	comments: {
		// adminpng,
		// researcherpng,
		// userpng,
	},
	data() {
		return {
			baseUrl: baseUrl,
			//图片
			adminpng: adminpng,
			researcherpng: researcherpng,
			userpng: userpng,

			currentPage: 1,
			keyword: '',
			posts: [],
			filteredData: [],
			pageSize: 15,

			//控制列表和内容显示隐藏
			lists: true,
			content: false,

			//以下为content字段
			paperData: [],  //此为第一行数据准备
			// paperUsername:'',
			// paperContent:'',
			title: '我是一个标题',
			comments: [], //分页前原始数据
			newComment: '',

			totalComments1: 0,
			pageSize1: 10,
			currentPage1: 1,

			tableData: [], //分页数据

			userid: localStorage.getItem('id'), //用户ID，判断是否登录
			paperid: 0,

			currentPost: '',
			dialogVisible: false,

			commentId: 0, //正在评论的评论id
			sendNewComment: '',
			score: 0,
			currentScore: 0,
		};
	},
	computed: {

	},
	created() {
		this.fetchData();
		//console.log(22222);
	},
	methods: {
		clickLike(row) {
			if (this.userid == '' || this.userid == null) {
				ElNotification({
					title: '系统提示',
					message: '请先登录后再点赞',
					duration: 3000,
				})
				return;
			} else {
				axios.post('/api/clickLike', { 'comment_id': row.id, 'section': 'news', 'user_id': this.userid }, { headers: { "Access-Control-Allow-Origin": "*" } })
					.then(response => {
						console.log('2222=', this.currentPost);
						ElNotification({
							title: '系统提示',
							message: '点赞成功',
							duration: 3000,
						})

						this.handlePostTitleClick(this.currentPost);
					})
					.catch(error => {
						// 请求失败，处理错误
						ElNotification({
							title: '系统提示',
							message: '点赞失败',
							duration: 3000,
						})
						console.error('请求数据失败:', error);
					});
			}
		},
		clickLikeCancel(row) {
			if (this.userid == '' || this.userid == null) {
				ElNotification({
					title: '系统提示',
					message: '请先登录后再点赞',
					duration: 3000,
				})
				return;
			} else {
				axios.post('/api/clickLikeCancel', { 'comment_id': row.id, 'section': 'news', 'user_id': this.userid }, { headers: { "Access-Control-Allow-Origin": "*" } })
					.then(response => {
						//console.log('2222=',this.currentPost);
						ElNotification({
							title: '系统提示',
							message: '取消成功',
							duration: 3000,
						})

						this.handlePostTitleClick(this.currentPost);
					})
					.catch(error => {
						// 请求失败，处理错误
						ElNotification({
							title: '系统提示',
							message: '取消失败',
							duration: 3000,
						})
						console.error('请求数据失败:', error);
					});
			}
		},
		sendComment() {
			if (this.userid == '' || this.userid == null) {
				ElNotification({
					title: '系统提示',
					message: '请先登录后再评论',
					duration: 3000,
				})
				return;
			} else {
				if (this.sendNewComment == '') {
					ElNotification({
						title: '系统提示',
						message: '评论不能为空',
						duration: 3000,
					})
					return;
				} else {
					//此处paperid为当前评论ID
					axios.post('/api/add_comment', { 'paper_id': this.commentId, 'user_id': this.userid, 'section': 'news_new', 'newComment': this.sendNewComment }, { headers: { "Access-Control-Allow-Origin": "*" } })
						.then(response => {
							console.log('2222=', this.currentPost);
							// ElNotification({
							//   title: '系统提示',
							//   message: response.data.msg,
							//   duration: 3000,
							// })
							this.dialogVisible = false;
							this.sendNewComment = '';

							this.handlePostTitleClick(this.currentPost);
						})
						.catch(error => {
							// 请求失败，处理错误
							ElNotification({
								title: '系统提示',
								message: '评论失败',
								duration: 3000,
							})
							console.error('请求数据失败:', error);
						});
				}
			}
		},
		pinglun(row) {
			this.dialogVisible = true;
			this.commentId = row.id;
		},
		//返回帖子列表
		backto() {
			this.lists = true;
			this.content = false;
		},

		//发表评论 
		submitComment() {
			//console.log(this.userid);
			if (this.userid == '' || this.userid == null) {
				ElNotification({
					title: '系统提示',
					message: '请先登录后再评论',
					duration: 3000,
				})
				return;
			} else {
				if (this.newComment == '') {
					ElNotification({
						title: '系统提示',
						message: '评论不能为空',
						duration: 3000,
					})
					return;
				} else {
					axios.post('/api/add_comment', { 'paper_id': this.paperid, 'user_id': this.userid, 'section': 'news', 'newComment': this.newComment, 'score': this.score }, { headers: { "Access-Control-Allow-Origin": "*" } })
						.then(response => {
							console.log('2222=', this.currentPost);
							// ElNotification({
							//   title: '系统提示',
							//   message: response.data.msg,
							//   duration: 3000,
							// })
							this.newComment = '';

							this.handlePostTitleClick(this.currentPost);
						})
						.catch(error => {
							// 请求失败，处理错误
							ElNotification({
								title: '系统提示',
								message: '评论失败',
								duration: 3000,
							})
							console.error('请求数据失败:', error);
						});
				}
			}
		},
		handlePageChange1(page) {
			//console.log('page=',page);
			//console.log('currentPage1=',this.currentPage1);
			this.currentPage1 = page;
			this.handleSearch1();
		},
		handlePageChange(page) {
			this.currentPage = page;
			this.handleSearch();
		},
		handlePostTitleClick(post) {
			//console.log('Post title clicked:', post);
			this.currentPost = post;
			// 这里可以添加点击标题后的逻辑处理
			this.lists = false;
			this.content = true;
			this.paperid = post.id;

			this.title = post.title;
			this.paperData = [{ paperUsername: post.username, paperContent: post.content, role: post.role, time: post.time, imageUrl: post.imageUrl }];

			this.comments = [];
			this.tableData = [];
			this.totalComments1 = 0;

			axios.post('/api/paper_content', { 'paper_id': post.id, 'section': 'news', 'user_id': this.userid }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					//console.log(response);
					if (response.data.code == 0) {
						this.comments = response.data.data;
						this.totalComments1 = response.data.data.length;
						if (this.totalComments1 > 0) {
							this.currentScore = response.data.data[0]['sc'];
						}
						this.handleSearch1();
						//console.log('totalComments1=',this.totalComments1);
					} else {
						// ElNotification({
						//   title: '系统提示',
						//   message: response.data.msg,
						//   duration: 3000,
						// })
					}
				})
				.catch(error => {
					// 请求失败，处理错误
					ElNotification({
						title: '系统提示',
						message: '发帖失败',
						duration: 3000,
					})
					console.error('请求数据失败:', error);
				});
		},

		fetchData() {


			axios.post('/api/paper_list', { 'section': 'news', 'keyword': this.keyword }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					//console.log(response);
					if (response.data.code == 0) {
						this.posts = response.data.data;
						this.handleSearch();
						//console.log(response);
					} else {
						ElNotification({
							title: '系统提示',
							message: response.data.msg,
							duration: 3000,
						})
					}
				})
				.catch(error => {
					// 请求失败，处理错误
					ElNotification({
						title: '系统提示',
						message: '发帖失败',
						duration: 3000,
					})
					console.error('请求数据失败:', error);
				});
		},
		handleSearch() {
			// 查询逻辑
			//console.log('查询关键词:', this.keyword);
			// 根据关键词过滤数据并进行分页

			this.filteredData = this.posts.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);

		},
		handleSearch1() {
			// 查询逻辑
			//console.log('查询关键词:', this.keyword);
			// 根据关键词过滤数据并进行分页

			this.tableData = this.comments.slice((this.currentPage1 - 1) * this.pageSize1, this.currentPage1 * this.pageSize1);
			//console.log('tableData==',this.tableData)

		},

		handleForSearch() {
			this.fetchData();
		},

	}
};
</script>

<style scoped>
.left-content {
	flex: 1;
	padding: 20px;
	margin-top: 30px;
	background: #f5f5f5;
	border-radius: 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-list {
	margin-bottom: 10px;
}

.input-with-button {
	display: flex;
	align-items: center;
	margin-bottom: 20px;
	height: 50px;
}

.input {
	margin-right: 10px;
	width: 512px;
	height: 35px;
	font-size: 18px;
}

.custom-table {
	width: 100%;
	background: #fff;
	border-radius: 10px;
	overflow: hidden;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.custom-header {
	font-size: 16px;
	background: #f0f0f0;
	color: #333;
}

.post-title {
	cursor: pointer;
	font-size: 16px;
	font-weight: 600;
	padding: 10px 15px;
	transition: color 0.3s;
}

.post-title:hover {
	color: #005bb5;
}

.role {
	display: inline-block;
	padding: 2px 6px;
	border-radius: 4px;
	color: #fff;
	text-align: center;
	font-size: 14px;
}

.role.admin {
	background-color: #e57373;
}

.role.scientist {
	background-color: #64b5f6;
}

.role.user {
	background-color: #81c784;
}

.pagination {
	text-align: center;
	margin-top: 20px;
}

.forum-detail {
	width: 100%;
	margin-top: 30px;
	padding: 20px;
	border-radius: 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-title-detail {
	font-size: 24px;
	font-weight: 700;
	margin-bottom: 20px;
}

.post-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.back-button {
	background: #DDDDDD;
	color: #333;
	border: none;
	padding: 10px 20px;
	cursor: pointer;
	transition: background 0.3s, color 0.3s;
	margin: 25px;
}

.back-button:hover {
	background: #62a9ff;
	color: #fff;
}

.custom-table-detail {
	width: 100%;
	background: #fff;
	border-radius: 10px;
	overflow: hidden;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-user {
	text-align: center;
	padding: 20px;
}

.avatar {
	width: 90px;
	height: 90px;
	border-radius: 50%;
}

.post-content-detail {
	padding: 20px;
	font-size: 16px;
	color: #333;
	line-height: 1.6;
	background: #f9f9f9;
	border-radius: 10px;
	margin-bottom: 20px;
}

.post-meta {
	display: flex;
	justify-content: space-between;
	color: darkgray;
	margin-top: 10px;
}

.post-actions {
	display: flex;
	justify-content: space-between;
	align-items: center;
	color: darkgray;
	margin-top: 10px;
}

.comment-section-title {
	font-size: 18px;
	font-weight: bold;
	color: #333;
	margin-bottom: 10px;
	margin-top: 30px;
	border-bottom: 2px solid #f0f0f0;
	padding: 15px 10px;
}

.comment-icon {
	color: #000;
	cursor: pointer;
	transition: color 0.3s;
	text-decoration: none;
}

.comment-icon:hover {
	color: #005bb5;
}

.like-icon {
	color: #0073e6;
	cursor: pointer;
	transition: color 0.3s;
}

.like-icon.liked {
	color: #ffb400;
}

.like-count {
	text-align: center;
	color: #333;
	font-weight: 600;
}

.post-time {
	text-align: right;
	color: darkgray;
}

.comment-section {
	margin-top: 20px;
	margin-bottom: 10px;
}

.comment-input {
	margin-bottom: 20px;
}

.submit-button {
	background: #DDDDDD;
	color: #333;
	border: none;
	padding: 10px 15px;
	cursor: pointer;
	transition: background 0.3s, color 0.3s;
	margin_left: 2px;
}

.submit-button:hover {
	background: #62a9ff;
	color: #fff;
}

.nested-comments {
	margin-top: 10px;
	padding-left: 20px;
	border-left: 2px solid #f0f0f0;
}

.nested-comment-content {
	margin-left: 30px;
	color: #555;
}

.dialog-footer {
	text-align: center;
	margin-top: 10px;
}

.comment-submit {
	font-size: 18px;
	font-weight: bold;
	color: #333;
	margin-bottom: 10px;
	margin-top: 30px;
	border-bottom: 2px solid #f0f0f0;
	padding: 15px 10px;
}

.give_score {
	font-size: 18px;
	font-weight: bold;
	color: #333;
	border-bottom: 2px solid #f0f0f0;
	padding: 10px 10px;
}

.submit_buttom {
	margin-top: 10px;
	background: #0073e6;
	border-radius: 5px;
	color: #fff;
	padding: 10px 20px;
	cursor: pointer;
	transition: background 0.3s;
}

.submit_button:hover {
	background: #005bb5;
}
</style>
<template>
	<!-- 左侧帖子部分 -->
	<div class="left-content" v-if="lists">
		<div class="post-list">
			<!-- 查询输入框 -->
			<div class="input-with-button">
				<el-input v-model="keyword" placeholder="请输入生物名称" class="input"></el-input>
				<el-button type="primary" @click="handleForSearch" class="input_button">查询</el-button>
			</div>
			<div class="input-with-button">
				<el-select v-model="selectedSpecies" placeholder="选择生物名称" class="input" @change="fetchYears">
					<el-option v-for="item in speciesOptions" :key="item.name" :label="item.name"
						:value="item.name"></el-option>
				</el-select>
				<el-select v-model="selectedYear" placeholder="选择年份" class="input">
					<el-option v-for="year in yearOptions" :key="year.date_year" :label="year.date_year"
						:value="year.date_year"></el-option>
				</el-select>
				<el-button type="primary" @click="handleForFilter" class="input_button">筛选</el-button>
				<el-button type="primary" @click="toggleMap" class="input_button">{{ showMap ? '关闭可视化' : '可视化'
				}}</el-button>
			</div>

			<div class="forum-table">
				<el-table :data="filteredData" class="custom-table" header-cell-class-name="custom-header">
					<el-table-column prop="name" min-width="5%" label='序号'>
						<template #default="{ row }">
							<span>{{ getIndex(row) }}</span>
						</template>
					</el-table-column>
					<el-table-column prop="name" min-width="15%" label='生物名称'>
						<template #default="{ row }">
							<div @click="handlePostTitleClick(row)" style="cursor: pointer;">{{ row.name }}</div>
						</template>
					</el-table-column>
					<el-table-column prop="originalscientificname" min-width="15%" style="color: darkgrey;" label='原学名'>
						<template #default="{ row }">{{ row.originalscientificname }}</template>
					</el-table-column>
					<el-table-column prop="username" min-width="15%" style="color: darkgrey;" label="族群">
						<template #default="{ row }">{{ row.kingdom }}</template>
					</el-table-column>
					<el-table-column prop="species" min-width="15%" style="color: darkgrey;" label='种类'>
						<template #default="{ row }">{{ row.species }}</template>
					</el-table-column>
					<el-table-column prop="date_year" min-width="7%" style="color: darkgrey;" label='年份'>
						<template #default="{ row }">{{ row.date_year }}</template>
					</el-table-column>
					<el-table-column prop="habitat_region" min-width="15%" style="color: darkgrey;" label="栖息区域">
						<template #default="{ row }">{{ row.habitat_region }}</template>
					</el-table-column>
					<el-table-column prop="decimallongitude" min-width="10%" style="color: darkgrey;" label="经度">
						<template #default="{ row }">{{ row.decimallongitude }}</template>
					</el-table-column>
					<el-table-column prop="decimallatitude" min-width="10%" style="color: darkgrey;" label="纬度">
						<template #default="{ row }">{{ row.decimallatitude }}</template>
					</el-table-column>
				</el-table>
			</div>
		</div>

		<!-- 分页器 -->
		<div class="pagination">
			<el-pagination v-model:currentPage="currentPage" :page-size="pageSize" :total="posts.length"
				layout="prev, pager, next" @current-change="handlePageChange" />
		</div>
		<!-- 地图容器 -->
		<div v-if="showMap" id="container" ref="amap" style="width: 100%; height: 500px; margin-top: 20px;"></div>

	</div>

	<!-- 帖子内容 -->
	<div class="forum-detail" v-if="content">
		<!-- 帖子标题 -->
		<div class="post-header">
			<h1 class="post-title">{{ title }}</h1>
			<el-button type="primary" @click="backto" class="back-button">返回海洋生物列表</el-button>
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
							<div>生物名称：{{ row.paperContent }}</div>
							<div>原学名：{{ row.originalscientificname }}</div>
							<div>族群：{{ row.kingdom }}</div>
							<div>生物种类：{{ row.species }}</div>
							<div>年份：{{ row.date_year }}</div>
							<div>现存数量：{{ row.quantity }}</div>
							<div>栖息区域：{{ row.habitat_region }}</div>
							<div>经度：{{ row.decimallongitude }}</div>
							<div>纬度：{{ row.decimallatitude }}</div>
							<div class="post-meta">
								<div>评分：{{ currentScore }}</div>
								<!-- <div>发布于：{{ row.time }}</div> -->
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
											<div>发表于：{{ row.ctime }}</div>
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
								<div v-if="row.likes == null" class="like-count">点赞数: 0</div>
								<div v-if="row.likes != null" class="like-count">点赞数: {{ row.likes }}</div>
								<div class="post-time">发表于：{{ row.comment_time }}</div>
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
		<div class="comment-submit">发表评论：</div>
		<el-input v-model="newComment" type="textarea" :rows="5" placeholder="请输入评论内容" class="comment-input"></el-input>
		<h5 class="comment-score">评分：</h5>
		<el-rate class="five_star" v-model="score" :max="5" show-text allow-half @change="handleScoreChange"></el-rate>
		<el-button type="primary" @click="submitComment" class="submit-button">发 表</el-button>
	</div>

	<el-dialog :visible.sync="dialogVisible" v-model="dialogVisible" title=" 评 论 " width="45%" center
		:close-on-click-modal="false">
		<el-input v-model="sendNewComment" type="textarea" :rows="3" placeholder="请输入评论内容" class="comment-input"></el-input>

		<div slot="footer" class="dialog-footer">
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
import AMapLoader from '@amap/amap-jsapi-loader';
window._AMapSecurityConfig = {
	// 设置安全密钥
	securityJsCode: "0286edbd4d140235c3560417b0be5957",
};

export default {
	comments: {
		// adminpng,
		// researcherpng,
		// userpng,
	},
	name: "Class",
	data() {
		return {
			selectedSpecies: '',
			selectedYear: '',
			speciesOptions: [],
			yearOptions: [],
			baseUrl: baseUrl,
			showMap: false,
			map: null,
			mapPoints: [], // 存储地图标记点

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
		this.fetchSpecies();
		this.fetchData();
	},
	methods: {
		toggleMap() {
			this.showMap = !this.showMap;
			if (this.showMap) {
				this.$nextTick(() => {
					this.initAMap();
				});
			}
		},
		initAMap() {
			AMapLoader.load({
				key: 'f5bd69297852a95d27f8afaa40b55c44',
				version: '2.0', // 指定要加载的 JSAPI 的版本
				plugins: ['AMap.Geocoder'] // 需要使用的的插件列表
			})
				.then((AMap) => {
					this.map = new AMap.Map(this.$refs.amap, {
						zoom: 5, // 初始化地图级别
						center: [116.397428, 39.90923],// 初始化地图位置，可根据需要调整
						mapStyle: 'amap://styles/08539321a17cd7c322f76950f2c68b3f'
					});
					// 添加初始的标记点
					this.addMarkersToMap();
				})
				.catch(e => {
					console.log(e);
				});
		},
		addMarkersToMap() {
			if (!this.map) return;
			// 清除地图上所有的覆盖物
			this.map.clearMap();
			// 添加新的标记点
			this.filteredData.forEach(point => {
				new AMap.Marker({
					position: [point.decimallongitude, point.decimallatitude],
					map: this.map,
					title: point.name
				});
			});
		},

		handleForFilter() {
			this.fetchFilteredData();
		},

		fetchFilteredData() {
			axios.post('/api/filter_marine_life', {
				species: this.selectedSpecies,
				year: this.selectedYear,
			}, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					if (response.data.code === 0) {
						this.posts = response.data.data;
						this.handleSearch();
						if (this.showMap) {
							this.addMarkersToMap(); // 更新地图标记
						}
					} else {
						ElNotification({
							title: '系统提示',
							message: response.data.msg,
							duration: 3000,
						});
					}
				})
				.catch(error => {
					ElNotification({
						title: '系统提示',
						message: '请求失败',
						duration: 3000,
					});
					console.error('请求数据失败:', error);
				});
		},

		clickLike(row) {
			if (this.userid == '' || this.userid == null) {
				ElNotification({
					title: '系统提示',
					message: '请先登录后再点赞',
					duration: 3000,
				})
				return;
			} else {
				axios.post('/api/clickLike', { 'comment_id': row.id, 'section': 'marine-life', 'user_id': this.userid }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
				axios.post('/api/clickLikeCancel', { 'comment_id': row.id, 'section': 'marine-life', 'user_id': this.userid }, { headers: { "Access-Control-Allow-Origin": "*" } })
					.then(response => {
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
					axios.post('/api/add_comment', { 'paper_id': this.commentId, 'user_id': this.userid, 'section': 'marine-life_new', 'newComment': this.sendNewComment }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
		getIndex(row) {
			// 获取行的索引并返回序号
			return this.posts.indexOf(row) + 1;
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
					axios.post('/api/add_comment', { 'paper_id': this.paperid, 'user_id': this.userid, 'section': 'marine-life', 'newComment': this.newComment, 'score': this.score }, { headers: { "Access-Control-Allow-Origin": "*" } })
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

			this.title = post.name;
			this.paperData = [{
				paperUsername: post.username, paperContent: post.name, species: post.species, habitat_region: post.habitat_region,
				quantity: post.quantity, role: post.role, time: post.time, originalscientificname: post.originalscientificname,
				kingdom: post.kingdom, date_year: post.date_year, decimallongitude: post.decimallongitude, decimallatitude: post.decimallatitude
				, imageUrl: post.imageUrl
			}];

			this.comments = [];
			this.tableData = [];
			this.totalComments1 = 0;

			// <div>原学名：{{row.originalscientificname}}</div>
			// <div>族群：{{row.kingdom}}</div>
			// <div>年份：{{row.date_year}}</div>
			// <div>经度：{{row.decimallongitude}}</div>
			// <div>纬度：{{row.decimallatitude}}</div>

			axios.post('/api/paper_content', { 'paper_id': post.id, 'section': 'marine-life', 'user_id': this.userid }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
						message: '请求失败',
						duration: 3000,
					})
					console.error('请求数据失败:', error);
				});
		},

		fetchData() {
			axios.post('/api/paper_list', { 'section': 'marine-life', 'keyword': this.keyword }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					console.log(response);
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
						message: '请求失败',
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
			if (this.showMap) {
				this.addMarkersToMap(); // 更新地图标记
			}
		},
		handleSearch1() {
			// 查询逻辑
			//console.log('查询关键词:', this.keyword);
			// 根据关键词过滤数据并进行分页

			this.tableData = this.comments.slice((this.currentPage1 - 1) * this.pageSize1, this.currentPage1 * this.pageSize1);
			//console.log('tableData==',this.tableData)

		},

		handleSearch2() {
			// 查询逻辑
			this.filteredData = this.posts; // 不进行分页，显示所有数据
			if (this.showMap) {
				this.addMarkersToMap(); // 更新地图标记
			}
		},

		handleForSearch() {
			this.fetchData();
		},

		fetchSpecies() {
			axios.post('/api/life_list', {
				selectType: 'species'
			}).then(response => {
				if (response.data.code === 0) {
					this.speciesOptions = response.data.data;
				} else {
					ElNotification({
						title: '系统提示',
						message: response.data.msg,
						duration: 3000,
					});
				}
			}).catch(error => {
				ElNotification({
					title: '系统提示',
					message: '请求失败',
					duration: 3000,
				});
				console.error('请求数据失败:', error);
			});
		},
		fetchYears() {
			axios.post('/api/life_selectedOption', {
				selectType: 'species',
				selectedOption: this.selectedSpecies
			}).then(response => {
				if (response.data.code === 0) {
					this.yearOptions = response.data.data;
				} else {
					ElNotification({
						title: '系统提示',
						message: response.data.msg,
						duration: 3000,
					});
				}
			}).catch(error => {
				ElNotification({
					title: '系统提示',
					message: '请求失败',
					duration: 3000,
				});
				console.error('请求数据失败:', error);
			});
		},
		// handleForFilter() {
		// 	this.fetchFilteredData();
		// },
		// fetchFilteredData() {
		// 	axios.post('/api/filter_marine_life', {
		// 		species: this.selectedSpecies,
		// 		year: this.selectedYear,
		// 	}, { headers: { "Access-Control-Allow-Origin": "*" } })
		// 		.then(response => {
		// 			if (response.data.code === 0) {
		// 				this.posts = response.data.data;
		// 				this.handleSearch();
		// 				if (this.showMap) {
		// 					this.addMarkersToMap(); // 更新地图标记
		// 				}
		// 			} else {
		// 				ElNotification({
		// 					title: '系统提示',
		// 					message: response.data.msg,
		// 					duration: 3000,
		// 				});
		// 			}
		// 		})
		// 		.catch(error => {
		// 			ElNotification({
		// 				title: '系统提示',
		// 				message: '请求失败',
		// 				duration: 3000,
		// 			});
		// 			console.error('请求数据失败:', error);
		// 		});
		// },

	},
	// handleForFilter() {
	// 	this.fetchFilteredData();
	// },
	// fetchFilteredData() {
	// 	axios.post('/api/filter_marine_life', {
	// 		species: this.selectedSpecies,
	// 		year: this.selectedYear,
	// 	}, { headers: { "Access-Control-Allow-Origin": "*" } })
	// 		.then(response => {
	// 			if (response.data.code === 0) {
	// 				this.posts = response.data.data;
	// 				this.handleSearch();
	// 				this.updateMapPoints();
	// 				if (this.showMap) {
	// 										this.addMarkersToMap(); // 更新地图标记
	// 									}
	// 			} else {
	// 				this.$notify({
	// 					title: '系统提示',
	// 					message: response.data.msg,
	// 					duration: 3000,
	// 				});
	// 			}
	// 		})
	// 		.catch(error => {
	// 			this.$notify({
	// 				title: '系统提示',
	// 				message: '请求失败',
	// 				duration: 3000,
	// 			});
	// 			console.error('请求数据失败:', error);
	// 		});
	// },
	updateMapPoints() {
		this.mapPoints = this.posts.map(post => ({
			id: post.id,
			lng: post.decimallongitude,
			lat: post.decimallatitude
		}));
		// 更新地图上的标记点
		this.addMarkersToMap();
	},
};
</script>

<style scoped>
#container {
	padding: 0px;
	margin: 0px;
	width: 1000px;
	height: 1000px;
	/* 可根据需要调整高度 */
}

.left-content {
	flex: 1;
	padding: 20px;
	margin-top: 30px;
	background: #f5f5f5;
	border-radius: 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
	/* padding: 20px; */
	border-radius: 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
	margin-left: 10px;
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

.comment-score {
	border-bottom: 2px solid #f0f0f0;
	padding: 15px 10px;
}

.five_star {
	border-bottom: 2px solid #f0f0f0;
	padding: 15px 10px;
}
</style>
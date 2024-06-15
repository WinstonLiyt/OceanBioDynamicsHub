<template>
	<div class="container">
		<div style="margin-bottom: 15px;margin-top: -10px;font-size: 20px;">
			<p>帖子列表</p>
		</div>
		<!-- 查询和新增按钮 -->
		<div class="search-bar">
			<el-input v-model="keyword" placeholder="帖子内容" style="width: 300px;margin-right: 10px;"></el-input>
			<el-select v-model="section" placeholder="请选择板块" style="width: 200px;margin-right: 20px;">
				<!-- <el-option label="普通帖子" value="general"></el-option> -->
				<!-- <el-option label="海洋区域" value="ocean"></el-option>
		  <el-option label="海洋生物" value="marine-life"></el-option> -->
				<el-option label="海洋信息" value="info"></el-option>
				<el-option label="海洋新闻" value="news"></el-option>
			</el-select>
			<el-button type="primary" @click="fetchData">查&nbsp;询</el-button>
			<!-- <el-button type="primary" @click="showAddDialog">新&nbsp;增</el-button> -->
		</div>

		<div class="forum-table" style="min-height: 300px;">
			<!-- 表格 -->
			<el-table :data="filteredData" style="width: 100%">
				<el-table-column label="序号" align="center" min-width="5%">
					<template #default="{ row }">
						<span>{{ getIndex(row) }}</span>
					</template>
				</el-table-column>
				<el-table-column prop="title" label="帖子标题" min-width="65%"></el-table-column>
				<el-table-column prop="time" label="发布时间" min-width="15%"></el-table-column>

				<el-table-column label="操作" min-width="15%">
					<template #default="{ row }">
						<div v-if='row.status == 1'>
							<el-button type="text" @click="handlechange(row)">查看</el-button>
							<el-button type="text" @click="handleDelete(row)">禁用</el-button>
						</div>
						<div v-if='row.status == 2'>
							<el-button type="text" @click="handledo(row)">解禁</el-button>
						</div>

					</template>
				</el-table-column>
			</el-table>
		</div>

		<!-- 分页 -->
		<el-pagination v-model:currentPage="currentPage" :total="total" :page-size="pageSize"
			@current-change="handlePageChange" layout="total, prev, pager, next, jumper" style="margin-top: 20px;">
		</el-pagination>

		<!-- 新增对话框 -->
		<el-dialog title=" 帖 子 内 容 " v-model="addDialogVisible" :close-on-click-modal="false" :close-on-press-escape="false"
			:modal="false" width="700px" center :showClose="false">

			<h3 class="post-title">标题：{{ title }}</h3>
			<div style="min-height: 200px;">
				内容：<div v-html="content"></div>
			</div>

			<!-- 操作按钮 -->
			<div class="dialog-footer" style="text-align: right;margin-top: 10px;">
				<el-button @click="addDialogVisible = false">返回</el-button>
				<!-- <el-button type="primary" @click="sendMessage">发送</el-button> -->
			</div>
		</el-dialog>


	</div>
</template>

<script>
import axios from '@/api/index.js'
import { ElMessageBox, ElNotification } from 'element-plus'
export default {
	data() {
		return {
			id: localStorage.getItem('id'),
			section: 'info',
			//role:localStorage.getItem('role'),
			keyword: '', // 查询关键词
			tableData: [], // 表格数据
			filteredData: [], // 过滤后的数据列表
			currentPage: 1, // 当前页码
			total: 0, // 数据总数
			pageSize: 10, // 每页显示条数
			addDialogVisible: false, // 新增对话框是否显示
			dialogVisible: false,
			rowid: 0,
			title: '',
			content: '',
		};
	},
	created() {
		this.fetchData();
	},
	beforeDestroy() {

	},
	methods: {
		handledo(row) {
			axios.post('/api/forum_disable', { 'id': row.id, 'section': this.section, 'status': 1 }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					// console.log(response);
					// 请求成功，将数据绑定到表格中
					ElNotification({
						title: '系统提示',
						message: response.data.msg,
						duration: 3000,
					});
					this.fetchData();
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
		fetchData() {
			axios.post('/api/forum_list', { 'keyword': this.keyword, 'section': this.section }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					if (response.data.code == 0) {
						this.tableData = [];
						console.log(response);
						// 请求成功，将数据绑定到表格中
						this.tableData = response.data.data;
						this.total = this.tableData.length;
						this.handleSearch();
					} else {
						this.tableData = [];
						this.total = 0;
						this.handleSearch();
					}
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
		handleSearch() {
			// 查询逻辑
			console.log('查询关键词:', this.keyword);
			// 根据关键词过滤数据并进行分页
			this.filteredData = this.tableData.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);
		},
		handlePageChange(page) {
			// 分页逻辑
			console.log('当前页码:', page);
			this.currentPage = page;
			this.handleSearch();
		},
		getIndex(row) {
			// 获取行的索引并返回序号
			return this.tableData.indexOf(row) + 1;
		},
		handlechange(row) {
			this.addDialogVisible = true;
			this.title = row.title;
			this.content = row.content;
			console.log('content=', this.content)
		},
		handleDelete(row) {
			axios.post('/api/forum_disable', { 'id': row.id, 'section': this.section, 'status': 2 }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					// console.log(response);
					// 请求成功，将数据绑定到表格中
					ElNotification({
						title: '系统提示',
						message: response.data.msg,
						duration: 3000,
					});
					this.fetchData();
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		}
	}
};

</script>

<style></style>
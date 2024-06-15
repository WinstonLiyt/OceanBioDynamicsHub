<template>
	<div class="container">
		<div style="margin-bottom: 15px;margin-top: -10px;font-size: 20px;">
			<p>用户列表</p>
		</div>
		<!-- 查询和新增按钮 -->
		<div class="search-bar">
			<el-input v-model="keyword" placeholder="用户名字" style="width: 200px;margin-right: 20px;"></el-input>
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
				<el-table-column prop="username" label="用户名" min-width="20%"></el-table-column>
				<el-table-column prop="full_name" label="姓名" min-width="15%"></el-table-column>
				<el-table-column prop="phone_number" label="手机号" min-width="15%"></el-table-column>

				<!-- <el-table-column v-if='row.role==2' label="角色">科学家</el-table-column>
			<el-table-column v-if='row.role==3' label="角色">普通用户</el-table-column> -->

				<el-table-column label="角色" min-width="10%">
					<template #default="{ row }">
						<span v-if='row.role == 2' type="text">科学家</span>
						<span v-if='row.role == 3' type="text">普通用户</span>
					</template>
				</el-table-column>

				<el-table-column label="操作" min-width="15%">
					<template #default="{ row }">

						<div v-if='row.status == 1'>
							<el-button v-if='row.role == 2' type="text" @click="handledown(row)">降为用户</el-button>
							<el-button v-if='row.role == 3' type="text" @click="handlechange(row)">升级科学家</el-button>
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
		<el-dialog title="讨  论  区" v-model="addDialogVisible" :close-on-click-modal="false" :close-on-press-escape="false"
			:modal="false" width="700px" center :showClose="false">

			<!-- 聊天内容显示区 -->
			<div class="chat-content" ref="chatContent" height=600px width=650px;
				style="border: 1px solid skyblue;min-height: 600px;margin-bottom: 10px;border-radius: 4px;">
				<div v-for="(message, index) in chatMessages" :key="index" class="message">{{ message }}

				</div>
			</div>

			<!-- 输入框 -->
			<el-input v-model="inputMessage" placeholder="请输入消息" class="input-message"></el-input>


			<!-- 操作按钮 -->
			<div class="dialog-footer" style="text-align: right;margin-top: 10px;">
				<el-button @click="backto">返回</el-button>
				<el-button type="primary" @click="sendMessage">发送</el-button>
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
			//role:localStorage.getItem('role'),
			keyword: '', // 查询关键词
			tableData: [], // 表格数据
			filteredData: [], // 过滤后的数据列表
			currentPage: 1, // 当前页码
			total: 0, // 数据总数
			pageSize: 10, // 每页显示条数
			addDialogVisible: false, // 新增对话框是否显示
			dialogVisible: false,
			inputMessage: '', // 输入框中的消息
			chatMessages: [], // 聊天消息列表
			timer: '',
			rowid: 0,
		};
	},
	created() {
		this.fetchData();
	},
	beforeDestroy() {

	},
	methods: {
		handledo(row) {
			axios.post('/api/user_disable', { 'id': row.id, 'status': 1 }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
			axios.post('/api/user_list', { 'keyword': this.keyword }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					console.log(response);
					if (response.data.code == 0) {
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
			axios.post('/api/user_change', { 'id': row.id }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					//console.log(response);
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
		handledown(row) {
			axios.post('/api/user_change_down', { 'id': row.id }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					//console.log(response);
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
		backto() {
			clearInterval(this.timer);
			this.addDialogVisible = false;
		},

		handleDelete(row) {
			axios.post('/api/user_disable', { 'id': row.id, 'status': 2 }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
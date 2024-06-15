<template>
	<div class="container">
		<div style="margin-bottom: 15px;margin-top: -10px;font-size: 20px;">
			<p>海洋生物列表</p>
		</div>
		<!-- 查询和新增按钮 -->
		<div class="search-bar">
			<el-input v-model="keyword" placeholder="动物名称" style="width: 300px;margin-right: 10px;"></el-input>
			<!-- <el-select v-model="section" placeholder="请选择板块"  style="width: 200px;margin-right: 20px;">
		  <el-option label="普通帖子" value="general"></el-option>
		  <el-option label="海洋区域" value="ocean"></el-option>
		  <el-option label="海洋生物" value="marine-life"></el-option>
		  <el-option label="海洋信息" value="info"></el-option>
		  <el-option label="海洋新闻" value="news"></el-option>
		</el-select> -->
			<el-button type="primary" @click="fetchData">查&nbsp;询</el-button>
			<el-button type="primary" @click="dialogVisible = true">新&nbsp;增</el-button>
		</div>

		<div class="forum-table" style="min-height: 300px;">
			<!-- 表格 -->
			<el-table :data="filteredData" style="width: 100%">
				<el-table-column label="序号" align="center" min-width="5%">
					<template #default="{ row }">
						<span>{{ getIndex(row) }}</span>
					</template>
				</el-table-column>
				<el-table-column prop="name" label="生物名称" min-width="15%"></el-table-column>
				<el-table-column prop="originalscientificname" label="原学名" min-width="15%"></el-table-column>
				<el-table-column prop="kingdom" label="族群" min-width="15%"></el-table-column>
				<el-table-column prop="species" label="生物种类" min-width="15%"></el-table-column>
				<el-table-column prop="date_year" label="年份" min-width="5%"></el-table-column>
				<el-table-column prop="quantity" label="数量" min-width="5%"></el-table-column>
				<el-table-column prop="habitat_region" label="栖息区域" min-width="15%"></el-table-column>
				<el-table-column prop="decimallongitude" label="经度" min-width="10%"></el-table-column>
				<el-table-column prop="decimallatitude" label="纬度" min-width="10%"></el-table-column>
				<el-table-column prop="time" label="发布时间" min-width="15%"></el-table-column>

				<el-table-column label="操作" min-width="15%">
					<template #default="{ row }">
						<el-button type="text" @click="handlechange(row)">修改</el-button>
						<el-button type="text" @click="handleDelete(row)">禁用</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>

		<!-- 分页 -->
		<el-pagination v-model:currentPage="currentPage" :total="total" :page-size="pageSize"
			@current-change="handlePageChange" layout="total, prev, pager, next, jumper" style="margin-top: 20px;">
		</el-pagination>

		<!-- 修改 -->
		<el-dialog title="帖子内容" v-model="addDialogVisible" :close-on-click-modal="false" :close-on-press-escape="false"
			:modal="false" width="700px" center :showClose="false">
			<div class="forum-table" style="min-height: 300px;margin-top:5px;">
				<el-form :model="formData" ref="form" label-width="100px" class="form">

					<el-form-item label="生物名称" prop="name">
						<el-input type="text" v-model="formData.name"></el-input>
					</el-form-item>
					<el-form-item label="原学名" prop="originalscientificname">
						<el-input type="text" v-model="formData.originalscientificname"></el-input>
					</el-form-item>
					<el-form-item label="族群" prop="kingdom">
						<el-input type="text" v-model="formData.kingdom"></el-input>
					</el-form-item>
					<el-form-item label="生物种类" prop="species">
						<el-input type="text" v-model="formData.species"></el-input>
					</el-form-item>
					<el-form-item label="年份" prop="date_year">
						<el-input type="text" v-model="formData.date_year"></el-input>
					</el-form-item>
					<el-form-item label="现存数量" prop="quantity">
						<el-input type="text" v-model="formData.quantity"></el-input>
					</el-form-item>
					<el-form-item label="栖息区域" prop="habitat_region">
						<el-input type="text" v-model="formData.habitat_region"></el-input>
					</el-form-item>
					<el-form-item label="经度" prop="decimallongitude">
						<el-input type="text" v-model="formData.decimallongitude"></el-input>
					</el-form-item>
					<el-form-item label="纬度" prop="decimallatitude">
						<el-input type="text" v-model="formData.decimallatitude"></el-input>
					</el-form-item>

				</el-form>
			</div>

			<!-- 操作按钮 -->
			<div class="dialog-footer" style="text-align: right;margin-top: 10px;">
				<el-button type="primary" @click="addDialogVisible = false">返回</el-button>
				<el-button type="primary" @click="update">保存</el-button>
			</div>
		</el-dialog>

		<!-- 新增-->
		<el-dialog title="新增海洋生物帖子" v-model="dialogVisible" :close-on-click-modal="false" :close-on-press-escape="false"
			:modal="false" width="700px" center :showClose="false">
			<div class="forum-table" style="min-height: 300px;margin-top:5px;">
				<el-form :model="formData1" ref="form1" label-width="100px" class="form">

					<el-form-item label="生物名称" prop="name">
						<el-input type="text" v-model="formData1.name"></el-input>
					</el-form-item>
					<el-form-item label="原学名" prop="originalscientificname">
						<el-input type="text" v-model="formData1.originalscientificname"></el-input>
					</el-form-item>
					<el-form-item label="族群" prop="kingdom">
						<el-input type="text" v-model="formData1.kingdom"></el-input>
					</el-form-item>
					<el-form-item label="生物种类" prop="species">
						<el-input type="text" v-model="formData1.species"></el-input>
					</el-form-item>
					<el-form-item label="年份" prop="date_year">
						<el-input type="text" v-model="formData1.date_year"></el-input>
					</el-form-item>
					<el-form-item label="现存数量" prop="quantity">
						<el-input type="text" v-model="formData1.quantity"></el-input>
					</el-form-item>
					<el-form-item label="栖息区域" prop="habitat_region">
						<el-input type="text" v-model="formData1.habitat_region"></el-input>
					</el-form-item>
					<el-form-item label="经度" prop="decimallongitude">
						<el-input type="text" v-model="formData1.decimallongitude"></el-input>
					</el-form-item>
					<el-form-item label="纬度" prop="decimallatitude">
						<el-input type="text" v-model="formData1.decimallatitude"></el-input>
					</el-form-item>

				</el-form>
			</div>

			<!-- 操作按钮 -->
			<div class="dialog-footer" style="text-align: right;margin-top: 10px;">
				<el-button type="primary" @click="dialogVisible = false">返回</el-button>
				<el-button type="primary" @click="save">保存</el-button>
			</div>
		</el-dialog>


	</div>
</template>

<script>
import axios from '@/api/index.js';
import { ElMessageBox, ElNotification } from 'element-plus';

export default {
	data() {
		return {
			id: localStorage.getItem('id'),
			//section:'general',
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
			formData: {
				rowid: 0,
				name: '',
				species: '',
				habitat_region: '',
				quantity: 0,
				originalscientificname: '',
				kingdom: '',
				date_year: 0,
				decimallongitude: '',
				decimallatitude: '',
				section: 'marine-life',
			},
			formData1: {
				id: localStorage.getItem('id'),
				name: '',
				species: '',
				habitat_region: '',
				quantity: 0,
				originalscientificname: '',
				kingdom: '',
				date_year: 0,
				decimallongitude: '',
				decimallatitude: '',
				section: 'marine-life',
			}
		};
	},
	created() {
		this.fetchData();
	},
	methods: {
		save() {
			if (!/^[0-9]*$/.test(this.formData1.quantity)) {
				ElNotification({
					title: '系统提示',
					message: '现存数量必须为数字',
					duration: 3000,
				});
				return;
			}

			if (this.formData1.name == '' || this.formData1.species == '' || this.formData1.habitat_region == '' || this.formData1.quantity == '') {
				ElNotification({
					title: '系统提示',
					message: '不能为空~',
					duration: 3000,
				});
				return;
			}
			axios.post('/api/forum_add', this.formData1, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					//if(response.data.code==0){
					ElNotification({
						title: '系统提示',
						message: response.data.msg,
						duration: 3000,
					});
					this.dialogVisible = false;
					this.fetchData();
					//}
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
		//修改帖子
		update() {
			if (this.formData.name == '' || this.formData.species == '' || this.formData.habitat_region == '' || this.formData.quantity == '') {
				ElNotification({
					title: '系统提示',
					message: '不能为空~',
					duration: 3000,
				});
				return;
			}

			axios.post('/api/forum_change', this.formData, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					this.tableData = [],
						console.log(response);
					// 请求成功，将数据绑定到表格中
					this.addDialogVisible = false;
					this.fetchData();
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},

		fetchData() {
			axios.post('/api/forum_list', { 'keyword': this.keyword, 'section': 'marine-life' }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
					// }else{
					// 	this.tableData=[];
					// }
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
			this.formData.rowid = row.id;
			this.formData.name = row.name;
			this.formData.species = row.species;
			this.formData.habitat_region = row.habitat_region;
			this.formData.quantity = row.quantity;
			this.formData.originalscientificname = row.originalscientificname;
			this.formData.kingdom = row.kingdom;
			this.formData.date_year = row.date_year;
			this.formData.decimallongitude = row.decimallongitude;
			this.formData.decimallatitude = row.decimallatitude;

		},
		handleDelete(row) {
			axios.post('/api/forum_disable', { 'id': row.id, 'section': 'marine-life' }, { headers: { "Access-Control-Allow-Origin": "*" } })
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
<template>
	<div class="about">
		<h1>This is an about page</h1>
	</div>
</template>
<script>
import { ref } from 'vue';
import axios from '@/api/index.js'
import { ElMessageBox, ElNotification } from 'element-plus'
export default {
	data() {
		return {

		}
	},
	created() {
		this.fetchData();
	},
	methods: {
		fetchData() {
			axios.get('/api/student/studentClass?id=' + this.id, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					console.log(response);
					// 请求成功，将数据绑定到表格中
					this.tableData = response.data.data;
					this.total = this.tableData.length;
					this.handleSearch();
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
	},
}	
</script>
<style></style>
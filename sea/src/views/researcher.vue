<template>
	<div class="container">
		<el-select v-model="selectedType" placeholder="请选择类型" @change="handleChange" style="width:50%;margin:10px 10px;">
			<el-option v-for="st in stype" :key="st.types" :label="st.vals" :value="st.types"></el-option>
		</el-select>
		<!-- 选择框 -->
		<el-select v-model="selectedOption" placeholder="请选择类目" @change="handleChange1" style="width:50%;margin:10px 10px;">
			<el-option v-for="item in options" :key="item.name" :label="item.name" :value="item.name"></el-option>
		</el-select>
		<!-- 起始年份选择框 -->
		<el-select v-model="startYear" placeholder="请选择起始年份" style="width:50%;margin:10px 10px;">
			<el-option v-for="year in years" :key="year.date_year" :label="year.date_year"
				:value="year.date_year"></el-option>
		</el-select>
		<!-- 结束年份选择框 -->
		<!-- <el-select v-model="endYear" placeholder="请选择结束年份" style="width:50%;margin:10px 10px;">
        <el-option
          v-for="year in years"
          :key="year"
          :label="year"
          :value="year"
        ></el-option>
      </el-select> -->
		<!-- 预测年份输入框 -->
		<el-input v-model="predictYear" placeholder="需要预测的年份,输入数字即可,比如10代表10年"
			style="width:50%;margin:10px 10px;"></el-input>
		<!-- 预测按钮 -->
		<el-button type="primary" @click="handlePredict" style="width:50%;margin:10px 10px;">预 测</el-button>
	</div>

	<div v-if='show' class='container'>
		<p>复制输入框里边的内容到编辑器中即可</p>
		<el-input v-model="url" style="width:50%;margin:10px 10px;"></el-input>
		<div class="image-container">
			<img :src="img_url" alt="加载的图片">
		</div>
	</div>

	<el-dialog :width="300" v-model="dialogVisible" title=" 提 示 " style="text-align: center;">
		<span>预测数据生成中...</span>
	</el-dialog>
</template>

<script>
import axios from '@/api/index.js'
import { ElMessageBox, ElNotification, ElLoading } from 'element-plus'

//import { ref, reactive, watch } from 'vue';
//import { getOptionsFromBackend } from '@/api'; // 假设这里是从后台获取数据的函数

export default {
	data() {
		return {
			dialogVisible: false,
			show: false,
			url: '',
			img_url: '',
			showmsg: '',
			options: [], // 存储选项的数组
			selectedOption: null, // 存储当前选中的选项 
			startYear: null, // 起始年份
			//endYear: null, // 结束年份
			predictYear: null, // 预测年份
			years: [], // 年份数组
			selectedType: null,
			stype: [{ types: 'kingdom', vals: 'kingdom-族群' }, { types: 'habitat_region', vals: 'habitat_region-栖息区域' },
			{ types: 'species', vals: 'species-种类' }, { types: 'originalscientificname', vals: 'originalscientificname-学名' }],
			// loading : Loading.service({
			//       text: '预测数据生成中...',
			//       spinner:'el-icon-upload',// 可用elment-ui中图标样式
			//       custom-class:"upload-class",// 自定义类名，添加样式
			//       target:"document.querySelector('el-dialog')" // 遮罩层作用的目标节点
			//     }),
			//width:{default:20%}
		};
	},
	created() {
		//this.fetchData(); // 初始化时获取数据
		//this.initYears(); // 初始化年份数组
	},
	methods: {
		// 获取数据
		fetchData() {
			axios.post('/api/life_list', { 'selectType': this.selectedType }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					console.log(response);
					if (response.data.code == 0) {
						this.options = [];
						// 请求成功，将数据绑定到表格中
						this.options = response.data.data;
						//this.total=this.tableData.length;
						//this.handleSearch();
					} else {
						// this.tableData=[];
						// this.total=0;
						// this.handleSearch();
					}
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
		fetchData1() {
			axios.post('/api/life_selectedOption', { 'selectType': this.selectedType, 'selectedOption': this.selectedOption }, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					console.log(response);
					if (response.data.code == 0) {
						this.years = [];
						// 请求成功，将数据绑定到表格中
						this.years = response.data.data;
						//this.total=this.tableData.length;
						//this.handleSearch();
					} else {
						// this.tableData=[];
						// this.total=0;
						// this.handleSearch();
					}
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
		// 初始化年份数组
		// initYears() {
		//   const currentYear = new Date().getFullYear();
		//   for (let year = currentYear - 50; year <= currentYear; year++) {
		//     this.years.push(year);
		//   }
		// },
		// 监听选中选项的变化
		handleChange() {
			if (this.selectedType == null) {
				ElNotification({
					title: '系统提示',
					message: '请选择类型',
					duration: 3000,
				})
				return;
			}
			this.options = [];
			this.years = [];
			this.selectedOption = null;
			this.startYear = null;
			//console.log('Selected option:', this.selectedOption);
			this.fetchData();
		},
		handleChange1() {
			if (this.selectedOption == null) {
				ElNotification({
					title: '系统提示',
					message: '请选择类目',
					duration: 3000,
				})
				return;
			}
			this.years = [];
			this.startYear = null;
			//console.log('Selected option:', this.selectedOption);
			this.fetchData1();
		},
		// 预测按钮点击事件
		handlePredict() {
			// console.log('预测按钮被点击');
			// console.log('起始年份:', this.startYear);
			// //console.log('结束年份:', this.endYear);
			// console.log('预测年份:', this.predictYear);
			// 在这里添加预测逻辑
			if (!/^\d{1,3}$/.test(this.predictYear)) {
				ElNotification({
					title: '系统提示',
					message: '预测年份为1-3位的正整数',
					duration: 3000,
				})
				return;
			} else {
				this.dialogVisible = true;
				axios.post('/api/life_predict',
					{ 'selectType': this.selectedType, 'startYear': this.startYear, 'predictYear': this.predictYear, 'selectedOption': this.selectedOption },
					{ timeout: 1000 * 60 * 2 },
					{ headers: { "Access-Control-Allow-Origin": "*" } })
					.then(response => {
						console.log(response);
						if (response.data.code == 0) {
							// 请求成功，将数据绑定到表格中
							this.show = true;
							this.url = '<img src="' + response.data.data + '"/>';
							this.img_url = response.data.data;
							this.dialogVisible = false;
						} else {
							ElNotification({
								title: '系统提示',
								message: response.data.msg,
								duration: 3000,
							})
							this.dialogVisible = false;
						}
					})
					.catch(error => {
						// 请求失败，处理错误
						console.error('请求数据失败:', error);
						this.dialogVisible = false;
					});
			}
		}
	}
};

</script>

<style scoped>
.container {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	margin-top: 20px;
}

el-select {
	width: 60%;
	margin: 10px 10px;
}
</style>

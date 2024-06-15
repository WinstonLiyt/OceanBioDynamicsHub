<template>
	<div class="post-page">
		<el-form :model="postForm" label-width="80px" class="custom-form">
			<el-form-item label="标题" required>
				<el-input v-model="postForm.title" placeholder="请输入标题" class="input"></el-input>
			</el-form-item>
			<el-form-item label="板块" required>
				<el-select v-model="postForm.section" placeholder="请选择板块" class="select">
					<el-option label="海洋资讯" value="info"></el-option>
					<el-option label="海洋新闻" value="news"></el-option>
				</el-select>
			</el-form-item>

			<el-form-item label="内容" required>
				<QuillEditor ref="myQuill" content-type="html" theme="snow" v-model="postForm.content"
					:options="editorOptions" class="editor"></QuillEditor>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="submitPost" class="submit-button">提交</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
import axios from '@/api/index.js';
import { ElMessageBox, ElNotification } from 'element-plus';
import { QuillEditor, Quill } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';

//  import { ImageDrop } from 'quill-image-drop-module'
//  Quill.register('modules/imageDrop', ImageDrop)

//  import BlotFormatter from 'quill-blot-formatter'
//  Quill.register('modules/blotFormatter', BlotFormatter)

// const modules = {
//   name: 'blotFormatter', // 名称
//   module: BlotFormatter, // 模块
//   options: toolbar //工具栏
// }

// 工具栏配置项
const toolbarOptions = [
	// 加粗 斜体 下划线 删除线 -----['bold', 'italic', 'underline', 'strike']
	['bold', 'italic', 'underline', 'strike'],
	// 引用  代码块-----['blockquote', 'code-block']
	['blockquote', 'code-block'],
	// 1、2 级标题-----[{ header: 1 }, { header: 2 }]
	[{ header: 1 }, { header: 2 }],
	// 有序、无序列表-----[{ list: 'ordered' }, { list: 'bullet' }]
	[{ list: 'ordered' }, { list: 'bullet' }],
	// 上标/下标-----[{ script: 'sub' }, { script: 'super' }]
	[{ script: 'sub' }, { script: 'super' }],
	// 缩进-----[{ indent: '-1' }, { indent: '+1' }]
	[{ indent: '-1' }, { indent: '+1' }],
	// 文本方向-----[{'direction': 'rtl'}]
	[{ direction: 'rtl' }],
	// 字体大小-----[{ size: ['small', false, 'large', 'huge'] }]
	[{ size: ['small', false, 'large', 'huge'] }],
	// 标题-----[{ header: [1, 2, 3, 4, 5, 6, false] }]
	[{ header: [1, 2, 3, 4, 5, 6, false] }],
	// 字体颜色、字体背景颜色-----[{ color: [] }, { background: [] }]
	[{ color: [] }, { background: [] }],
	// 字体种类-----[{ font: [] }]
	[{ font: [] }],
	// 对齐方式-----[{ align: [] }]
	[{ align: [] }],
	// 清除文本格式-----['clean']
	['clean'],
	// 链接、图片、视频-----['link', 'image', 'video']
	['link', 'image'],
	// ['table'] // 表格
]


export default {
	components: {
		QuillEditor
	},
	data() {
		return {
			role: localStorage.getItem('role'),
			postForm: {
				title: '',
				section: '',
				content: '',
				userid: localStorage.getItem('id'),
			},
			editorOptions: {
				placeholder: '请输入内容',
				modules: {
					toolbar: {
						container: toolbarOptions,
						handlers: { 'image': this.imageHandler },
					}
				}
			}
		};
	},
	computed: {
		//console.log('baseUrl=',baseUrl);
		editor() {
			return this.$refs.myQuill.quill
		}
	},
	methods: {
		imageHandler: function () {
			var input = document.createElement('input');
			input.setAttribute('type', 'file');
			input.setAttribute('accept', 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon');
			input.click();
			// 监听上传
			input.onchange = () => {
				var file = input.files[0];
				//console.log('file=',file);
				if (/^image\//.test(file.type)) {
					this.saveImage(file);
				} else {
					ElNotification({
						title: '系统提示',
						message: "只能上传图片哦",
						duration: 3000,
					})
				}
			};
		},
		saveImage: function (file) {
			//console.log('file11=',file);
			var fd = new FormData();
			fd.append('file', file);

			console.log('fd=', fd)
			//let url = '/api/file_upload';
			axios.post('/api/file_upload', fd, { headers: { "Access-Control-Allow-Origin": "*", 'Content-Type': 'multipart/form-data' } })
				.then(response => {
					this.insertImage(response.data.data);
					console.log(response.data.data);
				})
				.catch(error => {
					// 请求失败，处理错误
					console.error('请求数据失败:', error);
				});
		},
		insertImage: function (url) {
			let quill = this.$refs.myQuill.getQuill();
			console.log('quill=', this.$refs.myQuill)
			let length = quill.getSelection().index;
			quill.insertEmbed(length, "image", url);
			quill.setSelection(length + 1);
		},

		submitPost() {
			if (localStorage.getItem('id') == '' || localStorage.getItem('id') == null) {
				ElNotification({
					title: '系统提示',
					message: "请登录再发帖",
					duration: 3000,
				})
				return;
			}
			this.postForm.content = this.$refs.myQuill.getHTML();
			//console.log('postForm.content==',this.postForm.content);
			axios.post('/api/add_papers', this.postForm, { headers: { "Access-Control-Allow-Origin": "*" } })
				.then(response => {
					console.log(response);
					if (response.data.code == 0) {
						ElNotification({
							title: '发帖提示',
							message: response.data.msg,
							duration: 3000,
						})
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
					//console.error('请求数据失败:', error);
				});
		}
	}
};
</script>
<style>
.post-page {
	margin-top: 20px;
	max-width: 1200px;
	/* 	max-height: 200px; */
	padding: 20px;
	background: #fff;
	border-radius: 10px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 自定义font-size */
.ql-snow .ql-picker.ql-size .ql-picker-label::before,
.ql-snow .ql-picker.ql-size .ql-picker-item::before {
	content: "14px";
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="10px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="10px"]::before {
	content: "10px";
	font-size: 10px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="12px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="12px"]::before {
	content: "12px";
	font-size: 12px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="14px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="14px"]::before {
	content: "14px";
	font-size: 14px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="16px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="16px"]::before {
	content: "16px";
	font-size: 16px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="18px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="18px"]::before {
	content: "18px";
	font-size: 18px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="20px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="20px"]::before {
	content: "20px";
	font-size: 20px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="24px"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="24px"]::before {
	content: "24px";
	font-size: 24px;
}

/* 自定义标题 */
.ql-snow .ql-picker.ql-header .ql-picker-label::before,
.ql-snow .ql-picker.ql-header .ql-picker-item::before {
	content: "文本";
}

.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
	content: "标题1";
}

.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
	content: "标题2";
}

.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
	content: "标题3";
}

.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
	content: "标题4";
}

.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
	content: "标题5";
}

.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
	content: "标题6";
}

/* 自定义字体 */
.ql-snow .ql-picker.ql-font .ql-picker-label::before,
.ql-snow .ql-picker.ql-font .ql-picker-item::before {
	content: "微软雅黑";
}

/* .ql-snow .ql-picker.ql-font .ql-picker-label[data-value="serif"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="serif"]::before {
  content: "衬线字体";
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="monospace"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="monospace"]::before {
  content: "等宽字体";
} */
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="SimSun"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="SimSun"]::before {
	content: "宋体";
	font-family: "SimSun";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="SimHei"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="SimHei"]::before {
	content: "黑体";
	font-family: "SimHei";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="Microsoft-YaHei"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="Microsoft-YaHei"]::before {
	content: "微软雅黑";
	font-family: "Microsoft YaHei";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="YouYuan"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="YouYuan"]::before {
	content: "幼圆";
	font-family: "YouYuan";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="KaiTi"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="KaiTi"]::before {
	content: "楷体";
	font-family: "KaiTi";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="FangSong"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="FangSong"]::before {
	content: "仿宋";
	font-family: "FangSong";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="Arial"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="Arial"]::before {
	content: "Arial";
	font-family: "Arial";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="Times-New-Roman"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="Times-New-Roman"]::before {
	content: "Times New Roman";
	font-family: "Times New Roman";
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="sans-serif"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="sans-serif"]::before {
	content: "sans-serif";
	font-family: "sans-serif";
}

.ql-font-SimSun {
	font-family: "SimSun";
}

.ql-font-SimHei {
	font-family: "SimHei";
}

.ql-font-YouYuan {
	font-family: "YouYuan";
}

.ql-font-Microsoft-YaHei {
	font-family: "Microsoft YaHei";
}

.ql-font-KaiTi {
	font-family: "KaiTi";
}

.ql-font-FangSong {
	font-family: "FangSong";
}

.ql-font-Arial {
	font-family: "Arial";
}

.ql-font-Times-New-Roman {
	font-family: "Times New Roman";
}

.ql-font-sans-serif {
	font-family: "sans-serif";
}

.custom-form {
	background: #f7f7f7;
	border-radius: 10px;
	padding: 20px;
}

.el-form-item {
	margin-bottom: 20px;
}

.input,
.select,
.editor {
	width: 100%;
	font-size: 16px;
	/* 	height: 200px; */
}

.submit-button {
	background: #0073e6;
	color: #fff;
	border: none;
	padding: 10px 20px;
	cursor: pointer;
	transition: background 0.3s, color 0.3s;
	border-radius: 5px;
	margin-left: 44.5%;
}

.submit-button:hover {
	background: #005bb5;
	color: #fff;
}

.ql-snow {
	border-radius: 10px;
}

.ql-container {
	border-radius: 10px;
}

.ql-editor {
	min-height: 250px;
	/* 调整为 300px */
}
</style>
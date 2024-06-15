<template>
	<div class="forum-home">
		<!-- 导航菜单 -->
		<el-menu :default-active="activeMenu" mode="horizontal" class="nav-menu" @select="handleMenuSelect">
			<el-menu-item
				style="cursor:default; padding-left:10px; font-size: 20px; font-family: 'art'; opacity: 1; font-weight: bold;"
				disabled>
				<img src="../assets/icon.png" alt="png"
					style="height: 50px; vertical-align: middle; margin-right: 15px; border-radius: 50%; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);">
				海洋生物种群动态预测平台
			</el-menu-item>
			<el-menu-item index="index" style="font-size: 16px; font-family: 'art'">首页</el-menu-item>
			<el-menu-item index="ocean" style="font-size: 16px; font-family: 'art'">海洋区域</el-menu-item>
			<el-menu-item index="marine" style="font-size: 16px; font-family: 'art'">海洋生物</el-menu-item>
			<el-menu-item index="info" style="font-size: 16px; font-family: 'art'">海洋资讯</el-menu-item>
			<el-menu-item index="news" style="font-size: 16px; font-family: 'art'">海洋新闻</el-menu-item>
			<el-menu-item index="papers" style="font-size: 16px; font-family: 'art'">我要发帖</el-menu-item>
			<el-menu-item v-if="role === '2'" index="researcher"
				style="font-size: 16px; font-family: 'art'">科研预测</el-menu-item>
			<el-menu-item v-if="role === '1'" index="admin" style="font-size: 16px; font-family: 'art'">权限管理</el-menu-item>

			<div v-if="id == null" style="float: right; margin-top:13px; display: block; margin-left: 40px;">
				<el-button type="primary" @click="goToRegister" style="margin-right: 15px; font-family: 'art'">注
					册</el-button>
				<el-button type="primary" @click="goToLogin" style="font-family: 'art'">登 录</el-button>
			</div>

			<div v-if="id != null" style="float: right; display: block; margin-top: 13px; margin-left: 40px;">
				<span style="cursor: pointer; margin-right: 15px;" @click="userinfo"><u>{{ username }}</u></span>
				<el-button type="primary" @click="goToLogout" style="font-family: 'art'">退 出 </el-button>
			</div>
		</el-menu>

		<!-- 主要内容 -->
		<el-main class="main-content">
			<component :is="currentComponent"></component>
		</el-main>

		<!-- 底部说明 -->
		<el-footer class="footer_web"
			style="background-color: #f8f9fa; padding: 0 0; height: 28px; border-top: 1px solid #e7e7e7;">
			<div style="display: flex; justify-content: space-between; align-items: center; margin: 0; height: 100%;">
				<div style="flex: 1; text-align: left; padding-left: 10px; width: 33%">
					<p style="margin: 0; font-size: 14px; line-height: 28px; color: #6c757d">海洋生物种群动态预测平台</p>
				</div>
				<div style="flex: 1; text-align: center; width: 33%">
					<p style="margin: 0; font-size: 14px; color: #6c757d; line-height: 28px;">© 2024 yuanteli@TJU. All
						rights reserved.</p>
				</div>
				<div style="flex: 1; text-align: right; padding-right: 10px; width: 33%">
					<a href="https://github.com/WinstonLiyt/OceanBioDynamicsHub" target="_blank"
						style="text-decoration: none; color: #6c757d; font-size: 14px; line-height: 28px;">
						<i class="fab fa-github"></i> GitHub: WinstonLiyt/OceanBioDynamicsHub
					</a>
				</div>
			</div>
		</el-footer>
	</div>

	<!-- 注册弹框 -->
	<el-dialog :visible.sync="dialogVisible" v-model="dialogVisible" title=" 注  册 " width="25%" center
		:close-on-click-modal="false" style="border-radius: 10px;">
		<el-form :model="form" :rules="rules" ref="registerForm" label-width="100px">

			<div class="avatar-upload" @click="handleUploadClick">
				<input type="file" ref="fileInput" accept="image/*" style="display: none" @change="handleFileChange">
				<img v-if='form.imageUrl' :src="baseUrl + form.imageUrl" class="avatar">
				<img v-else :src="imageUrl" class="avatar">
				<i class="el-icon-plus avatar-uploader-icon"></i>
			</div>

			<el-form-item label="账号" prop="account">
				<el-input v-model="form.account"></el-input>
			</el-form-item>
			<el-form-item label="密码" prop="password">
				<el-input type="password" v-model="form.password"></el-input>
			</el-form-item>
			<el-form-item label="确认密码" prop="confirmPassword">
				<el-input type="password" v-model="form.confirmPassword"></el-input>
			</el-form-item>
			<el-form-item label="姓名" prop="name">
				<el-input v-model="form.name"></el-input>
			</el-form-item>
			<el-form-item label="手机号" prop="phone">
				<el-input v-model="form.phone"></el-input>
			</el-form-item>
		</el-form>

		<div slot="footer" class="dialog-footer">
			<el-button @click="dialogVisible = false">取消</el-button>
			<el-button type="primary" @click="register">注册</el-button>
		</div>
	</el-dialog>

	<!-- 登录弹框 -->
	<el-dialog :visible.sync="dialogVisibleLogin" v-model="dialogVisibleLogin" title=" 登  录 " width="25%" center
		:close-on-click-modal="false" style="border-radius: 10px;">
		<el-form :model="formLogin" :rules="rulesLogin" ref="loginForm" label-width="100px">
			<el-form-item label="账号" prop="accountLogin">
				<el-input v-model="formLogin.accountLogin"></el-input>
			</el-form-item>
			<el-form-item label="密码" prop="passwordLogin">
				<el-input type="password" v-model="formLogin.passwordLogin"></el-input>
			</el-form-item>
		</el-form>

		<div slot="footer" class="dialog-footer">
			<el-button @click="dialogVisibleLogin = false">取消</el-button>
			<el-button type="primary" @click="login">登录</el-button>
		</div>
	</el-dialog>

	<!-- 个人信息弹框 -->
	<el-dialog :visible.sync="infoDialogVisible" v-model="infoDialogVisible" title=" 个 人 信 息 " width="25%" center
		:close-on-click-modal="false" style="border-radius: 10px;">
		<el-form :model="formInfo" :rules="rules1" ref="infoForm" label-width="100px">

			<div class="avatar-upload" @click="handleUploadClick">
				<input type="file" ref="fileInput" accept="image/*" style="display: none" @change="handleFileChange">
				<img v-if='formInfo.imageUrl' :src="baseUrl + formInfo.imageUrl" class="avatar">
				<img v-else :src="imageUrl" class="avatar">
				<i class="el-icon-plus avatar-uploader-icon"></i>
			</div>

			<el-form-item label="账号" prop="account">
				<el-input v-model="formInfo.account" disabled></el-input>
			</el-form-item>
			<el-form-item label="原密码" prop="password">
				<el-input type="password" v-model="formInfo.password"></el-input>
			</el-form-item>
			<el-form-item label="新密码" prop="confirmPassword">
				<el-input type="password" v-model="formInfo.confirmPassword"></el-input>
			</el-form-item>
			<el-form-item label="确认新密码" prop="confirmPassword1">
				<el-input type="password" v-model="formInfo.confirmPassword1"></el-input>
			</el-form-item>
			<el-form-item label="姓名" prop="name">
				<el-input v-model="formInfo.name"></el-input>
			</el-form-item>
			<el-form-item label="手机号" prop="phone">
				<el-input v-model="formInfo.phone"></el-input>
			</el-form-item>
		</el-form>

		<div slot="footer" class="dialog-footer">
			<el-button @click="infoDialogVisible = false">取消</el-button>
			<el-button type="primary" @click="updateInfo">修改</el-button>
		</div>
	</el-dialog>
</template>

<script>
import { ref } from 'vue';
import axios from '@/api/index.js'
import { ElMessageBox, ElNotification } from 'element-plus'

import index from '@/views/general/index.vue'
import admin from '@/views/admin/index.vue'
import papers from '@/views/papers.vue'
import info from '@/views/info/info.vue'
import news from '@/views/news/news.vue'
import ocean from '@/views/ocean/oindex.vue'
import marine from '@/views/marine-line/mindex.vue'
import researcher from '@/views/researcher.vue'
import imgs from '@/assets/150.png'
import { baseUrl } from '@/api/index.js'
import icon from '@/assets/icon.png';
import { onMounted } from 'vue';
// import $ from 'jquery';
// import 'material-icons/iconfont/material-icons.css'; // 确保你有加载 Material Icons 的样式


export default {
	name: 'HomeView',
	components: {
		index,
		admin,
		papers,
		info,
		news,
		ocean,
		marine,
		researcher,
	},
	data() {
		return {
			icon,
			baseUrl: baseUrl,
			imageUrl: imgs,
			id: localStorage.getItem('id'),
			username: localStorage.getItem('username'),
			role: localStorage.getItem('role'),
			activeMenu: 'index',// 当前选中的菜单项
			currentComponent: 'index',
			showChatbot: true,
			dialogVisible: false,
			form: {
				imageUrl: '', // 上传的头像图片链接
				account: '',
				password: '',
				confirmPassword: '',
				name: '',
				phone: '',
				img: '',
			},
			formInfo: {
				//id:localStorage.getItem('id'),
				imageUrl: localStorage.getItem('imageUrl'), // 上传的头像图片链接
				account: localStorage.getItem('username'),
				password: '',
				confirmPassword: '',
				confirmPassword1: '',
				name: localStorage.getItem('full_name'),
				phone: localStorage.getItem('phone_number'),
				img: '',
			},
			dialogVisibleLogin: false,
			formLogin: {
				accountLogin: '',
				passwordLogin: '',
			},
			infoDialogVisible: false,
			rules: {
				account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
				password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
				confirmPassword: [
					{ required: true, message: '请再次输入密码', trigger: 'blur' },
					{
						validator: this.checkPasswordConfirmation,
						trigger: 'blur'
					}
				],
				name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
				phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }]
			},
			rulesLogin: {
				accountLogin: [{ required: true, message: '请输入账号', trigger: 'blur' }],
				passwordLogin: [{ required: true, message: '请输入密码', trigger: 'blur' }],
			},
			rules1: {
				account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
				name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
				phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }]
			},
		};
	},
	mounted() {
		$(function () {
			var INDEX = 0;
			$("#chat-submit").click(function (e) {
				e.preventDefault();
				var msg = $("#chat-input").val();
				if (msg.trim() == '') {
					return false;
				}
				generate_message(msg, 'self');

				$.ajax({
					url: '/chat-send',
					type: 'POST',
					data: JSON.stringify({
						message: msg
					}),
					contentType: "application/json",
					success: function (response) {
						generate_message(response.message, 'user');
					}
				});
			});

			function generate_message(msg, type) {
				INDEX++;
				var str = "";
				str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + "\">";
				str += "          <span class=\"msg-avatar\">";
				str += '<img src="https://cdn-icons-png.flaticon.com/512/4139/4139981.png">';
				str += "          <\/span>";
				str += "          <div class=\"cm-msg-text\">";
				str += msg;
				str += "          <\/div>";
				str += "        <\/div>";
				$(".chat-logs").append(str);
				$("#cm-msg-" + INDEX).hide().fadeIn(300);
				if (type == 'self') {
					$("#chat-input").val('');
				}
				$(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
			}

			$(document).delegate(".chat-btn", "click", function () {
				var value = $(this).attr("chat-value");
				var name = $(this).html();
				$("#chat-input").attr("disabled", false);
				generate_message(name, 'self');
			});

			$("#chat-circle").click(function () {
				$("#chat-circle").toggle('scale');
				$(".chat-box").toggle('scale');
			});

			$(".chat-box-toggle").click(function () {
				$("#chat-circle").toggle('scale');
				$(".chat-box").toggle('scale');
			});
		});
	},
	created() {
	},
	methods: {
		updateInfo() {
			this.$refs.infoForm.validate(valid => {
				if (valid) {
					if (this.formInfo.account.length < 6) {
						ElNotification({
							title: '系统提示',
							message: '用户名需要大于等于6位！',
							duration: 3000,
						});
						return;
					}
					if (this.formInfo.password.length > 0) {
						if (this.formInfo.confirmPassword.length < 6 || this.formInfo.confirmPassword1.length < 6) {
							ElNotification({
								title: '系统提示',
								message: '新密码或确认新密码需要大于等于6位！',
								duration: 3000,
							});
							return;
						}
						if (this.formInfo.confirmPassword != this.formInfo.confirmPassword1) {
							ElNotification({
								title: '系统提示',
								message: '新密码和确认新密码应相同！',
								duration: 3000,
							});
							return;
						}
					}
					if (!/^[1][3,4,5,6,7,8,9][0-9]{9}$/.test(this.formInfo.phone)) {
						ElNotification({
							title: '系统提示',
							message: '手机格式错误！',
							duration: 3000,
						});
						return;
					}
					this.formInfo.id = this.id;
					this.formInfo.img = this.formInfo.imageUrl; //.replace(baseUrl,'');

					// 执行修改逻辑
					axios.post('/api/update_info', this.formInfo, { headers: { "Access-Control-Allow-Origin": "*" } })
						.then(response => {
							if (response.data.code == 0) {
								ElNotification({
									title: '系统提示',
									message: '修改成功！',
									duration: 3000,
								});
								this.infoDialogVisible = false;

								localStorage.setItem('username', this.formInfo.account);
								localStorage.setItem('imageUrl', this.formInfo.imageUrl);
								localStorage.setItem('full_name', this.formInfo.name);
								localStorage.setItem('phone_number', this.formInfo.phone);

								this.formInfo.password = '';
								this.formInfo.confirmPassword = '';
								this.formInfo.confirmPassword1 = '';
							} else {
								ElNotification({
									title: '系统提示',
									message: response.data.msg,
									duration: 3000,
								})
							}
							// 请求成功，将数据绑定到表格中
							//this.tableData = response.data.data;
							//this.total=this.tableData.length;
							//this.handleSearch();
						})
						.catch(error => {
							// 请求失败，处理错误
							ElNotification({
								title: '系统提示',
								message: '修改失败',
								duration: 3000,
							})
							console.error('请求数据失败:', error);
						});
					//console.log('注册成功');
					//this.dialogVisible = false;
				} else {
					console.log('表单验证失败');
					return false;
				}
			});
		},
		userinfo() {
			console.log('this.form=', this.form);
			console.log('this.formInfo=', this.formInfo);
			this.infoDialogVisible = true;
		},
		handleUploadClick() {
			this.$refs.fileInput.click();
		},
		async handleFileChange(event) {
			const file = event.target.files[0];
			console.log('file=' + file);
			if (!file) {
				ElNotification({
					title: '系统提示',
					message: '请选择需要上传的文件',
					duration: 3000,
				})
				return;
			}
			const formDatas = new FormData();
			formDatas.append('file', file);

			const response = await axios.post('/api/info_upload', formDatas, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			});
			//console.log('1服务器返回的数据:', response);
			if (response.data.code == 0) {
				//this.imageUrl = baseUrl + response.data.data;
				this.form.imageUrl = response.data.data;
				this.formInfo.imageUrl = response.data.data;
				//console.log('55=', this.imageUrl)
				//console.log('66=', this.form.imageUrl)
			} else {
				ElNotification({
					title: '系统提示',
					message: '上传失败',
					//message:error,
					duration: 3000,
				})
			}
		},

		goToLogin() {
			this.formLogin = this.$options.data().formLogin;
			this.dialogVisibleLogin = true;
		},
		goToRegister() {
			this.form = this.$options.data().form;
			this.dialogVisible = true;
		},
		goToLogout() {
			localStorage.removeItem('username');
			localStorage.removeItem('role');
			localStorage.removeItem('id');
			localStorage.removeItem('full_name');
			localStorage.removeItem('phone_number');
			localStorage.removeItem('imageUrl');


			this.id = localStorage.getItem('id');
			this.username = localStorage.getItem('username');
			this.role = localStorage.getItem('role');
			this.formInfo.imageUrl = localStorage.getItem('imageUrl');
			this.formInfo.name = localStorage.getItem('full_name');
			this.formInfo.phone = localStorage.getItem('phone_number');
			this.currentComponent = 'index';
			this.activeMenu = 'index';
		},
		checkPasswordConfirmation(rule, value, callback) {
			if (value !== this.form.password) {
				callback(new Error('两次输入的密码不一致！'));
			} else {
				callback();
			}
		},
		register() {
			this.$refs.registerForm.validate(valid => {
				if (valid) {
					if (this.form.account.length < 6) {
						ElNotification({
							title: '系统提示',
							message: '用户名需要大于等于6位！',
							duration: 3000,
						});
						return;
					}
					if (this.form.password.length < 6) {
						ElNotification({
							title: '系统提示',
							message: '密码需要大于等于6位！',
							duration: 3000,
						});
						return;
					}
					if (this.form.password != this.form.confirmPassword) {
						ElNotification({
							title: '系统提示',
							message: '两次输入的密码不一致！',
							duration: 3000,
						});
						return;
					}
					if (!/^[1][3,4,5,6,7,8,9][0-9]{9}$/.test(this.form.phone)) {
						ElNotification({
							title: '系统提示',
							message: '手机格式错误！',
							duration: 3000,
						});
						return;
					}

					this.form.img = this.form.imageUrl;

					// 执行注册逻辑
					axios.post('/api/register', this.form, { headers: { "Access-Control-Allow-Origin": "*" } })
						.then(response => {
							//console.log(response);
							if (response.data.code == 0) {
								ElNotification({
									title: '系统提示',
									message: '注册成功！',
									duration: 3000,
								});
								this.dialogVisible = false;
								this.form = this.$options.data().form;
							} else {
								ElNotification({
									title: '系统提示',
									message: response.data.msg,
									duration: 3000,
								})
							}
							// 请求成功，将数据绑定到表格中
							//this.tableData = response.data.data;
							//this.total=this.tableData.length;
							//this.handleSearch();
						})
						.catch(error => {
							// 请求失败，处理错误
							ElNotification({
								title: '系统提示',
								message: '登录失败',
								duration: 3000,
							})
							console.error('请求数据失败:', error);
						});
					//console.log('注册成功');
					//this.dialogVisible = false;
				} else {
					console.log('表单验证失败');
					return false;
				}
			});
		},
		login() {
			//this.formLogin.accountLogin=''
			this.$refs.loginForm.validate(valid => {
				if (valid) {
					if (this.formLogin.accountLogin.length < 6) {
						ElNotification({
							title: '系统提示',
							message: '用户名需要大于等于6位！',
							duration: 3000,
						});
						return;
					}
					if (this.formLogin.passwordLogin.length < 6) {
						ElNotification({
							title: '系统提示',
							message: '密码需要大于等于6位！',
							duration: 3000,
						});
						return;
					}
					// 执行登录逻辑
					axios.post('/api/login', this.formLogin, { headers: { "Access-Control-Allow-Origin": "*" } })
						.then(response => {
							//console.log(response);
							if (response.data.code == 0) {
								//this.loggedIn=true;
								this.username = response.data.data.username;
								this.role = String(response.data.data.role);
								this.id = response.data.data.id;
								localStorage.setItem('username', response.data.data.username);
								localStorage.setItem('role', String(response.data.data.role));
								localStorage.setItem('id', response.data.data.id);
								this.dialogVisibleLogin = false;

								this.formInfo.account = response.data.data.username;
								this.formInfo.name = response.data.data.full_name;
								this.formInfo.phone = response.data.data.phone_number;
								if (response.data.data.imageUrl == '' || response.data.data.imageUrl == null) {
									//return
								} else {
									this.formInfo.imageUrl = response.data.data.imageUrl;
									localStorage.setItem('imageUrl', response.data.data.imageUrl);
								}

								localStorage.setItem('full_name', response.data.data.full_name);
								localStorage.setItem('phone_number', response.data.data.phone_number);

								//console.log('222=', this.form)

								//console.log('role=',this.role);
								//console.log('id=',this.id);
								this.currentComponent = 'index';
								this.activeMenu = 'index';
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
								message: '登录失败',
								duration: 3000,
							})
							console.error('请求数据失败:', error);
						});

					//console.log('注册成功');
					//this.dialogVisible = false;
				} else {
					console.log('表单验证失败');
					return false;
				}
			});
		},

		handleMenuSelect(index) {
			this.activeMenu = index;
			if ('papers' == index) {
				if (localStorage.getItem('id') == null || localStorage.getItem('id') == '') {
					ElNotification({
						title: '发帖提示',
						message: '请登录后再发帖！',
						duration: 3000,
					});
					//this.activeMenu = '';
					return;
				}
			}
			this.currentComponent = index;
			// 根据选中的菜单项执行相应的操作，比如切换内容
		}
	}
};
</script>

<style scoped>
@font-face {
	font-family: 'msyh';
	src: url('../assets/fonts/msyh.ttc') format('truetype');
}

@font-face {
	font-family: 'art';
	src: url('../assets/fonts/art.TTF') format('truetype');
}

.forum-home {
	display: flex;
	flex-direction: column;
	height: 100vh;
}

.top-nav {
	/* background-color: #62a9ff; 导航背景色 */
	background-color: #A9A9A9;

}

.top-nav-inner {
	display: flex;
	justify-content: flex-start;
	align-items: center;
	padding: 0 250px;
	/* 左右页边距 */
}

.guest-info {
	margin-right: 20px;
}

.nav-menu {
	margin: 0;
	/* 去掉默认边距 */
	padding: 0 5px;
	margin-bottom: 2px;
	/* 左右页边距 */
	background-color: #DDDDDD;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-content {
	/* display: flex; */
	flex: 1;
	padding: 0 0;
}

.avatar-upload {
	text-align: center;
	margin-bottom: 20px;
}

.avatar-uploader-icon {
	font-size: 28px;
	color: #999;
	cursor: pointer;
	display: block;
	margin-top: 10px;
}

.avatar {
	width: 120px;
	height: 120px;
	border-radius: 50%;
	cursor: pointer;
}

.forum-posts {
	margin-bottom: 20px;
}

.footer_web {
	text-align: center;
	margin: 0;
}

.dialog-footer {
	display: flex;
	justify-content: center;
	align-items: center;
}

.carousel-img {
	width: 100%;
	height: 100%;
	object-fit: contain;
	/* 保持图片等比例缩放 */
}

#chat-circle {
	position: fixed;
	bottom: 50px;
	right: 50px;
	background: #33CCFF;
	width: 80px;
	height: 80px;
	border-radius: 50%;
	color: white;
	padding: 28px;
	cursor: pointer;
	box-shadow: 0px 3px 16px 0px rgba(0, 0, 0, 0.6), 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
}

.btn#my-btn {
	background: white;
	padding-top: 13px;
	padding-bottom: 12px;
	border-radius: 45px;
	padding-right: 40px;
	padding-left: 40px;
	color: #33CCFF;
}

/* #chat-overlay {
  background: rgba(255, 255, 255, 0.1);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: none;
}

.chat-box {
  display: none;
  background: #efefef;
  position: fixed;
  right: 30px;
  bottom: 50px;
  width: 350px;
  max-width: 85vw;
  max-height: 100vh;
  border-radius: 5px;
  box-shadow: 0px 5px 35px 9px #ccc;
}

.chat-box-toggle {
  float: right;
  margin-right: 15px;
  cursor: pointer;
}

.chat-box-header {
  background: #33CCFF;
  height: 70px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  color: white;
  text-align: center;
  font-size: 20px;
  padding-top: 17px;
}

.chat-box-body {
  position: relative;
  height: 370px;
  overflow: hidden;
}

.chat-box-body:after {
  content: "";
}  */

#chat-circle {
	position: fixed;
	bottom: 50px;
	right: 50px;
	background: #33CCFF;
	width: 80px;
	height: 80px;
	border-radius: 50%;
	color: white;
	padding: 28px;
	cursor: pointer;
	box-shadow: 0px 3px 16px 0px rgba(0, 0, 0, 0.6), 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
}

.btn#my-btn {
	background: white;
	padding-top: 13px;
	padding-bottom: 12px;
	border-radius: 45px;
	padding-right: 40px;
	padding-left: 40px;
	color: #33CCFF;
}

#chat-overlay {
	background: rgba(255, 255, 255, 0.1);
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	border-radius: 50%;
	display: none;
}


.chat-box {
	display: none;
	background: #efefef;
	position: fixed;
	right: 30px;
	bottom: 50px;
	width: 350px;
	max-width: 85vw;
	max-height: 100vh;
	border-radius: 5px;
	/*   box-shadow: 0px 5px 35px 9px #464a92; */
	box-shadow: 0px 5px 35px 9px #ccc;
}

.chat-box-toggle {
	float: right;
	margin-right: 15px;
	cursor: pointer;
}

.chat-box-header {
	background: #33CCFF;
	height: 70px;
	border-top-left-radius: 5px;
	border-top-right-radius: 5px;
	color: white;
	text-align: center;
	font-size: 20px;
	padding-top: 17px;
}

.chat-box-body {
	position: relative;
	height: 370px;
	height: auto;
	border: 1px solid #ccc;
	overflow: hidden;
}

.chat-box-body:after {
	content: "";
	background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTAgOCkiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+PGNpcmNsZSBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIgY3g9IjE3NiIgY3k9IjEyIiByPSI0Ii8+PHBhdGggZD0iTTIwLjUuNWwyMyAxMW0tMjkgODRsLTMuNzkgMTAuMzc3TTI3LjAzNyAxMzEuNGw1Ljg5OCAyLjIwMy0zLjQ2IDUuOTQ3IDYuMDcyIDIuMzkyLTMuOTMzIDUuNzU4bTEyOC43MzMgMzUuMzdsLjY5My05LjMxNiAxMC4yOTIuMDUyLjQxNi05LjIyMiA5LjI3NC4zMzJNLjUgNDguNXM2LjEzMSA2LjQxMyA2Ljg0NyAxNC44MDVjLjcxNSA4LjM5My0yLjUyIDE0LjgwNi0yLjUyIDE0LjgwNk0xMjQuNTU1IDkwcy03LjQ0NCAwLTEzLjY3IDYuMTkyYy02LjIyNyA2LjE5Mi00LjgzOCAxMi4wMTItNC44MzggMTIuMDEybTIuMjQgNjguNjI2cy00LjAyNi05LjAyNS0xOC4xNDUtOS4wMjUtMTguMTQ1IDUuNy0xOC4xNDUgNS43IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PHBhdGggZD0iTTg1LjcxNiAzNi4xNDZsNS4yNDMtOS41MjFoMTEuMDkzbDUuNDE2IDkuNTIxLTUuNDEgOS4xODVIOTAuOTUzbC01LjIzNy05LjE4NXptNjMuOTA5IDE1LjQ3OWgxMC43NXYxMC43NWgtMTAuNzV6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIvPjxjaXJjbGUgZmlsbD0iIzAwMCIgY3g9IjcxLjUiIGN5PSI3LjUiIHI9IjEuNSIvPjxjaXJjbGUgZmlsbD0iIzAwMCIgY3g9IjE3MC41IiBjeT0iOTUuNSIgcj0iMS41Ii8+PGNpcmNsZSBmaWxsPSIjMDAwIiBjeD0iODEuNSIgY3k9IjEzNC41IiByPSIxLjUiLz48Y2lyY2xlIGZpbGw9IiMwMDAiIGN4PSIxMy41IiBjeT0iMjMuNSIgcj0iMS41Ii8+PHBhdGggZmlsbD0iIzAwMCIgZD0iTTkzIDcxaDN2M2gtM3ptMzMgODRoM3YzaC0zem0tODUgMThoM3YzaC0zeiIvPjxwYXRoIGQ9Ik0zOS4zODQgNTEuMTIybDUuNzU4LTQuNDU0IDYuNDUzIDQuMjA1LTIuMjk0IDcuMzYzaC03Ljc5bC0yLjEyNy03LjExNHpNMTMwLjE5NSA0LjAzbDEzLjgzIDUuMDYyLTEwLjA5IDcuMDQ4LTMuNzQtMTIuMTF6bS04MyA5NWwxNC44MyA1LjQyOS0xMC44MiA3LjU1Ny00LjAxLTEyLjk4N3pNNS4yMTMgMTYxLjQ5NWwxMS4zMjggMjAuODk3TDIuMjY1IDE4MGwyLjk0OC0xOC41MDV6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIvPjxwYXRoIGQ9Ik0xNDkuMDUgMTI3LjQ2OHMtLjUxIDIuMTgzLjk5NSAzLjM2NmMxLjU2IDEuMjI2IDguNjQyLTEuODk1IDMuOTY3LTcuNzg1LTIuMzY3LTIuNDc3LTYuNS0zLjIyNi05LjMzIDAtNS4yMDggNS45MzYgMCAxNy41MSAxMS42MSAxMy43MyAxMi40NTgtNi4yNTcgNS42MzMtMjEuNjU2LTUuMDczLTIyLjY1NC02LjYwMi0uNjA2LTE0LjA0MyAxLjc1Ni0xNi4xNTcgMTAuMjY4LTEuNzE4IDYuOTIgMS41ODQgMTcuMzg3IDEyLjQ1IDIwLjQ3NiAxMC44NjYgMy4wOSAxOS4zMzEtNC4zMSAxOS4zMzEtNC4zMSIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjEuMjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvZz48L3N2Zz4=');
	opacity: 0.1;
	top: 0;
	left: 0;
	bottom: 0;
	right: 0;
	height: 100%;
	position: absolute;
	z-index: -1;
}

#chat-input {
	background: #f4f7f9;
	width: 100%;
	position: relative;
	height: 47px;
	padding-top: 10px;
	padding-right: 50px;
	padding-bottom: 10px;
	padding-left: 15px;
	border: none;
	resize: none;
	outline: none;
	border: 1px solid #ccc;
	color: #888;
	border-top: none;
	border-bottom-right-radius: 5px;
	border-bottom-left-radius: 5px;
	overflow: hidden;
}

.chat-input>form {
	margin-bottom: 0;
}

#chat-input::-webkit-input-placeholder {
	/* Chrome/Opera/Safari */
	color: #ccc;
}

#chat-input::-moz-placeholder {
	/* Firefox 19+ */
	color: #ccc;
}

#chat-input:-ms-input-placeholder {
	/* IE 10+ */
	color: #ccc;
}

#chat-input:-moz-placeholder {
	/* Firefox 18- */
	color: #ccc;
}

.chat-submit {
	position: absolute;
	bottom: 3px;
	right: 10px;
	background: transparent;
	box-shadow: none;
	border: none;
	border-radius: 50%;
	color: #33CCFF;
	width: 35px;
	height: 35px;
}

.chat-logs {
	padding: 15px;
	height: 370px;
	overflow-y: scroll;
}

.chat-logs::-webkit-scrollbar-track {
	-webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
	background-color: #F5F5F5;
}

.chat-logs::-webkit-scrollbar {
	width: 5px;
	background-color: #F5F5F5;
}

.chat-logs::-webkit-scrollbar-thumb {
	background-color: #33CCFF;
}



@media only screen and (max-width: 500px) {
	.chat-logs {
		height: 40vh;
	}
}

.chat-msg.user>.msg-avatar img {
	width: 45px;
	height: 45px;
	border-radius: 50%;
	float: left;
	width: 15%;
}

.chat-msg.self>.msg-avatar img {
	width: 45px;
	height: 45px;
	border-radius: 50%;
	float: right;
	width: 15%;
}

.cm-msg-text {
	background: white;
	padding: 10px 15px 10px 15px;
	color: #666;
	max-width: 75%;
	float: left;
	margin-left: 10px;
	position: relative;
	margin-bottom: 20px;
	border-radius: 30px;
}

.chat-msg {
	clear: both;
}

.chat-msg.self>.cm-msg-text {
	float: right;
	margin-right: 10px;
	background: #33CCFF;
	color: white;
}

.cm-msg-button>ul>li {
	list-style: none;
	float: left;
	width: 50%;
}

.cm-msg-button {
	clear: both;
	margin-bottom: 70px;
}
</style>

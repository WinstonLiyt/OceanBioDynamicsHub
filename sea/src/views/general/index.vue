<template>
	<!-- 左侧帖子部分 -->
	<!-- Banner 和欢迎语 -->
	<div class="banner">
		<div class="overlay"></div>
		<div class="welcome-text">
			<img src="../../assets/home/animal4.gif" alt="Welcome Animation" class="welcome-gif">
			欢迎来到海洋生物种群动态预测平台！探索神秘的海洋世界，分享您的发现与见解。
			<img src="../../assets/home/animal.gif" alt="Welcome Animation" class="welcome-gif">
		</div>
	</div>

	<!-- 主体内容 -->
	<el-main class="main-content">
		<div>
			<!-- interval设置图片自动轮放时间，单位毫秒  -->
			<!-- 轮播图 -->
			<el-carousel :interval="2000" type="card" height="350px" indicator-position="outside">
				<el-carousel-item v-for="image in images" :key="image">
					<img :src="image" class="carousel-img">
				</el-carousel-item>
			</el-carousel>
		</div>

		<!-- 图片说明部分 -->
		<div class="info-section">
			<div class="info-card" v-for="info in infos" :key="info.title">
				<img :src="info.image" class="info-img">
				<div class="info-text">
					<h3>{{ info.title }}</h3>
					<p>{{ info.description }}</p>
				</div>
			</div>
		</div>
		
		<div class="project-description">
					<p>为了贯彻这一战略指导，本项目设计并开发了一款用于存储、讨论和预测海洋生物种群相关数据与信息的数据库系统，旨在为海洋生物多样性的保护和可持续利用提供科学支持与决策依据，并增强公众对海洋生物的了解和喜爱。</p>
				</div>

		<component :is="currentComponent"></component>
	</el-main>
</template>

<script>
import axios from '@/api/index.js'
import { ElMessageBox, ElNotification } from 'element-plus'
import adminpng from '@/assets/admin.jpg'
import researcherpng from '@/assets/researcher.jpg'
import userpng from '@/assets/user.png'
import { location } from '@element-plus/icons-vue'
// import 'element-plus/theme-chalk/src/base.scss'
// import 'element-plus/theme-chalk/src/icon.scss'

export default {
	data() {
		return {
			images: [
				require("../../assets/home/s1.jpg"),
				require("../../assets/home/s2.jpg"),
				require("../../assets/home/s3.jpg"),
				require("../../assets/home/s4.jpg"),
				require("../../assets/home/s5.jpg"),
				require("../../assets/home/s6.jpg"),
			],
			infos: [
				{
					image: require("../../assets/home/t1.jpeg"),
					title: "全球海洋温度攀升",
					description: "2022年全球海洋温度创下自1958年有记录以来的最高纪录海洋温度，并且自1990年以来全球海洋温度一直呈加速上升趋势。",
				},
				{
					image: require("../../assets/home/t2.jpg"),
					title: "海洋生物愈发濒危",
					description: "海洋中众多物种正面临着濒临灭绝的危机。国际自然保护联盟的红色名录进一步揭示了超过41,200种物种目前正受到灭绝威胁。",
				},
				{
					image: require("../../assets/home/t3.jpg"),
					title: "中国海洋保护战略",
					description: "习近平总书记在二十大中所强调的，发展海洋经济、保护海洋生态环境以及加速建设海洋强国是推动中国特色现代化的重要任务和组成部分。",
				},
			],
		};
	},
};
</script>

<style scoped>
.banner {
	position: relative;
	height: 100px;
	display: flex;
	align-items: center;
	justify-content: center;
	text-align: center;
	color: white;
}

.overlay {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: linear-gradient(135deg, #808080, #80deea);
	/* Dark overlay for better text readability */
}

.welcome-text {
	position: relative;
	z-index: 1;
	font-size: 24px;
	max-width: 90%;
	margin: 0 auto;
	display: flex;
	align-items: center;
	justify-content: center;
	font-family: 'art';
}

.welcome-gif {
	width: 110px;
	height: 110px;
	margin-right: 20px;
	margin-left: 20px;
}

.carousel-img {
	width: 100%;
	height: 100%;
	object-fit: contain;
	/* 保持图片等比例缩放 */
}

.info-section {
	display: flex;
	justify-content: space-around;
	align-items: center;
	margin-top: 20px;
}

.info-card {
	width: 30%;
	background: white;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
	border-radius: 10px;
	overflow: hidden;
	text-align: center;
}

.info-img {
	width: 100%;
	height: 230px;
	object-fit: cover;
}

.info-text {
	padding: 20px;
}

.info-text h3 {
	margin: 10px 0;
	font-size: 20px;
}

.info-text p {
	color: #666;
}

.project-description {
	margin: 40px auto;
	padding: 20px;
	max-width: 90%;
	background: linear-gradient(135deg, #e0f7fa, #80deea);
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	border-radius: 10px;
	font-size: 18px;
	line-height: 1.6;
	text-align: center;
	color: #333;
	font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.project-description p {
	margin: 0;
	padding: 10px;
	color: #004d40;
	font-size: 20px;
	font-weight: 600;
}
</style>
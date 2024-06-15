<template>
	<div style="width:100%;margin-top:30px;">
		<div style="width:25%;text-align: center;display: inline-block;">
			<el-button type="primary" @click="current = 'user'" style="margin-top: 5px;">用户管理</el-button>
		</div>
		<div style="width:25%;text-align: center;display: inline-block;">
			<el-button type="primary" @click="current = 'forum'" style="margin-top: 5px;">帖子管理</el-button>
		</div>
		<div style="width:25%;text-align: center;display: inline-block;">
			<el-button type="primary" @click="current = 'oceanRegion'" style="margin-top: 5px;">海洋区域管理</el-button>
		</div>
		<div style="width:25%;text-align: center;display: inline-block;">
			<el-button type="primary" @click="current = 'marineLife'" style="margin-top: 5px;">海洋生物管理</el-button>
		</div>
	</div>

	<el-main style="width: 100%;">
		<component :is='current'></component>
	</el-main>
</template>

<script>
import user from '@/views/admin/user.vue'
import forum from '@/views/admin/forum.vue'
import marineLife from '@/views/admin/marineLife.vue'
import oceanRegion from '@/views/admin/oceanRegion.vue'
export default {
	components: {
		user,
		forum,
		marineLife,
		oceanRegion
	},
	data() {
		return {
			current: 'user',
		}
	},
}

</script>

<style></style>
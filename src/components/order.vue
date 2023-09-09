<!--<script setup lang="ts">-->
<!--	import axios from "axios"-->
<!--	import { reactive, onMounted } from "vue"-->

<!--	// 表格数据接口-->
<!--	interface ITable {-->
<!--		name: string;-->
<!--		age: number;-->
<!--		describe: string;-->
<!--	}-->

<!--	let data = reactive({-->
<!--		tableData: [] as ITable[],  // 总的数据-->
<!--		pageData: [] as ITable[],   // 分页的数据-->
<!--		currentPage: 1, // 当前页 默认是第一页-->
<!--		pageSize: 10,   // 每页大小 默认每页10条数据-->
<!--		pageTotal: 0 		// 总数据量 默认为 0-->
<!--	})-->

<!--	// 在声明周期函数获取数据-->
<!--	onMounted(() => {-->
<!--		fetchData()-->
<!--	})-->

<!--	const fetchData = async () => {-->
<!--		// pubic/table_data.json ：默认请求后端数据-->
<!--		const result = await axios.get("/table_data.json")-->

<!--		data.tableData = result.data.data-->
<!--		data.pageTotal = result.data.data.length-->

<!--		data.pageData = queryByPage()-->
<!--	}-->

<!--	// 实现分页的方法-->
<!--	const queryByPage = (): ITable[] => {-->
<!--		// 起始位置 = (当前页 - 1) x 每页的大小-->
<!--		let start = (data.currentPage - 1) * data.pageSize-->
<!--		// 结束位置 = 当前页 x 每页的大小-->
<!--		let end = data.currentPage * data.pageSize-->

<!--		// 返回切割数组后的数据-->
<!--		return data.tableData.slice(start, end)-->
<!--	}-->

<!--	// 改变每页大小的方法-->
<!--	const handleSizeChange = (val: number) => {-->
<!--		data.pageSize = val-->

<!--		data.pageData = queryByPage()-->
<!--	}-->

<!--	// 改变当前页的方法-->
<!--	const handleCurrentChange = (val: number) => {-->
<!--		data.currentPage = val-->

<!--		data.pageData = queryByPage()-->
<!--	}-->
<!--</script>-->

<!--<template>-->
<!--	<el-card class="box-card" style="width: 70%;">-->
<!--    <template #header>-->
<!--      <div class="card-header">-->
<!--        <span>vue3实现前端分页</span>-->
<!--      </div>-->
<!--    </template>-->
<!--		<el-table :data="data.pageData" border style="width: 100%;">-->
<!--    <el-table-column prop="name" label="姓名" width="150" align="center" />-->
<!--    <el-table-column prop="age" label="年龄" width="80" align="center" />-->
<!--    <el-table-column prop="describe" label="描述" align="center" />-->
<!--  </el-table>-->
<!--	<el-pagination-->
<!--		v-model:currentPage="data.currentPage"-->
<!--		v-model:page-size="data.pageSize"-->
<!--		:page-sizes="[10, 20, 50, 100]"-->
<!--		:background="true"-->
<!--		layout="total, sizes, prev, pager, next, jumper"-->
<!--		:total="data.pageTotal"-->
<!--		@size-change="handleSizeChange"-->
<!--		@current-change="handleCurrentChange"-->
<!--		style="margin-top: 12px;display: flex;justify-content: flex-end;"-->
<!--	/>-->
<!--  </el-card>-->
<!--</template>-->

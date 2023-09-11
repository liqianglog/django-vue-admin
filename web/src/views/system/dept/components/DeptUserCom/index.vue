<template>
	<div v-show="!showCount" class="dept-user-com-box dept-info">
		<div class="di-left">
			<h3>{{ deptInfo.dept_name || '' }}</h3>
			<div class="di-cell">
				<p>部门负责人：</p>
				<p class="content">{{ deptInfo.owner || '无' }}</p>
			</div>
			<div class="di-cell">
				<p>部门人数：</p>
				<p class="content">{{ deptInfo.dept_user || 0 }}人</p>
			</div>
			<div class="di-cell">
				<p>部门简介：</p>
				<p class="content">{{ deptInfo.description || '无' }}</p>
			</div>
			<div class="di-cell">
				<p>显示子级：</p>
				<el-switch
					v-model="isShowChildFlag"
					inline-prompt
					active-text="是"
					inactive-text="否"
					:disabled="!currentDeptId"
					@change="handleSwitchChange"
					style="--el-switch-on-color: var(--el-color-primary)"
				/>
			</div>
		</div>
		<div style="height: 180px; width: 380px" ref="deptCountBar"></div>
		<div style="height: 180px; width: 200px" ref="deptSexPie"></div>
	</div>

	<fs-crud
		ref="crudRef"
		v-bind="crudBinding"
		:customClass="!showCount ? 'dept-user-com-box dept-user-com-table' : 'dept-user-com-box dept-user-com-table-cover'"
	>
		<template #toolbar-left>
			<el-button :icon="!showCount ? 'Hide' : 'View'" circle @click="showCount = !showCount"></el-button>
		</template>
		<template #actionbar-right>
			<importExcel api="api/system/user/">导入 </importExcel>
		</template>
	</fs-crud>
</template>

<script lang="ts" setup name="user">
import { ref, onMounted } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import importExcel from '/@/components/importExcel/index.vue';
import * as echarts from 'echarts';
import { ECharts, EChartsOption, init } from 'echarts';
import { getDeptInfoById } from './api';
import { HeadDeptInfoType } from '../../types';

let deptCountChart: ECharts;
let deptSexChart: ECharts;

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });

let currentDeptId = ref('');
let deptCountBar = ref();
let deptSexPie = ref();
let isShowChildFlag = ref(false);
let deptInfo = ref<Partial<HeadDeptInfoType>>({});
let showCount = ref(false);

/**
 * 初始化顶部部门折线图
 */
const initDeptCountBarChart = () => {
	const xAxisData = deptInfo.value.sub_dept_map?.map((item) => item.name) || [];
	const yAxisData = deptInfo.value.sub_dept_map?.map((item) => item.count) || [];

	const option: EChartsOption = {
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow',
			},
		},
		xAxis: {
			type: 'category',
			data: xAxisData,
			axisTick: {
				alignWithLabel: true,
			},
		},
		yAxis: {
			type: 'value',
		},
		dataZoom: [
			{
				type: 'inside',
			},
		],
		grid: {
			top: '6%',
			right: '5%',
			bottom: '10%',
			left: '10%',
		},
		series: [
			{
				data: yAxisData,
				type: 'bar',
				barWidth: '60%',
				showBackground: true,
				itemStyle: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
						{ offset: 0, color: '#83bff6' },
						{ offset: 0.5, color: '#188df0' },
						{ offset: 1, color: '#188df0' },
					]),
				},
			},
		],
	};

	deptCountChart.setOption(option);
};

/**
 * 初始化顶部性别统计
 */
const initDeptSexPieChart = () => {
	const option: EChartsOption = {
		tooltip: {
			trigger: 'item',
		},
		legend: {
			orient: 'vertical',
			right: '0%',
			left: '65%',
			top: 'center',
			itemWidth: 12,
			itemHeight: 12,
		},
		series: [
			{
				type: 'pie',
				radius: '65%',
				center: ['32%', '50%'],
				label: {
					show: false,
					position: 'center',
				},
				color: ['#188df0', '#f56c6c', '#dcdfe6'],
				data: [
					{ value: deptInfo.value.gender?.male || 0, name: '男' },
					{ value: deptInfo.value.gender?.female || 0, name: '女' },
					{ value: deptInfo.value.gender?.unknown || 0, name: '未知' },
				],
			},
		],
	};
	deptSexChart.setOption(option);
};

/**
 * 获取顶部部门信息
 */
const getDeptInfo = async () => {
	const res = await getDeptInfoById(currentDeptId.value, isShowChildFlag.value ? '1' : '0');
	if (res?.code === 2000) {
		deptInfo.value = res.data;
		initDeptCountBarChart();
		initDeptSexPieChart();
	}
};

/**
 * 部门切换刷新用户列表
 */
const handleDoRefreshUser = (id: string) => {
	currentDeptId.value = id;
	crudExpose.doSearch({ form: { dept: id } });
	getDeptInfo();
};

const handleSwitchChange = () => {
	handleDoRefreshUser(currentDeptId.value);
};

onMounted(() => {
	crudExpose.doRefresh();
	deptCountChart = init(deptCountBar.value as HTMLElement);
	deptSexChart = init(deptSexPie.value as HTMLElement);
	getDeptInfo();
});

defineExpose({
	handleDoRefreshUser,
});

// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose, context: { getDeptInfo, isShowChildFlag } });

// 初始化crud配置
const { resetCrudOptions } = useCrud({
	crudExpose,
	crudOptions,
	context: {},
});
</script>

<style lang="scss" scoped>
.dept-user-com-box {
	padding: 0 10px;
	border-radius: 8px 0 0 8px;
	box-sizing: border-box;
	background-color: #fff;
}
.dept-user-com-table {
	height: calc(100% - 200px);
}
.dept-user-com-table-cover {
	height: 100%;
}
.dept-info {
	width: 100%;
	height: 200px;
	display: flex;
	align-items: center;
	justify-content: space-around;
	margin-bottom: 10px;

	.di-left {
		h3 {
			font-size: 18px;
			font-weight: 900;
		}
		.di-cell {
			margin-top: 6px;
			display: flex;
			align-items: center;

			p:nth-child(1) {
				display: block;
				width: 85px;
				text-align: left;
			}
			.content {
				max-width: 120px;
				overflow: hidden;
				white-space: nowrap;
				text-overflow: ellipsis;
			}
		}
	}
}
</style>

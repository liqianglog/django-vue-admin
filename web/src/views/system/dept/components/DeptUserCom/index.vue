<template>
	<div class="dept-user-com-box dept-info">
		<div class="di-left">
			<div class="di-cell">
				<h3>技术部</h3>
				<!-- <el-switch
							v-model="isShowChildFlag"
							inline-prompt
							active-text="是"
							inactive-text="否"
							style="--el-switch-on-color: var(--el-color-primary)"
						/> -->
			</div>
			<div class="di-cell">
				<p>部门人数：10人</p>
				<p class="di-margin">部门负责人：test</p>
			</div>
			<p>部门简介：</p>
		</div>
		<div style="height: 100px; width: 150px" ref="deptSexPie"></div>
		<div class="dept-split">
			<div class="ds-line"></div>
		</div>
	</div>
	<fs-crud ref="crudRef" v-bind="crudBinding" customClass="dept-user-com-box dept-user-com-table">
		<!-- -->
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
import { ECharts, EChartsOption, init } from 'echarts';

let chart: ECharts;

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose });
// 初始化crud配置
const { resetCrudOptions } = useCrud({
	crudExpose,
	crudOptions,
	context: {},
});

let deptSexPie = ref();
let isShowChildFlag = ref(false);

/**
 * 部门切换刷新用户列表
 */
const handleDoRefreshUser = (id: string) => {
	crudExpose.doSearch({ form: { dept: id } });
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
			left: '58%',
			top: 'center',
			itemWidth: 12,
			itemHeight: 12,
		},
		series: [
			{
				type: 'pie',
				radius: '65%',
				center: ['35%', '50%'],
				label: {
					show: false,
					position: 'center',
				},
				color: ['#51A3FC', '#E790E8', '#dcdfe6'],
				data: [
					{ value: 1048, name: '男' },
					{ value: 735, name: '女' },
					{ value: 580, name: '未知' },
				],
			},
		],
	};
	chart.setOption(option);
};

onMounted(() => {
	crudExpose.doRefresh();
	chart = init(deptSexPie.value as HTMLElement);
	initDeptSexPieChart();
});

defineExpose({
	handleDoRefreshUser,
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
			display: flex;
			align-items: center;
		}
		.di-margin {
			margin-left: 20px;
		}
		p {
			margin-top: 6px;
		}
	}
}
</style>

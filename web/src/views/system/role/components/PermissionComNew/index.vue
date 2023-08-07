<template>
	<div class="permission-com">
		<el-button size="small" type="primary" class="pc-save-btn">保存菜单授权</el-button>
		<el-collapse v-model="collapseCurrent" @change="handleCollapseChange" accordion>
			<el-collapse-item v-for="item in menuData" :key="item.key" :name="item.key">
				<template #title>
					<div @click.stop="handleClick">
						<p class="pc-collapse-title">
							<el-checkbox v-model="item.isCheck">
								<span>{{ item.name }}</span>
							</el-checkbox>
						</p>
						<div v-show="!collapseCurrent.includes(item.key)">
							<el-checkbox v-for="btn in item.btns" :key="btn.value" :label="btn.value" v-model="btn.isCheck">{{ btn.label }}</el-checkbox>
						</div>
					</div>
				</template>
				<div class="pc-collapse-main">
					<div class="pccm-item">
						<p>允许对这些数据有以下操作</p>
						<el-checkbox v-for="btn in item.btns" :key="btn.value" v-model="btn.isCheck" :label="btn.value">
							<p class="btn-item">
								{{ btn.label }}
								<span @click.stop.prevent="handleSettingClick">
									<el-icon><Setting /></el-icon>
								</span>
							</p>
						</el-checkbox>
					</div>

					<div class="pccm-item">
						<p>对这些数据有以下字段权限</p>

						<el-radio-group v-model="item.radio">
							<el-radio label="1">全部字段可查看可编辑</el-radio>
							<el-radio label="2">全部字段仅可查看不可编辑</el-radio>
							<el-radio label="3">自定义字段权限</el-radio>
						</el-radio-group>

						<ul v-show="item.radio === '3'" class="columns-list">
							<li class="columns-head">
								<div class="width-txt">
									<span>字段</span>
								</div>
								<div class="width-check">
									<el-checkbox name="look"><span>查看</span></el-checkbox>
								</div>
								<div class="width-check">
									<el-checkbox name="edit"><span>编辑</span></el-checkbox>
								</div>
							</li>

							<li class="columns-item">
								<div class="width-txt">姓名</div>
								<div class="width-check"><el-checkbox class="ci-checkout"></el-checkbox></div>
								<div class="width-check"><el-checkbox class="ci-checkout"></el-checkbox></div>
							</li>

							<li class="columns-item">
								<div class="width-txt">性别</div>
								<div class="width-check"><el-checkbox class="ci-checkout"></el-checkbox></div>
								<div class="width-check"><el-checkbox class="ci-checkout"></el-checkbox></div>
							</li>
						</ul>
					</div>
				</div>
			</el-collapse-item>
		</el-collapse>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

let menuData = ref([
	{
		key: '1',
		name: '用户管理',
		isCheck: true,
		radio: '1',
		btns: [
			{ label: '新增', value: 'create', isCheck: true },
			{ label: '编辑', value: 'edit', isCheck: true },
			{ label: '删除', value: 'delete', isCheck: true },
			{ label: '查询', value: 'look', isCheck: true },
		],
	},
	{
		key: '2',
		name: '系统管理',
		isCheck: false,
		radio: '2',
		btns: [
			{ label: '新增', value: 'create', isCheck: false },
			{ label: '编辑', value: 'edit', isCheck: true },
			{ label: '删除', value: 'delete', isCheck: false },
			{ label: '查询', value: 'look', isCheck: true },
		],
	},
]);
let collapseCurrent = ref(['1']);

const handleClick = () => {};

const handleCollapseChange = (val: string) => {
	collapseCurrent.value = [val];
};

const handleSettingClick = () => {
	console.log(123123);
};
</script>

<style lang="scss" scoped>
.permission-com {
	height: calc(100% - 30px);
	padding: 15px;
	margin: 15px;
	border: 1px solid #ebeef5;
	box-sizing: border-box;
	.pc-save-btn {
		margin-bottom: 15px;
	}
	.pc-collapse-title {
		line-height: 32px;
		span {
			font-size: 16px;
		}
	}
	.pc-collapse-main {
		padding-top: 15px;
		border-top: 1px solid #ebeef5;
		box-sizing: border-box;
		.pccm-item {
			margin-bottom: 10px;

			.btn-item {
				display: flex;
				align-items: center;
				span {
					margin-left: 5px;
				}
			}
			.columns-list {
				.width-txt {
					width: 200px;
				}
				.width-check {
					width: 80px;
				}
				.width-icon {
					cursor: pointer;
				}
				.columns-head {
					display: flex;
					align-items: center;
					padding: 6px 0;
					border-bottom: 1px solid #ebeef5;
					box-sizing: border-box;
					span {
						font-weight: 900;
					}
				}
				.columns-item {
					display: flex;
					align-items: center;
					padding: 6px 0;
					box-sizing: border-box;
					.ci-checkout {
						height: auto !important;
					}
				}
			}
		}
	}
}
</style>

<style lang="scss">
.permission-com {
	.el-collapse-item__header {
		height: auto;
	}
}
</style>

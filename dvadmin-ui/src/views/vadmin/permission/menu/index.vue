<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch">
      <el-form-item label="菜单名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入菜单名称"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="菜单类型" prop="menuType">
        <el-select v-model="queryParams.menuType" placeholder="菜单类型" clearable size="small">
          <el-option
            v-for="dict in menuTypeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="菜单状态" clearable size="small">
          <el-option
            v-for="dict in statusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['permission:menus:post']"
        >新增
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table
      v-loading="loading"
      :data="menuList"
      row-key="id"
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
    >
      <el-table-column prop="name" label="菜单名称" :show-overflow-tooltip="true" width="160"></el-table-column>
      <el-table-column prop="icon" label="图标" align="center" width="100">
        <template slot-scope="scope">
          <svg-icon :icon-class="scope.row.icon || ''"/>
        </template>
      </el-table-column>
      <el-table-column prop="orderNum" label="排序" width="60"></el-table-column>
      <el-table-column prop="menuType" label="菜单类型" :formatter="menuTypeFormat" width="80"></el-table-column>
      <el-table-column prop="perms" label="权限标识" :show-overflow-tooltip="true"></el-table-column>
      <el-table-column prop="component_path" label="组件路径" :show-overflow-tooltip="true"></el-table-column>
      <!--      <el-table-column prop="interface_path" label="接口路径" :show-overflow-tooltip="true"></el-table-column>-->
      <!--      <el-table-column prop="interface_method" label="请求方式" :formatter="interfaceMethodFormat" width="70"></el-table-column>-->
      <el-table-column prop="status" label="状态" :formatter="statusFormat" width="80"></el-table-column>
      <el-table-column label="更新时间" align="center" prop="update_datetime">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.update_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="create_datetime">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.create_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
        v-if="hasPermi(['permission:menus:{id}:put', 'permission:menus:post', 'permission:menus:{id}:delete'])"
      >
        <template slot-scope="scope">
          <el-button size="mini"
                     type="text"
                     icon="el-icon-edit"
                     @click="handleUpdate(scope.row)"
                     v-hasPermi="['permission:menus:{id}:put']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-plus"
            @click="handleAdd(scope.row)"
            v-hasPermi="['permission:menus:post']"
          >新增
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['permission:menus:{id}:delete']"
          >删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加或修改菜单对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="24">
            <el-form-item label="上级菜单">
              <treeselect
                v-model="form.parentId"
                :options="menuOptions"
                :normalizer="normalizer"
                :show-count="true"
                placeholder="选择上级菜单"
              />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="菜单类型" prop="menuType">
              <el-radio-group v-model="form.menuType">
                <el-radio label="0">目录</el-radio>
                <el-radio label="1">菜单</el-radio>
                <el-radio label="2">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item v-if="form.menuType != '2'" label="菜单图标">
              <el-popover
                placement="bottom-start"
                width="460"
                trigger="click"
                @show="$refs['iconSelect'].reset()"
              >
                <IconSelect ref="iconSelect" @selected="selected"/>
                <el-input slot="reference" v-model="form.icon" placeholder="点击选择图标" readonly>
                  <svg-icon
                    v-if="form.icon"
                    slot="prefix"
                    :icon-class="form.icon"
                    class="el-input__icon"
                    style="height: 32px;width: 16px;"
                  />
                  <i v-else slot="prefix" class="el-icon-search el-input__icon"/>
                </el-input>
              </el-popover>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="form.menuType == '2'?'菜单名称':'按钮名称'" prop="name">
              <el-input v-model="form.name" placeholder="请输入菜单名称"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="显示排序" prop="orderNum">
              <el-input-number v-model="form.orderNum" controls-position="right" :min="0"/>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item v-if="form.menuType != '2'" label="是否外链">
              <el-radio-group v-model="form.isFrame">
                <el-radio label="0">是</el-radio>
                <el-radio label="1">否</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="form.menuType != '2'" label="路由地址" prop="web_path">
              <el-input v-model="form.web_path" placeholder="请输入前端路由地址"/>
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="form.menuType != '2'">
            <el-form-item label="组件路径" prop="component_path">
              <el-input v-model="form.component_path" placeholder="请输入前端组件路径" @change="ComponentPathChange"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="form.menuType != '0'" label="接口路径" prop="interface_path">
              <el-input v-model="form.interface_path" placeholder="请输入后端接口路径" @change="InterfacePathChange"/>
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="form.menuType != '0'">
            <el-form-item label="请求方法" prop="interface_method">
              <el-select v-model="form.interface_method" placeholder="请选择后端请求方法" clearable size="small"
                         @change="CreatePerms">
                <el-option
                  v-for="dict in interfaceMethodOptions"
                  :key="dict.dictValue"
                  :label="dict.dictLabel"
                  :value="dict.dictValue"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item v-if="form.menuType != '0'" label="权限标识">
              <el-input v-model="form.perms" placeholder="请权限标识" maxlength="50"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="form.menuType != '2'" label="显示状态">
              <el-radio-group v-model="form.visible">
                <el-radio
                  v-for="dict in visibleOptions"
                  :key="dict.dictValue"
                  :label="dict.dictValue"
                >{{dict.dictLabel}}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="form.menuType != '2'" label="菜单状态">
              <el-radio-group v-model="form.status">
                <el-radio
                  v-for="dict in statusOptions"
                  :key="dict.dictValue"
                  :label="dict.dictValue"
                >{{dict.dictLabel}}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="form.menuType == '1'" label="是否缓存">
              <el-radio-group v-model="form.isCache">
                <el-radio label="0">不缓存</el-radio>
                <el-radio label="1">缓存</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {addMenu, delMenu, getMenu, listMenu, updateMenu} from "@/api/vadmin/permission/menu";
  import Treeselect from "@riophae/vue-treeselect";
  import "@riophae/vue-treeselect/dist/vue-treeselect.css";
  import IconSelect from "@/components/IconSelect";

  export default {
    name: "Menu",
    components: {Treeselect, IconSelect},
    data() {
      return {
        // 遮罩层
        loading: true,
        // 显示搜索条件
        showSearch: true,
        // 菜单表格树数据
        menuList: [],
        // 菜单树选项
        menuOptions: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 显示状态数据字典
        visibleOptions: [],
        // 菜单状态数据字典
        statusOptions: [],
        // 菜单类型数据字典
        menuTypeOptions: [],
        interfaceMethodOptions: [],
        // 查询参数
        queryParams: {
          name: undefined,
          visible: undefined,
          pageNum: 'all'
        },
        // 表单参数
        form: {},
        // 表单校验
        rules: {
          name: [
            {required: true, message: "菜单名称不能为空", trigger: "blur"}
          ],
          orderNum: [
            {required: true, message: "菜单顺序不能为空", trigger: "blur"}
          ],
          web_path: [
            {required: true, message: "路由地址不能为空", trigger: "blur"}
          ]
        }
      };
    },
    created() {
      this.getList();
      this.getDicts("sys_show_hide").then(response => {
        this.visibleOptions = response.data;
      });
      this.getDicts("sys_normal_disable").then(response => {
        this.statusOptions = response.data;
      });
      this.getDicts("sys_menu_type").then(response => {
        this.menuTypeOptions = response.data;
      });
      this.getDicts("sys_interface_method").then(response => {
        this.interfaceMethodOptions = response.data;
      });
    },
    methods: {
      // 选择图标
      selected(name) {
        this.form.icon = name;
      },
      /** 接口路径变化，必须斜杠开头，不能斜杠结尾*/
      InterfacePathChange() {
        if(this.form.interface_path.length === 0) {
          this.form.perms = ''
          return
        }
        if (this.form.interface_path.indexOf("/") !== 0) {
          this.form.interface_path = "/" + this.form.interface_path
        }
        if (!this.form.interface_path.endsWith('/')) {
          this.form.interface_path = this.form.interface_path + "/"
        }
        this.CreatePerms()
      },
      /** 自动生成权限标识 */
      CreatePerms() {
        let res = this.form.interface_path + ":" + this.form.interface_method
        this.form.perms = res.toLocaleLowerCase().replace(/(\/)/g, ':').replace(/(::)/g, ':').replace(/(^:)|(:$)/g, "")
      },
      /** 组件路径变化，替换斜杠开头 */
      ComponentPathChange() {
        this.form.component_path = this.form.component_path.replace(/(^\/)/g, '')
      },
      /** 查询菜单列表 */
      getList() {
        this.loading = true;
        listMenu(this.queryParams).then(response => {
          this.menuList = this.handleTree(response.data, "id");
          this.loading = false;
        });
      },
      /** 转换菜单数据结构 */
      normalizer(node) {
        if (node.children && !node.children.length) {
          delete node.children;
        }
        return {
          id: node.id,
          label: node.name,
          children: node.children
        };
      },
      /** 查询菜单下拉树结构 */
      getTreeselect() {
        listMenu({pageNum: 'all'}).then(response => {
          this.menuOptions = [];
          const menu = {id: 0, name: '主类目', children: []};
          menu.children = this.handleTree(response.data, "id");
          this.menuOptions.push(menu);
        });
      },
      // 菜单状态字典翻译
      statusFormat(row, column) {
        return this.selectDictLabel(this.statusOptions, row.status);
      },
      // 菜单类型 字典翻译
      menuTypeFormat(row, column) {
        return this.selectDictLabel(this.menuTypeOptions, row.menuType);
      },
      // 请求方式 字典翻译
      interfaceMethodFormat(row, column) {
        return this.selectDictLabel(this.interfaceMethodOptions, row.interface_method);
      },
      // 取消按钮
      cancel() {
        this.open = false;
        this.reset();
      },
      // 表单重置
      reset() {
        this.form = {
          id: undefined,
          parentId: 0,
          name: undefined,
          icon: undefined,
          web_path: undefined,
          menuType: this.selectDictDefault(this.menuTypeOptions),
          orderNum: undefined,
          component_path: undefined,
          interface_path: undefined,
          perms: undefined,
          interface_method: this.selectDictDefault(this.interfaceMethodOptions),
          isFrame: "1",
          isCache: "1",
          visible: this.selectDictDefault(this.visibleOptions),
          status: this.selectDictDefault(this.statusOptions)
        };
        this.resetForm("form");
      },
      /** 搜索按钮操作 */
      handleQuery() {
        this.getList();
      },
      /** 重置按钮操作 */
      resetQuery() {
        this.resetForm("queryForm");
        this.handleQuery();
      },
      /** 新增按钮操作 */
      handleAdd(row) {
        this.reset();
        this.getTreeselect();
        if (row != null && row.id) {
          this.form.parentId = row.id;
        } else {
          this.form.parentId = 0;
        }
        this.open = true;
        this.title = "添加菜单";
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.reset();
        this.getTreeselect();
        getMenu(row.id).then(response => {
          this.form = response.data;
          this.open = true;
          this.title = "修改菜单";
        });
      },
      /** 提交按钮 */
      submitForm: function () {
        this.$refs["form"].validate(valid => {
          if (valid) {
            const cloneData = JSON.parse(JSON.stringify(this.form))
            if (cloneData.parentId === 0) {
              delete cloneData['parentId']
            }
            if (this.form.id != undefined) {
              updateMenu(cloneData).then(response => {
                this.msgSuccess("修改成功");
                this.open = false;
                this.getList();
              });
            } else {
              addMenu(cloneData).then(response => {
                this.msgSuccess("新增成功");
                this.open = false;
                this.getList();
              });
            }
          }
        });
      },
      /** 删除按钮操作 */
      handleDelete(row) {
        this.$confirm('是否确认删除名称为"' + row.name + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delMenu(row.id);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        })
      }
    }
  };
</script>

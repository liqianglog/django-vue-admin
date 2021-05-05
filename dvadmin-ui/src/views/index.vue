<template>
  <div class="app-container home">
    <el-row :gutter="20">
      <el-col :sm="24" :lg="24">
        <blockquote class="text-warning" style="font-size: 14px">
          领取阿里云通用云产品1888优惠券，精选云服务器 ECS 1核2G 87.12元/年
          <br/>
          <el-link
            href="https://www.aliyun.com/activity/new?source=5176.11533457&userCode=jpef8a71"
            type="primary"
            target="_blank"
          >https://www.aliyun.com/activity/new?source=5176.11533457&userCode=jpef8a71
          </el-link
          >
          <br/>
          领取腾讯云通用云产品2860优惠券，半价购买，满200减100，满500减250
          <br/>
          <el-link
            href="https://curl.qcloud.com/yWalJsQY"
            type="primary"
            target="_blank"
          >https://curl.qcloud.com/yWalJsQY
          </el-link
          >
          <br/>
          阿里云服务器折扣区
          <el-link href="https://www.aliyun.com/minisite/goods?source=5176.11533457&userCode=jpef8a71" type="primary"
                   target="_blank"
          >>☛☛点我进入☚☚
          </el-link
          >
          &nbsp;&nbsp;&nbsp; 腾讯云服务器秒杀区
          <el-link href="https://curl.qcloud.com/cRu8Ljf8" type="primary" target="_blank"
          >>☛☛点我进入☚☚
          </el-link
          >
          <br/>
          <h4 class="text-danger">
            云产品通用红包，可叠加官网常规优惠使用。(仅限新用户)
            <br>
            通过推广链接购买服务器者，可免费提供搭建环境服务一次。
          </h4>
          <h4 class="text-danger">

          </h4>
        </blockquote>
        <hr/>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :sm="24" :lg="12" style="padding-left: 20px">
        <h2>dvAdmin后台管理框架</h2>
        <p>
          一直想做一款后台管理系统，看了很多优秀的开源项目，发现只有Java、Go，但是发现没有合适Python的。于是利用空闲休息时间开始自己写一
          套后台系统。如此有了dvAdmin管理系统。您可以基于此系统进行持续开发，以做出符合自己系统。所有前端后台代码封装过后十分精简易上手，
          出错概率低。同时支持移动客户端访问。系统会陆续更新一些实用功能。
        </p>
        <p>
          <b>当前版本:</b> <span>v{{ version }}</span>
        </p>
        <p>
          <el-tag type="danger">&yen;免费开源</el-tag>
        </p>
        <p>
          <el-button
            type="primary"
            size="mini"
            icon="el-icon-cloudy"
            plain
            @click="goTarget('https://gitee.com/liqianglog/django-vue-admin')"
          >访问码云
          </el-button
          >
          <el-button
            size="mini"
            icon="el-icon-s-home"
            plain
            @click="goTarget('http://django-vue-admin.com')"
          >访问主页
          </el-button
          >
        </p>
      </el-col>

      <el-col :sm="24" :lg="12" style="padding-left: 50px">
        <el-row>
          <el-col :span="12">
            <h2>技术选型</h2>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6">
            <h4>后端技术</h4>
            <ul>
              <li>Python</li>
              <li>Django</li>
              <li>django-redis</li>
              <li>django-celery-beat</li>
              <li>django-rest-framework</li>
              <li>django-rest-framework-jwt</li>
              <li>...</li>
            </ul>
          </el-col>
          <el-col :span="6">
            <h4>前端技术</h4>
            <ul>
              <li>Vue</li>
              <li>Vuex</li>
              <li>Element-ui</li>
              <li>Axios</li>
              <li>Sass</li>
              <li>Quill</li>
              <li>...</li>
            </ul>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <el-divider/>
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="12" :lg="8">
        <el-card class="update-log">
          <div slot="header" class="clearfix">
            <span>联系信息</span>
          </div>
          <div class="body">
            <p>
              <i class="el-icon-s-promotion"></i> 官网：
              <el-link
                href="http://django-vue-admin.com"
                target="_blank"
              >http://django-vue-admin.com
              </el-link
              >
            </p>
            <p>
              <i class="el-icon-user-solid"></i> QQ群：
              <a href="https://qm.qq.com/cgi-bin/qm/qr?k=E2fte0FJlSr56-thAmabGcV3Lv6vLsp9&jump_from=webapi"
                 target="_blank"
              > 812482043</a
              >
            </p>
            <p>
              <img
                src="@/assets/images/qq.jpg"
                alt="donate"
                width="25%"
              />
            </p>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="8">
        <el-card class="update-log">
          <div slot="header" class="clearfix">
            <span>更新日志</span>
          </div>
          <el-collapse accordion>
            <el-collapse-item title="">
              <template slot="title">
                v1.1.0 - 2021-05-05&nbsp;&nbsp;&nbsp;
                <el-badge value="new" class="item" style="padding-top: 10px;padding-left: 10px;"/>
              </template>
              <ol>
                <li>新增服务监控功能</li>
                <li>新增操作日志功能</li>
                <li>新增导入功能</li>
                <li>新增celery定时任务</li>
                <li>新增消息通知功能</li>
                <li>新增后端接口文档</li>
                <li>新增docker-compose部署</li>
                <li>新增支持重写用户模型</li>
                <li>数据权限完善</li>
                <li>登录日志优化</li>
                <li>后端代码架构优化</li>
                <li>文件管理功能完善</li>
                <li>修复创建用户密码问题</li>
                <li>其他细节优化</li>
              </ol>
            </el-collapse-item>
            <el-collapse-item title="v1.0.0 - 2021-03-01">
              <ol>
                <li>dvAdmin前后端分离系统正式发布</li>
              </ol>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="8">
        <el-card class="update-log">
          <div slot="header" class="clearfix">
            <span>捐赠支持</span>
          </div>
          <div class="body">
            <img
              src="@/assets/images/collection_code.jpg"
              alt="donate"
              width="100%"
            />
            <!--            <span style="display: inline-block; height: 30px; line-height: 30px"-->
            <!--              >加群交流就是最好的支持~</span-->
            <!--            >-->
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "index",
    data() {
      return {
        // 版本号
        version: "1.1.0",
      };
    },
    methods: {
      goTarget(href) {
        window.open(href, "_blank");
      },
    },
  };
</script>

<style scoped lang="scss">
  .home {
    blockquote {
      padding: 10px 20px;
      margin: 0 0 20px;
      font-size: 17.5px;
      border-left: 5px solid #eee;
    }

    hr {
      margin-top: 20px;
      margin-bottom: 20px;
      border: 0;
      border-top: 1px solid #eee;
    }

    .col-item {
      margin-bottom: 20px;
    }

    ul {
      padding: 0;
      margin: 0;
    }

    font-family: "open sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 13px;
    color: #676a6c;
    overflow-x: hidden;

    ul {
      list-style-type: none;
    }

    h4 {
      margin-top: 0px;
    }

    h2 {
      margin-top: 10px;
      font-size: 26px;
      font-weight: 100;
    }

    p {
      margin-top: 10px;

      b {
        font-weight: 700;
      }
    }

    .update-log {
      ol {
        display: block;
        list-style-type: decimal;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0;
        margin-inline-end: 0;
        padding-inline-start: 40px;
      }
    }
  }
</style>


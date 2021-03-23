module.exports = {
    title: 'Django-Vue-Admin',
    base: '/',
    head: [
        [
            'link', // 设置 favicon.ico，注意图片放在 public 文件夹下
            { rel: 'icon', href: '/logo.png' }
        ]
    ],
    description: '',
    themeConfig: {
        logo: '/logo.png',
        nav: [
            { text: '在线文档', link: '/document/' },
            { text: '关于我们', link: '/about/' },
            { text: '在线体验', link: 'https://demo.django-vue-admin.com/' },
            { text: 'Gitee', link: 'https://gitee.com/liqianglog/django-vue-admin' },
            { text: 'Github', link: 'https://github.com/liqianglog/django-vue-admin' },
        ],
        sidebar: [
            {
                title: '文档',   // 必要的
                // path: '/document/',      // 可选的, 标题的跳转链接，应为绝对路径且必须存在
                collapsable: false, // 可选的, 默认值是 true,
                sidebarDepth: 1,    // 可选的, 默认值是 1
                children: [
                    '/document/',
                    '/document/kslj',
                    '/document/hjbs',
                    '/document/web',
                    '/document/server',
                    '/document/gxrz',
                ]
            },
            {
                title: '其他',
                children: [
                    '/other/cjwt',
                    '/other/jzzc',
                ],
                collapsable: false,
                sidebarDepth: 1,
                initialOpenGroupIndex: -1 // 可选的, 默认值是 0
            }
        ]
    }
}

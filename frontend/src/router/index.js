import {createRouter, createWebHashHistory } from "vue-router";
import Home from "@/views/Home.vue";

// 制定路由规则
const routes = [
    {
        path: "/",
        name: "main",
        component: () => import("@/views/Main.vue"),
        redirect: "/home", // 默认跳转到home
        children: [
            {
                path: "home",
                name: "home",
                component: () => import("@/views/Home.vue")
            },
            {
                path: 'browse',
                name: 'browse',
                component: () => import('@/views/Browse.vue')
            },
            {
                path: 'help',
                name: 'help',
                component: () => import('@/views/Help.vue')
            },
            {
                path: 'download',
                name: 'download',
                component: () => import('@/views/Download.vue')
            },
            {
                path: '/gene-information',
                name: 'GeneInformationPage',
                component: () => import('@/views/GeneInformationPage.vue'), // 根据实际路径修改
                props: true // 允许通过 props 接收参数
            },
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router;
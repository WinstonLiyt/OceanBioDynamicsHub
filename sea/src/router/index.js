import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  // if (to.path === "/") {
  //   //在登录页清除存储信息
  //   //localStorage.removeItem('tk');
  //   localStorage.removeItem('role');
  //   //localStorage.removeItem('menus');
  // }
  // let role = localStorage.getItem('role');
  // //没有token，则重定向到登录页
  // if (!role && to.path !== "/") {
  //   return "/";
  // }
});

export default router

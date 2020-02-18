import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home'
import Login from '../views/Login'
import Blog from '../views/Blog'
import Registration from "../views/Registration";
import VueStudy from "../views/VueStudy";
import Logout from "../views/Logout";
import CreatePost from "../views/CreatePost";
import FullArticle from "../views/FullArticle";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home,
        meta: { title: 'дом'}
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
        meta: { title: 'Вход'}
    },
    {
        path: '/logout',
        name: 'logout',
        component: Logout,
        meta: { title: 'Выход'}
    },
    {
        path: '/signup',
        name: 'signup',
        component: Registration,
        meta: { title: 'Регистрация'}
    },
    {
        path: '/blog',
        name: 'blog',
        component: Blog,
        meta: { title: 'Блог'}
    },
    {
        path: '/blog/create',
        name: 'create_article',
        component: CreatePost,
        meta: { auth: true, title: 'Создание статьи'}
    },
    {
        path: '/blog/:id',
        name: 'article',
        component: FullArticle,
        meta: { title: 'Статья имя'}
    },
    {
        path: '/Vue-STUDY',
        name: 'VueStudy',
        component: VueStudy,
        meta: { auth: true, title: 'Учеба'}
    },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.auth)) {
    if (localStorage.getItem('token')) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router

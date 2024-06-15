import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import AMapLoader from "@amap/amap-jsapi-loader";
const app = createApp(App)
// var $ = require("jquery")

// 注册ElementPlus图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

// 使用ElementPlus
app.use(store)
   .use(router)
   .use(ElementPlus, { locale: zhCn, })

// // 使用vue-amap
// app.use(VueAMap)

// VueAMap.initAMapApiLoader({
//   key: 'f5bd69297852a95d27f8afaa40b55c44',
//   plugin: ['AMap.Marker'],
//   v: '1.4.15'
// });

app.mount('#app')
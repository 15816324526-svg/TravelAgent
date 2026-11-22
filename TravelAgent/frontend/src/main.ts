import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
/*index.html 创建 #app，
main.ts 把 Vue 安装进 #app，
PlannerView.vue 在里面生成 .planner-page，
CSS 再为它们设置样式*/
createApp(App)
  .use(router)
  .mount('#app') 

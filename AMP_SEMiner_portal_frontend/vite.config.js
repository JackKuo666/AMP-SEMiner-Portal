import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 添加的别名
  resolve:{
    alias:[
      {
        find: "@",
        replacement: "/src",
      }
    ]
  }
})

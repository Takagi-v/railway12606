import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // 加载环境变量（保留本地增强）
  const env = loadEnv(mode, process.cwd(), '')

  return {
    // 以远端为主：保留基础 vue 插件；保留本地按需组件增强
    plugins: [
      vue(),
      Components({
        resolvers: [
          AntDesignVueResolver({
            importStyle: false // css in js
          })
        ]
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      port: 5173,
      host: true, // 保留本地增强：允许外部访问
      proxy: {
        '/api': {
          // 以远端为主的默认目标，同时保留本地可通过环境变量覆盖
          target: env.VITE_API_BASE_URL?.replace('/api', '') || 'http://localhost:8000',
          changeOrigin: true,
          // 保留本地 rewrite（与前缀相同，确保兼容）
          rewrite: path => path.replace(/^\/api/, '/api')
        }
      }
    },
    build: {
      // 保留本地增强：生产构建优化
      outDir: 'dist',
      sourcemap: env.VITE_DEBUG === 'true',
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: env.VITE_DEBUG !== 'true',
          drop_debugger: true
        }
      }
    },
    define: {
      // 保留本地增强：全局常量
      __APP_VERSION__: JSON.stringify(env.VITE_APP_VERSION || '1.0.0'),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString())
    }
  }
})

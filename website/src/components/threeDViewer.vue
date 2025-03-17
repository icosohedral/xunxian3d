<template>
  <div class="flex px-6 py-4 bg-stone-200">
    <h1 class="text-2xl font-bold text-amber-700 flex items-center">
      <img src="/static/slogo.ico" alt="Logo" class="w-20 h-10 mr-2">
      寻仙模型查看器
    </h1>
  </div>
  
  <div class="canvas-container">
    <div class="canvas-wrapper">
      <TresCanvas class="fixed-canvas" clear-color="#FFFFFF"> 
        <TresPerspectiveCamera :position="[0, 2, 5]" />
        <OrbitControls />
        <TresAmbientLight :intensity="1" />
        <TresDirectionalLight :position="[5, 5, 5]" :intensity="0.8" />
        <primitive v-if="objModel" :object="objModel" />
      </TresCanvas>
    </div>

    <!-- 右侧操作区域 -->
    <div class="sidebar text-left">
      <!-- 选择预置模型 -->
      <div class="preset-area">
        <label for="preset-models" class="block mb-2 font-semibold text-gray-700">选择模型</label>
        <select 
          id="preset-models" 
          class="w-full p-2 border rounded-lg" 
          @change="handlePresetSelect"
        >
          <option value="">-- 选择模型 --</option>
          <option v-for="model in presetModels" :key="model.url" :value="model.url">
            {{ model.name }}
          </option>
        </select>
      </div>

      <!-- 文件上传按钮 -->
      <div class="upload-area mt-4">
        <label class="block mb-2 font-semibold text-gray-700">上传模型</label>
        <input 
          class="w-full p-2 border rounded-lg" 
          type="file" 
          accept=".obj" 
          @change="handleUpload" 
        />
      </div>

      <!-- 操作说明 -->
      <div class="instructions mt-6">
        <h2 class="block font-semibold text-base text-gray-700 mb-4">操作说明</h2>
        <ul class="text-gray-600">
          <li class="mb-2">🔄 <strong>按住左键</strong> 旋转模型</li>
          <li class="mb-2">🤏 <strong>按住右键</strong> 拖动模型</li>
          <li class="mb-2">🔍 <strong>使用滚轮</strong> 缩放模型</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { markRaw } from 'vue' // 引入 markRaw
import { TresCanvas } from '@tresjs/core'
import { OrbitControls } from '@tresjs/cientos'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { MeshStandardMaterial } from 'three'
import api from '../api' // 导入 API

export default {
  name: "ThreeDViewer",
  components: {
    TresCanvas,
    OrbitControls
  },
  data() {
    return {
      presetModels: [], // 存储模型列表
      modelUrl: '', // 当前加载的模型 URL
      objModel: null // Three.js 加载的模型
    }
  },
  mounted() {
    this.fetchModels()
  },
  watch: {
    modelUrl(newUrl) {
      if (!newUrl) return
      const loader = new OBJLoader()
      loader.load(newUrl, (obj) => {
        const grayMaterial = new MeshStandardMaterial({ color: 0x808080 }) // 设定灰色材质
        obj.traverse((child) => {
          if (child.isMesh) {
            child.material = grayMaterial
          }
        })
        this.objModel = markRaw(obj) // **关键：使用 markRaw() 避免 Vue 代理 obj**
      })
    }
  },
  methods: {
    async fetchModels() {
      try {
        const response = await api.get_model_list()
        if (response.data.result) {
          // 解析模型列表
          this.presetModels = response.data.data.map((model) => {
            return {
              name: model, // 可以根据需要设置名字
              url: `/static/models/${model}` // 根据实际文件路径调整
            }
          })
        } else {
          console.error('获取模型列表失败:', response.data.message)
        }
      } catch (error) {
        console.error('API 请求失败:', error)
      }
    },
    handleUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.modelUrl = URL.createObjectURL(file) // 赋值给 modelUrl
      }
    },
    handlePresetSelect(event) {
      this.modelUrl = event.target.value // 更新 modelUrl
    }
  }
}

</script>



<style>
/* 页面整体布局 */
.canvas-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

/* 3D 画布区域 */
.canvas-wrapper {
  width: 800px;
  height: 600px;
  position: relative;
  overflow: hidden;
  background-color: white;
}

.fixed-canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

/* 右侧操作区域 */
.sidebar {
  width: 250px;
  padding: 20px;
  margin-left: 20px;
  background-color: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

/* 选择预置模型 */
.preset-area {
  margin-bottom: 20px;
}

/* 上传区域 */
.upload-area input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  cursor: pointer;
}

/* 操作说明 */
.instructions {
  font-size: 14px;
}

.instructions ul {
  line-height: 1.6;
}

.instructions li {
  display: flex;
  align-items: center;
}

.instructions li strong {
  font-weight: bold;
}
</style>

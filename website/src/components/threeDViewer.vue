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
        <!-- 添加网格 -->
        <!-- <TresGridHelper :args="[10, 20, '#888888', '#444444']" /> -->
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
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
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
      const fileExtension = newUrl.split('.').pop().toLowerCase()

      if (fileExtension === 'obj') {
        const loader = new OBJLoader()
        loader.load(newUrl, (obj) => {
          const grayMaterial = new MeshStandardMaterial({ color: 0x808080 })
          obj.traverse((child) => {
            if (child.isMesh) {
              child.material = grayMaterial
            }
          })
          this.objModel = markRaw(obj)
        })
      } else if (fileExtension === 'glb' || fileExtension === 'gltf') {
        const loader = new GLTFLoader()
        loader.load(newUrl, (gltf) => {
          this.objModel = markRaw(gltf.scene)
        })
      }
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
              name: model.replace(/\.(glb|gltf|obj)$/i, ''), // 去除扩展名
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
    handlePresetSelect(event) {
      this.modelUrl = event.target.value // 更新 modelUrl
    }
  }
}

</script>



<style src="../style/index.css">

</style>

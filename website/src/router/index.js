import { createRouter, createWebHistory } from 'vue-router';
import threeDViewer from '@/components/threeDViewer.vue';

const routes = [
  {
    path: '/',
    name: 'threeDViewer',
    component: threeDViewer
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Set the document title dynamically based on the route's meta title
router.beforeEach((to, from, next) => {
  document.title = '寻仙模型查看器';
  next();
});

export default router;


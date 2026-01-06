/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import { createRouter, createMemoryHistory } from 'vue-router'

// Components
import App from './App.vue'
import Notes from './components/Notes.vue'
import Prototype from './components/Prototype.vue'
import Create from './components/Create.vue'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'


const routes = [
  { path: '/notes:item_type:item_ref', name: 'notes', component: Notes, props: true },
  { path: '/prototype', name: 'prototype', component: Prototype },
  { path: '/create', name: 'create', component: Create }
];

// 2. Create the router instance
const router = createRouter({
  history: createMemoryHistory(), // Recommended HTML5 history mode
  routes
})

const app = createApp(App)
app.use(router)
registerPlugins(app)
app.mount('#app')

// Manually push the initial navigation for memory history
router.push('/prototype');
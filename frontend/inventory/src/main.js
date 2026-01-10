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
import BaseUnit from './components/BaseUnit.vue'
import Camera from './components/Camera.vue'
import OtherItems from './components/OtherItems.vue'
import CreateCamera from './components/CreateCamera.vue'
import CreateOtherItem from './components/CreateOtherItem.vue'
import AddMaintenanceTask from './components/AddMaintenanceTask.vue'
import AddNote from './components/AddNote.vue'
import UpdateOtherItem from './components/UpdateOtherItem.vue'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

const routes = [
  { path: '/notes:item_type:item_ref', name: 'notes', component: Notes, props: true },
  { path: '/prototype', name: 'prototype', component: Prototype },
  { path: '/create', name: 'create', component: Create },
  { path: '/create-camera:base_unit?', name: 'create-camera', component: CreateCamera, props: true},
  { path: '/base-unit:id:name:location:has_new_mast_bearing:has_new_feet:face_camera:license_plate_camera:widescreen_camera', name: 'base-unit', component: BaseUnit, props: true },
  { path: '/camera:id:name:camera_type:location:base_unit', name: 'camera', component: Camera, props: true },
  { path: '/other-items:id:name:location:base_unit', name: 'other-items', component: OtherItems, props: true },
  { path: '/create-other-item:base_unit?', name: 'create-other-item', component: CreateOtherItem, props: true },
  { path: '/update-other-item:name', name: 'update-other-item', component: UpdateOtherItem, props: true },
  { path: '/add-maintenance-task:item_type:item_ref', name: 'add-maintenance-task', component: AddMaintenanceTask, props: true },
  { path: '/add-note:item_type:item_ref', name: 'add-note', component: AddNote, props: true },
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
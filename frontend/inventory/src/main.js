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
import Prototype from './components/Prototype.vue'
import CreateBaseUnit from './components/CreateBaseUnit.vue'
import BaseUnit from './components/BaseUnit.vue'
import Camera from './components/Camera.vue'
import OtherItems from './components/OtherItems.vue'
import CreateCamera from './components/CreateCamera.vue'
import CreateOtherItem from './components/CreateOtherItem.vue'
import AddMaintenanceTask from './components/AddMaintenanceTask.vue'
import AddNote from './components/AddNote.vue'
import UpdateOtherItem from './components/UpdateOtherItem.vue'
import UpdateCamera from './components/UpdateCamera.vue'
import UpdateBaseUnit from './components/UpdateBaseUnit.vue'
import MastBearingReport from './components/MastBearingReport.vue'
import NewFeetReport from './components/NewFeetReport.vue'
import MaintItemsReport from './components/MaintItemsReport.vue'
import UpdateMaintenanceTask from './components/UpdateMaintenanceTask.vue'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

// Define routes
const routes = [
  { path: '/prototype', name: 'prototype', component: Prototype },
  { path: '/create-base-unit', name: 'create-base-unit', component: CreateBaseUnit },
  { path: '/update-base-unit:name:id:location:has_new_feet:has_new_mast_bearing', name: 'update-base-unit', component: UpdateBaseUnit, props: true },
  { path: '/create-camera:base_unit?', name: 'create-camera', component: CreateCamera, props: true},
  { path: '/update-camera:name', name: 'update-camera', component: UpdateCamera, props: true },
  { path: '/base-unit:id:name:location:has_new_mast_bearing:has_new_feet:face_camera:license_plate_camera:widescreen_camera', name: 'base-unit', component: BaseUnit, props: true },
  { path: '/camera:id:name:camera_type:location:base_unit', name: 'camera', component: Camera, props: true },
  { path: '/other-items:id:name:location:base_unit', name: 'other-items', component: OtherItems, props: true },
  { path: '/create-other-item:base_unit?', name: 'create-other-item', component: CreateOtherItem, props: true },
  { path: '/update-other-item:name', name: 'update-other-item', component: UpdateOtherItem, props: true },
  { path: '/add-maintenance-task:item_type:item_ref', name: 'add-maintenance-task', component: AddMaintenanceTask, props: true },
  { path: '/update-maintenance-task:id:description:last_done_date', name: 'update-maintenance-task', component: UpdateMaintenanceTask, props: true },
  { path: '/add-note:item_type:item_ref', name: 'add-note', component: AddNote, props: true },
  { path: '/mast-bearing-report', name: 'mast-bearing-report', component: MastBearingReport },
  { path: '/new-feet-report', name: 'new-feet-report', component: NewFeetReport },
  { path: '/maint-items-report', name: 'maint-items-report', component: MaintItemsReport },
];

// Create the router instance
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
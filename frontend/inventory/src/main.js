/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import { createRouter, createMemoryHistory } from 'vue-router'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

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
import SystemTestChecklist from './components/SystemTestChecklist.vue'
import SystemTestInfo from './components/SystemTestInfo.vue'
import AddCamera from './components/AddCamera.vue'
import AddOtherItem from './components/AddOtherItem.vue'
import HistoryReport from './components/HistoryReport.vue'
import AddIssue from './components/AddIssue.vue'
import Notes from './components/Notes.vue'
import Issues from './components/Issues.vue'
import MaintenanceTasks from './components/MaintenanceTasks.vue'
import IssueReportInfo from './components/IssueReportInfo.vue'
import IssueReport from './components/IssueReport.vue'
import NotesReportInfo from './components/NotesReportInfo.vue'
import NotesReport from './components/NotesReport.vue'
import ViewMaintenanceTasks from './components/ViewMaintenanceTasks.vue'
import ViewIssues from './components/ViewIssues.vue'
import Login from './components/Login.vue'
import ViewNotes from './components/ViewNotes.vue'


// Define routes
const routes = [
  { path: '/prototype', name: 'prototype', component: Prototype },
  { path: '/create-base-unit', name: 'create-base-unit', component: CreateBaseUnit },
  { path: '/update-base-unit:name:id:location', name: 'update-base-unit', component: UpdateBaseUnit, props: true },
  { path: '/create-camera:base_unit?', name: 'create-camera', component: CreateCamera, props: true},
  { path: '/add-camera:base_unit_name:base_unit_id', name: 'add-camera', component: AddCamera, props: true},
  { path: '/update-camera:name:lane:base_unit_name?', name: 'update-camera', component: UpdateCamera, props: true },
  { path: '/base-unit:id:name:location', name: 'base-unit', component: BaseUnit, props: true },
  { path: '/camera:id:name:lane:camera_type:location:base_unit', name: 'camera', component: Camera, props: true },
  { path: '/other-items:id:name:location:base_unit', name: 'other-items', component: OtherItems, props: true },
  { path: '/create-other-item:base_unit?', name: 'create-other-item', component: CreateOtherItem, props: true },
  { path: '/add-other-item:base_unit_name:base_unit_id', name: 'add-other-item', component: AddOtherItem, props: true},
  { path: '/update-other-item:name', name: 'update-other-item', component: UpdateOtherItem, props: true },
  { path: '/add-maintenance-task:item_type:item_ref:item_name', name: 'add-maintenance-task', component: AddMaintenanceTask, props: true },
  { path: '/view-maint-tasks:item_type:item_ref:item_name', name: 'view-maint-tasks', component: MaintenanceTasks, props: true },
  { path: '/view-maint-tasks-all', name: 'view-maint-tasks-all', component: ViewMaintenanceTasks },
  { path: '/update-maintenance-task:id:description:item_type:item_name', name: 'update-maintenance-task', component: UpdateMaintenanceTask, props: true },
  { path: '/add-note:item_type:item_ref:item_name', name: 'add-note', component: AddNote, props: true },
  { path: '/view-notes:item_type:item_ref:item_name', name: 'view-notes', component: Notes, props: true },
  { path: '/add-issue:item_type:item_ref:item_name', name: 'add-issue', component: AddIssue, props: true }, 
  { path: '/view-issues:item_type:item_ref:item_name', name: 'view-issues', component: Issues, props: true }, 
  { path: '/view-issues-all', name: 'view-issues-all', component: ViewIssues },
  { path: '/mast-bearing-report', name: 'mast-bearing-report', component: MastBearingReport },
  { path: '/new-feet-report', name: 'new-feet-report', component: NewFeetReport },
  { path: '/maint-items-report', name: 'maint-items-report', component: MaintItemsReport },
  { path: '/report-history:item_type:item_name', name: 'report-history', component: HistoryReport, props: true },
  { path: '/system-test-info', name: 'system-test-info', component: SystemTestInfo },
  { path: '/system-test-checklist:technician_name:base_unit:report_date', name: 'system-test-checklist', component: SystemTestChecklist, props: true },
  { path: '/issue-report-info', name: 'issue-report-info', component: IssueReportInfo },
  { path: '/issue-report:item_type:query_string:end_date:start_date?', name: 'issue-report', component: IssueReport, props: true },
  { path: '/notes-report-info', name: 'notes-report-info', component: NotesReportInfo },
  { path: '/notes-report:item_type:query_string:end_date:start_date?', name: 'notes-report', component: NotesReport, props: true },
  { path: '/view-notes-all', name: 'view-notes-all', component: ViewNotes },
  { path: '/login', name: 'login', component: Login },

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
router.push('/login');
<!--
This file is the vue component implementation for an other items detail screen.
 -->
<template>
  <div class="tools-menu-container">
    <v-row>
      <v-col style="padding-right: 4px; padding-left: 5px">
        <div class="tools-menu-right">
          <button @click="toggleViewsMenu" class="tools-button" aria-label="Settings menu">
            <img src="../assets/views.png" alt="Views Menu" class="button-image"/>
          </button>
          <div v-if="isViewsOpen" class="tools-dropdown">
              <ul>
              <li @click="selectViewsOption('Main')">Main</li>
              <li @click="selectViewsOption('Issues')">Issues</li>
              <li @click="selectViewsOption('Notes')">Notes</li>
              <li @click="selectViewsOption('MaintTasks')">Maint Tasks</li>
              </ul>
          </div>
        </div>
      </v-col>
      <v-col style="padding-right: 4px; padding-left: 0px">
        <div class="tools-menu-right">
          <button @click="toggleReportsMenu" class="tools-button" aria-label="Settings menu">
            <img src="../assets/report_icon.jpg" alt="Reports Menu" class="button-image" />
          </button>

          <div v-if="isReportsOpen" class="tools-dropdown">
              <ul>
              <li @click="selectReportsOption('MastBearing')">Has New Mast Bearing</li>
              <li @click="selectReportsOption('NewFeet')">Has New Feet</li>
              <li @click="selectReportsOption('MaintItems')">Has Expired Maintenance Tasks</li>
              <li @click="selectReportsOption('IssueReport')">Issue Report</li>
              <li @click="selectReportsOption('NotesReport')">Notes Report</li>
              </ul>
          </div>
        </div>
      </v-col>
      <v-col style="padding-right: 4px; padding-left: 0px">
        <div class="tools-menu-right">
          <button @click="toggleChecklistsMenu" class="tools-button" aria-label="Settings menu">
            <img src="../assets/checkbox_icon.png" alt="Checklists Menu" class="button-image"/>
          </button>
          <div v-if="isChecklistsOpen" class="tools-dropdown">
              <ul>
              <li @click="selectChecklistsOption('SystemTestChecklist')">System Test Checklist</li>
              </ul>
          </div>
        </div>
      </v-col>
      <v-col>
        <v-spacer></v-spacer>
      </v-col>
    </v-row>
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Issues View
        </div>
      </v-row>  
    </v-container>
    <v-container  class="table-container">
      <v-row>
        <v-data-table
          :headers="issueHeaders"
          :items="getFilteredItems"
          :search="issueSearch"
          item-value="description"
          class="elevation-1"
          :key="issueKey"
          @dblclick:row="navigateToDetails"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="issueSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <v-select
              v-model="itemType"
              :items="itemTypes"
              dense
              hide-details
            ></v-select>
            <v-spacer></v-spacer>
          </template>
          <!-- Use the specific slot name 'item.actions' -->
          <template v-slot:item.actions="{ item }">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="deleteIssue(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <v-container class="table-container">
      <div class="d-flex justify-center align-center" style="padding-top: 20px;">
        <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
      </div>
    </v-container>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import ConfirmDialog from './ConfirmDialog.vue';
  import api, {activity_log, fetchBaseUnitById, fetchCameraById, fetchOtherItemById} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const isReportsOpen = ref(false);
  const isChecklistsOpen = ref(false);
  const isViewsOpen = ref(false);
  const errorDialog = ref(null);
  const loading = ref(true);
  const router = useRouter();
  const route = useRoute();
  const issueTable = ref([]);
  const issueSearch = ref('');
  const issueKey = ref(0);
  const confirmDialog = ref(null);
  const itemType = ref('ALL');
  const itemTypes = ref([]);
  
  // Table headers
  const issueHeaders = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Item Type', value: 'item_type' , sortable: true},
    {title: 'Item Name', value: 'item_name' , sortable: true},
    {title: 'Date', value: 'date' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  // fetch the user information when params change
  watch(
    // fetch the user information when params change
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN ViewIssues.watch.refresh newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      await fetchIssues();
      await fetchItemTypes();
      issueKey.value += 1;
      console.log("OUT ViewIssues.watch.refresh");
    }
  );

  // Initialize data on mount of component
  onMounted(async () => {
    console.log('IN ViewIssues.onMounted');
    await fetchIssues();
    await fetchItemTypes();
    issueKey.value += 1;
    document.addEventListener('click', handleClickOutside);
    console.log('OUT ViewIssues.onMounted');
  });

  // Navigate to base units detail screen on double-click.
  const navigateToDetails = async (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToDetails: " + JSON.stringify(item));

    event.preventDefault();

    if(item.item_type === "Base Unit"){
      let baseUnit = await fetchBaseUnitById(item.item_ref);
      console.log("baseUnit=" + JSON.stringify(baseUnit))
      let face_cameras = [];
      let license_plate_cameras = [];
      let windscreen_cameras = [];
      if ('face_cameras' in baseUnit && baseUnit.face_cameras != null) {
        face_cameras = baseUnit.face_cameras;
      }
      let license_plate_camera = [];
      if ('license_plate_cameras' in baseUnit && baseUnit.license_plate_cameras != null) {
        license_plate_cameras = baseUnit.license_plate_cameras;
      }
      let windscreen_camera = [];
      if ('windscreen_cameras' in baseUnit && baseUnit.windscreen_cameras != null) {
        windscreen_cameras = baseUnit.windscreen_cameras;
      }

      router.push(
        {
          name: 'base-unit',
          query: { face_cameras: face_cameras, license_plate_cameras: license_plate_cameras, windscreen_cameras: windscreen_cameras },
          params: {id: baseUnit.id, name: baseUnit.name, location: baseUnit.location}
        });
    } else if(item.item_type === "Camera") {
      let camera = await fetchCameraById(item.item_ref)
      let camera_location = -1;
      if ('location' in camera && camera.location != null) {
        camera_location = camera.location;
      }
      let camera_bu = "NONE";
      if ('base_unit' in camera && camera.base_unit != null) {
        camera_bu = camera.base_unit;
      }

      console.log("camera_location=" + camera_location + "; camera_bu=" + camera_bu);
      router.push({name: 'camera', params: {id: camera.id, name: camera.name, lane: camera.lane, location: camera_location, base_unit: camera_bu, camera_type: camera.type}}).catch(failure => {
        console.log('An unexpected navigation failure occurred:', failure);
      });
    } else if(item.item_type === "Other Item") {
      let otherItem = await fetchOtherItemById(item.item_ref)
      let other_location = -1;
      if ('location' in otherItem && otherItem.location != null) {
        other_location = otherItem.location;
      }
      let other_bu = "NONE";
      if ('base_unit' in otherItem && otherItem.base_unit != null) {
        other_bu = otherItem.base_unit;
      }

      router.push({name: 'other-items', params: {id: otherItem.id, name: otherItem.name, location: other_location, base_unit: other_bu}}).catch(failure => {
        console.log('An unexpected navigation failure occurred:', failure);
      });
    }
    console.log("OUT navigateToDetails");
  }

  // Remove document listener when component is unmounted.
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
  });

  const getFilteredItems = computed(() => {
    if (!itemType.value || itemType.value === 'ALL') return issueTable.value;
    return issueTable.value.filter(row => {
      return row.item_type === itemType.value;
    });
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN ViewIssues.goBack");
    router.back();
    console.log("OUT ViewIssues.goBack");
  };

  // Toggle the reports menu.
  const toggleReportsMenu = () => {
    isReportsOpen.value = !isReportsOpen.value;
  };

  // Toggle the checklists menu.
  const toggleChecklistsMenu = () => {
    isChecklistsOpen.value = !isChecklistsOpen.value;
  };

  // Toggle the views menu.
  const toggleViewsMenu = () => {
    isViewsOpen.value = !isViewsOpen.value;
  };
  
  // Select an option from the reports menu dropdown.
  const selectReportsOption = (option) => {
    console.log('Selected:' + option);
    isReportsOpen.value = false; // Close menu after selection
    // Emit event to parent component if needed, e.g., emit('select', option)
    if(option === "MastBearing"){
      router.push({name: "mast-bearing-report"});
    } else if (option === "NewFeet") {
      router.push({name: "new-feet-report"});
    } else if (option === "MaintItems") {
      router.push({name: "maint-items-report"});
    } else if (option === "IssueReport") {
      router.push({name: "issue-report-info"});
    } else if (option === "NotesReport") {
      router.push({name: "notes-report-info"});
    }

  };

  const selectChecklistsOption = (option) => {
    console.log("IN Prototype.selectChecklistsOption");
    console.log('Selected:' + option);
    isChecklistsOpen.value = false; // Close menu after selection
    if(option == 'SystemTestChecklist'){
      router.push({name: "system-test-info"});
    }
    console.log("OUT Prototype.selectChecklistsOption");
  };

  const selectViewsOption = (option) => {
    console.log("IN Prototype.selectViewsOption");
    console.log('Selected:' + option);
    isViewsOpen.value = false; // Close menu after selection
    if(option == 'Main'){
      router.push({name: "prototype"});
    } else if(option == 'Issues') {
      router.push({name: "view-issues-all"});
    } else if(option == 'MaintTasks') {
      router.push({name: "view-maint-tasks-all"});
    } else if(option == 'Notes') {
      router.push({name: "view-notes-all"});
    }

    console.log("OUT Prototype.selectViewsOption");
  };

  // Close the menu when clicking outside
  const handleClickOutside = (event) => {
    if (!event.target.closest('.tools-menu-container')) {
        isReportsOpen.value = false;
        isChecklistsOpen.value = false;
    }
  };


  // Delete an issue from the database
  const deleteIssue = async (item) => {
    console.log("IN  ViewIssues.deleteIssue item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this issue?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
        headers: {
            'Content-Type': 'application/json'
        }
      };
      const requestBody = {
        id: item.id,
      };
      try {
          const response = await api.post('/delete-issue', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting task:' + e,
            { color: 'red lighten-3' }
          );
      }
      console.log('Task deleted!');
      await fetchIssues();
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT  ViewIssues.deleteIssue");
  };

  // Retrieve issues from the database through a REST call.
  const fetchIssues = async () => {
    console.log("IN ViewIssues.fetchIssues");

    const config = {
      headers: {
        'Content-Type': 'application/json'
      }
    };
    try {
        const response = await api.get('/get-all-issues', config);
        issueTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
          'Confirm Error',
          'Error fetching data:' + e,
          { color: 'red lighten-3' }
        );
    }
    console.log("OUT ViewIssues.fetchIssues");
  };

  // Retrieve item type values.
  const fetchItemTypes= async () => {
    const config = {
      headers: {
          'Content-Type': 'application/json'
      }
    };

    try {
      const response = await api.get('/get-item-types', config);
      itemTypes.value = response.data;
      itemTypes.value.push('ALL')
      loading.value = false;
    } catch (e) {
      loading.value = false;
      const result = await errorDialog.value.open(
          'Confirm Error',
          'Error fetching data:' + e,
          { color: 'red lighten-3' }
        );
    }
  };
  
</script>

<style>
  .v-data-table {
    border: 1px solid green;
  }

  /* Set header background color */
  .theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr > th {
    background: var(--v-primary-base); /* Use a CSS variable for theme color */
  }

  /* Set alternating row colors (striped table) */
  .v-table tbody tr:nth-child(odd) {
    background-color: #f5f5f5; /* Light grey for odd rows */
  }
  .v-table thead th {
    background-color:  #F5F5DC; /* White for even rows */
  }
  .v-table tbody tr:nth-child(even) {
    background-color: #ffffff; /* White for even rows */
  }
</style>
<style scoped>
  .my-division {
    padding-top: 15px;
    padding-bottom: 15px;
    padding-left: 100px;
  }
  .tools-menu-container {
    position: absolute;
    top: 0; /* Aligns to the top edge of the parent */
    right: 0; /* Aligns to the right edge of the parent */
    display: inline-block;
  }

  .tools-button {
    /* background-color: lightgray;  Example styling */
    color: white;
    padding: 0.5px .5px;
    border: none;
    cursor: pointer;
  }

  .tools-dropdown {
    position: absolute;
    right: 0;
    background-color: #f9f9f9;
    min-width: 320px;
    box-shadow: 0px 1px 1px 0px rgba(0,0,0,0.2);
    z-index: 1;
  }

  .tools-dropdown ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  .tools-dropdown li {
    padding: 12px 16px;
    cursor: pointer;
  }

  .tools-dropdown li:hover {
    background-color: #ddd;
  }
  .tools-menu-right {
    margin-left: auto; /* Pushes this element and everything after it to the far right */
    padding-right: 1px;
    padding-top: 10px;
  }
  .button-image {
    width: 20px; /* Set a specific width */
    height: auto; /* Maintain aspect ratio */
  }

  .detail-container {
    border: 1px solid green;
    width: 70%;
  }

  .detail-sheet { 
    width: 95%;
  }

  .table-container { 
    width: 100%;
  }

  .outer-div {
    width: 80%;
    padding-top: 30px;
    padding-left: 10%;
  }

  .pre-wrap-cell {
    white-space: pre-wrap; /* or pre-line */
  }

   /* Specific styles for screens smaller than 600px */
  @media (max-width: 600px) {
    .detail-container {
      border: 1px solid green;
      width: 100%; /* Take up full width on mobile */
      padding: 0 1em; /* Add some padding */
    }
    .detail-sheet { 
      width: 99%
    }
    .table-container { 
      width: 100%
    }
    .outer-div {
      width: 100%;
    }
  }
</style>
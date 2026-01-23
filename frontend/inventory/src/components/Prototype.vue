<!--
This file is the vue component implementation for the main screen that lists
all of the base units, cameras, and other items. There is also a dropdown on the 
upper right for generating reports.
 -->
<template>
  <div class="tools-menu-container">
    <v-row>
      <v-col style="padding-right: 5px;">
        <div class="tools-menu-right">
          <button @click="toggleReportsMenu" class="tools-button" aria-label="Settings menu">
            <img src="../assets/report_icon.jpg" alt="Description of action" class="button-image" />
              <!-- You can use a settings icon here, e.g., a gear symbol (⚙) or an SVG -->
              <!-- ⚙ Settings -->
          </button>

          <div v-if="isReportsOpen" class="tools-dropdown">
              <ul>
              <li @click="selectReportsOption('MastBearing')">Has New Mast Bearing</li>
              <li @click="selectReportsOption('NewFeet')">Has New Feet</li>
              <li @click="selectReportsOption('MaintItems')">Has Expired Maintenance Tasks</li>
              </ul>
          </div>
        </div>
      </v-col>
      <v-col style="padding-left: 0px">
        <div class="tools-menu-right">
          <button @click="toggleChecklistsMenu" class="tools-button" aria-label="Settings menu">
            <img src="../assets/checkbox_icon.png" alt="Description of action" class="button-image"/>
              <!-- You can use a settings icon here, e.g., a gear symbol (⚙) or an SVG -->
              <!-- ⚙ Settings -->
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
          Base Units
        </div>
      </v-row>
      <v-row>
        <!-- Data Table -->
        <v-data-table
          :headers="headers"
          :items="baseUnitsTable"
          :search="baseUnitSearch"
          item-value="name"
          class="elevation-1"
          :key="baseUnitsKey"
          @dblclick:row="navigateToDetails"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="baseUnitSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="createBaseUnit">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
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
                <v-list-item @click="deleteBaseUnit(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateBaseUnit(item)">
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
                <v-list-item @click="baseUnitHistoryReport(item)">
                  <v-list-item-title>History</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          Cameras
        </div>
      </v-row>
      <v-row>
        <!-- Data Table -->
        <v-data-table
          :headers="camerasHeaders"
          :items="camerasTable"
          :search="cameraSearch"
          item-value="name"
          class="elevation-1"
          :key="cameraKey"
          @dblclick:row="navigateToCameraDetails"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="cameraSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="createCamera">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
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
                <v-list-item @click="deleteCamera(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateCamera(item)">
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
                <v-list-item @click="cameraHistoryReport(item)">
                  <v-list-item-title>History</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          Other Items
        </div>
      </v-row>
      <v-row>
        <!-- Data Table -->
        <v-data-table
          :headers="otherItemsHeaders"
          :items="otherItemsTable"
          :search="otherSearch"
          item-value="name"
          class="elevation-1"
          :key="otherKey"
          @dblclick:row="navigateToOtherItemsDetails"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="otherSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="createOtherItem">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
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
                <v-list-item @click="deleteOtherItem(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateOtherItem(item)">
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
                <v-list-item @click="otherItemHistoryReport(item)">
                  <v-list-item-title>History</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, watch, onUnmounted, computed } from 'vue';
  import { VDataTable } from 'vuetify/components';
  import { useRouter, useRoute } from 'vue-router';
  import api, {activity_log} from "../api";
  import ConfirmDialog from './ConfirmDialog.vue';
  import ErrorDialog from './ErrorDialog.vue';
  
  // Data
  const isReportsOpen = ref(false);
  const isChecklistsOpen = ref(false);
  const baseUnitSearch = ref('');
  const cameraSearch = ref('');
  const otherSearch = ref('');
  const baseUnitsTable = ref([]);
  const camerasTable = ref([]);
  const otherItemsTable = ref([]);

  const loading = ref(true);
  const router = useRouter();
  const route = useRoute();
  const confirmDialog = ref(null);
  const baseUnitsKey = ref(0);
  const otherKey = ref(0);
  const cameraKey = ref(0);
  const errorDialog = ref(null);

  // Table headers
  const headers = ref([
    {title: 'Name', align: 'start', sortable: true, value: 'name', class: 'blue lighten-5'},
    {title: 'Location', value: 'location', sortable: true },
    {title: 'Face Cameras', value: 'face_cameras_str' , sortable: true},
    {title: 'License Plate Cameras', value: 'license_plate_cameras_str', sortable: true},
    {title: 'Widescreen Cameras', value: 'widescreen_cameras_str', sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const camerasHeaders = ref([
    {title: 'Name', align: 'start', sortable: true, value: 'name', class: 'blue lighten-5'},
    {title: 'Type', value: 'type', sortable: true },
    {title: 'Base Unit', value: 'base_unit' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const otherItemsHeaders = ref([
    {title: 'Name', align: 'start', sortable: true, value: 'name', class: 'blue lighten-5'},
    {title: 'Base Unit', value: 'base_unit' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  // fetch the user information when params change
  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN Prototype.watch.refresh");
      fetchBaseUnits();
      baseUnitsKey.value += 1;
      fetchCameras();
      cameraKey.value += 1;
      fetchOtherItems();
      otherKey.value += 1;
      console.log("OUT Prototype.watch.refresh");
    }
  );

  // Initialize data when component is mounted
  onMounted(async () => {
    console.log('IN Prototype.onMounted');
    fetchBaseUnits();
    baseUnitsKey.value += 1;
    fetchCameras();
    cameraKey.value += 1;
    fetchOtherItems();
    otherKey.value += 1;
    console.log('Before');
    document.addEventListener('click', handleClickOutside);
    console.log('After');
    console.log('OUT Prototype.onMounted');
  });

  // Remove document listener when component is unmounted.
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
  });

  // Navigate to base units detail screen on double-click.
  const navigateToDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToDetails: " + JSON.stringify(item));

    event.preventDefault();

    let face_cameras = [];
    let license_plate_cameras = [];
    let widescreen_cameras = [];
    if ('face_cameras' in item && item.face_cameras != null) {
      face_cameras = item.face_cameras;
    }
    let license_plate_camera = [];
    if ('license_plate_cameras' in item && item.license_plate_cameras != null) {
      license_plate_cameras = item.license_plate_cameras;
    }
    let widescreen_camera = [];
    if ('widescreen_cameras' in item && item.widescreen_cameras != null) {
      widescreen_cameras = item.widescreen_cameras;
    }

    router.push(
      {
        name: 'base-unit',
        query: { face_cameras: face_cameras, license_plate_cameras: license_plate_cameras, widescreen_cameras: widescreen_cameras },
        params: {id: item.id, name: item.name, location: item.location, has_new_mast_bearing: item.has_new_mast_bearing, has_new_feet: item.has_new_feet}
      });
    console.log("OUT navigateToDetails");
  }

  // Navigate to camera details screen on double-click.
  const navigateToCameraDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToCameraDetails: " + JSON.stringify(item));

    event.preventDefault();
    let camera_location = -1;
    if ('location' in item && item.location != null) {
      camera_location = item.location;
    }
    let camera_bu = "NONE";
    if ('base_unit' in item && item.base_unit != null) {
      camera_bu = item.base_unit;
    }

    console.log("camera_location=" + camera_location + "; camera_bu=" + camera_bu);
    router.push({name: 'camera', params: {id: item.id, name: item.name, location: camera_location, base_unit: camera_bu, camera_type: item.type}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToCameraDetails");
  }

  // Navigate to other items detail screen on double-click.
  const navigateToOtherItemsDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToOtherItemsDetails: " + JSON.stringify(item));

    event.preventDefault();
    let other_location = -1;
    if ('location' in item && item.location != null) {
      other_location = item.location;
    }
    let other_bu = "NONE";
    if ('base_unit' in item && item.base_unit != null) {
      other_bu = item.base_unit;
    }

    router.push({name: 'other-items', params: {id: item.id, name: item.name, location: other_location, base_unit: other_bu}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToOtherItemsDetails");
  }

  // Toggle the reports menu.
  const toggleReportsMenu = () => {
    isReportsOpen.value = !isReportsOpen.value;
  };

  // Toggle the reports menu.
  const toggleChecklistsMenu = () => {
    isChecklistsOpen.value = !isChecklistsOpen.value;
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

  // Close the menu when clicking outside
  const handleClickOutside = (event) => {
    if (!event.target.closest('.tools-menu-container')) {
        isReportsOpen.value = false;
        isChecklistsOpen.value = false;
    }
  };

  // Create a base unit object in the database.
  const createBaseUnit = () => {
    console.log("IN createBaseUnit");
    router.push({name: 'create-base-unit'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createBaseUnit");
  }

  // Delete a base unit object from the database.
  const deleteBaseUnit = async (item) => {
    console.log("IN deleteBaseUnit item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete the base unit ' + item.name + '?',
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
        face_cameras: item.face_cameras,
        license_plate_cameras: item.license_plate_cameras,
        widescreen_cameras: item.widescreen_cameras
      };
      try {
          const response = await api.post('/delete-base-unit', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting data:' + e,
            { color: 'red lighten-3' }
          );
      }
      fetchOtherItems();
      fetchBaseUnits();
      fetchCameras();
      console.log('Other Item deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteOtherItem");
  };

  // Update.  base unit object.
  const updateBaseUnit = (item) => {
    console.log("IN updateBaseUnit");
    router.push({name: 'update-base-unit', params: {name: item.name, id: item.id, location: item.location, has_new_feet: item.has_new_feet, has_new_mast_bearing: item.has_new_mast_bearing}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT updateBaseUnit");
  };

  const baseUnitHistoryReport = (item) => {
    console.log("IN baseUnitHistoryReport name=" + item.name);
    router.push({name: 'report-history', params: {item_type: 'Base Unit', item_name: item.name}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT baseUnitHistoryReport");
  }

  // Create a camera object in the database.
  const createCamera = () => {
    console.log("IN createCamera");
    router.push({name: 'create-camera'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createCamera");
  }

  // Delete a camera object from the database.
  const deleteCamera = async (item) => {
    console.log("IN deleteCamera item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete the camera' + item.name + '?',
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
        name: item.name,
        type: item.type,
        base_unit: item.base_unit
      };
      try {
          const response = await api.post('/delete-camera', requestBody, config);
          loading.value = false;
          activity_log('Camera', item.name, 'Removed from Base Unit ' + item.base_unit + ' and deleted from database');
          activity_log('Base Unit', item.base_unit, 'Removed Camera ' + item.name + ' from Base Unit ' + item.base_unit + ' and deleted from database');
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting camera:' + e,
            { color: 'red lighten-3' }
          );
      }
      fetchCameras();
      fetchBaseUnits();
      console.log('Camera deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteCamera");
  };
  const updateCamera = (item) => {
    console.log("IN updateCamera item=" + JSON.stringify(item));
    router.push({name: 'update-camera', params: {name: item.name, base_unit_name: item.base_unit}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT updateCamera");
  };

  const cameraHistoryReport = (item) => {
    console.log("IN cameraHistoryReport name=" + item.name);
    router.push({name: 'report-history', params: {item_type: 'Camera', item_name: item.name}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT cameraHistoryReport");
  }

  // Create an other item in the database.
  const createOtherItem = () => {
    console.log("IN createOtherItem");
    router.push({name: 'create-other-item'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createOtherItem");
  }

  // Delete an other item from the database.
  const deleteOtherItem = async (item) => {
    console.log("IN deleteOtherItem item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this other item?',
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
          const response = await api.post('/delete-other-item', requestBody, config);
          loading.value = false;
          activity_log('Other Item', item.name, 'Removed from Base Unit ' + item.base_unit + ' and deleted from database');
          activity_log('Base Unit', item.base_unit, 'Removed Other Item ' + item.name + ' from Base Unit ' + item.base_unit + ' and deleted from database');
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting other item:' + e,
            { color: 'red lighten-3' }
          );
      }
      fetchOtherItems();
      fetchBaseUnits();
      console.log('Other Item deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteOtherItem");
  };

  // Update an other item
  const updateOtherItem = (item) => {
    console.log("IN updateOtherItem");
    router.push({name: 'update-other-item', params: {name: item.name}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT updateOtherItem");
  };

  const otherItemHistoryReport = (item) => {
    console.log("IN otherItemHistoryReport");
    router.push({name: 'report-history', params: {item_type: 'Other Item', item_name: item.name}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT otherItemHistoryReport");
  }

  // Retrieve base units from the database.
  const fetchBaseUnits = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-base-units', config)
        const target_bu = response.data;
        baseUnitsTable.value = target_bu;
        baseUnitsTable.value.forEach(bu => {
          if('face_cameras' in bu && bu.face_cameras != null){
            bu.face_cameras_str = bu.face_cameras.join(', ');
          } else {
            bu.face_cameras_str = "";
          }
          if('license_plate_cameras' in bu && bu.license_plate_cameras != null){
            bu.license_plate_cameras_str = bu.license_plate_cameras.join(', ');
          } else {
            bu.license_plate_cameras_str = "";
          }
          if('widescreen_cameras' in bu && bu.widescreen_cameras != null){
            bu.widescreen_cameras_str = bu.widescreen_cameras.join(', ');
          } else {
            bu.widescreen_cameras_str = "";
          }
        });

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

  // Retrieve cameras from the database.
  const fetchCameras = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    try {
        const response = await api.get('/get-cameras', config);
        camerasTable.value = response.data;
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

  // Retrieve other items from the database.
  const fetchOtherItems = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-other-items', config);
        otherItemsTable.value = response.data;
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
    border: 5px solid green;
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
  .table-container { 
    width: 80%;
    padding-top: 30px;
  }
  .outer-div {
    width: 100%;
    padding-top: 30px;
  }
  /* Specific styles for screens smaller than 600px */
  @media (max-width: 600px) {
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
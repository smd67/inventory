<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 150px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Base Units
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error">
    <v-container>
      <!-- Data Table -->
      <v-data-table
        :headers="headers"
        :items="baseUnitsTable"
        :search="baseUnitSearch"
        item-value="name"
        class="elevation-1"
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
              <v-list-item @click="showNotes(item)">
                <v-list-item-title>Show Notes</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 150px;">
      Cameras
    </div>
    <v-container>
      <!-- Data Table -->
      <v-data-table
        :headers="camerasHeaders"
        :items="camerasTable"
        :search="cameraSearch"
        item-value="name"
        class="elevation-1"
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
              <v-list-item @click="showNotes(item)">
                <v-list-item-title>Show Notes</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 150px;">
      Other Items
    </div>
    <v-container>
      <!-- Data Table -->
      <v-data-table
        :headers="otherItemsHeaders"
        :items="otherItemsTable"
        :search="otherSearch"
        item-value="name"
        class="elevation-1"
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
              <v-list-item @click="showNotes(item)">
                <v-list-item-title>Show Notes</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
  </div>
  <div v-else class="error-banner" style="color: red;">
    {{ error }}
  </div>
</template>

<script setup>
  import { ref, onMounted, watch } from 'vue';
  import { VDataTable } from 'vuetify/components';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";

  const baseUnitSearch = ref('');
  const cameraSearch = ref('');
  const otherSearch = ref('');
  const baseUnitsTable = ref([]);
  const camerasTable = ref([]);
  const otherItemsTable = ref([]);
  const error = ref(null);
  const loading = ref(true);
  const router = useRouter();
  const route = useRoute();

  const headers = ref([
    {title: 'Name', align: 'start', sortable: true, value: 'name', class: 'blue lighten-5'},
    {title: 'Location', value: 'location', sortable: true },
    {title: 'Face Camera', value: 'face_camera' , sortable: true},
    {title: 'License Plate Camera', value: 'license_plate_camera', sortable: true},
    {title: 'Widescreen Camera', value: 'widescreen_camera', sortable: true},
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
    () => route.params.id,
    async refresh => {
      fetchBaseUnits();
      fetchCameras();
      fetchOtherItems();
    }
  );

  onMounted(async () => {
    console.log('IN onMounted');
    fetchBaseUnits();
    fetchCameras();
    fetchOtherItems();
    console.log('OUT onMounted');
  });

  const showNotes = (item) => {
    console.log("IN showNotes id=" + item.id);
    router.push({name: 'notes', params: {item_type: 'BASE_UNIT', item_ref: item.id}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT showNotes");
  }


  const navigateToDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToDetails: " + JSON.stringify(item));

    event.preventDefault();

    let face_camera = "NONE";
    if ('face_camera' in item && item.face_camera != null) {
      face_camera = item.face_camera;
    }
    let license_plate_camera = "NONE";
    if ('license_plate_camera' in item && item.license_plate_camera != null) {
      license_plate_camera = item.license_plate_camera;
    }
    let widescreen_camera = "NONE";
    if ('widescreen_camera' in item && item.widescreen_camera != null) {
      widescreen_camera = item.widescreen_camera;
    }

    router.push({name: 'base-unit', params: {id: item.id, name: item.name, location: item.location, has_new_mast_bearing: item.has_new_mast_bearing, has_new_feet: item.has_new_feet, face_camera: face_camera, license_plate_camera: license_plate_camera, widescreen_camera: widescreen_camera}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToDetails");
  }

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

  const createBaseUnit = () => {
    console.log("IN createBaseUnit");
    router.push({name: 'create'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createBaseUnit");
  }

  const createCamera = () => {
    console.log("IN createCamera");
    router.push({name: 'create-camera'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createCamera");
  }

  const createOtherItem = () => {
    console.log("IN createOtherItem");
    router.push({name: 'create-other-item'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createOtherItem");
  }

  const fetchBaseUnits = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-base-units/', config);
        baseUnitsTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        error.value = 'Error fetching data:' + e;
    }
  };

const fetchCameras = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-cameras/', config);
        camerasTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        error.value = 'Error fetching data:' + e;
    }
  };
  const fetchOtherItems = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-other-items/', config);
        otherItemsTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        error.value = 'Error fetching data:' + e;
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
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
        :search="search"
        item-value="name"
        class="elevation-1"
      >
        <!-- If you still want the default pagination controls alongside the search -->
        <template v-slot:footer.prepend>
          <v-text-field
            v-model="search"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            density="compact"
            variant="outlined"
            bg-color="#f5f5f5"
            hide-details
            class="flex-grow-1 mr-4"
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn color="primary" dark small class="ma-2" @click="createNewItem">
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
        :search="search"
        item-value="name"
        class="elevation-1"
      >
        <!-- If you still want the default pagination controls alongside the search -->
        <template v-slot:footer.prepend>
          <v-text-field
            v-model="search"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            density="compact"
            variant="outlined"
            bg-color="#f5f5f5"
            hide-details
            class="flex-grow-1 mr-4"
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn color="primary" dark small class="ma-2" @click="createNewItem">
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
        :search="search"
        item-value="name"
        class="elevation-1"
      >
        <!-- If you still want the default pagination controls alongside the search -->
        <template v-slot:footer.prepend>
          <v-text-field
            v-model="search"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            density="compact"
            variant="outlined"
            bg-color="#f5f5f5"
            hide-details
            class="flex-grow-1 mr-4"
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn color="primary" dark small class="ma-2" @click="createNewItem">
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
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { VDataTable } from 'vuetify/components';
  import { useRouter } from 'vue-router';

  const search = ref('')
  const baseUnitsTable = ref([]);
  const camerasTable = ref([]);
  const otherItemsTable = ref([]);
  const error = ref(null);
  const loading = ref(true);
  const router = useRouter();
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

  const createNewItem = () => {
    console.log("IN createNewItem");
    router.push({name: 'create'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createNewItem");
  }

  const fetchBaseUnits = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-base-units/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await axios.get(apiUrl, config);
        baseUnitsTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        error.value = 'Error fetching data:' + e;
    }
  };

const fetchCameras = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-cameras/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await axios.get(apiUrl, config);
        camerasTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        error.value = 'Error fetching data:' + e;
    }
  };
  const fetchOtherItems = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-other-items/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await axios.get(apiUrl, config);
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
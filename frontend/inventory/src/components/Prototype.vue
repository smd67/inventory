<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 120px;">
    Asset Tracker
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error">
    <v-container>
      <!-- Data Table -->
      <v-data-table
        :headers="headers"
        :items="inventoryTable"
        :search="search"
        item-value="id"
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
  import { isNavigationFailure, NavigationFailureType } from 'vue-router';

  const search = ref('')
  const inventoryTable = ref([]);
  const error = ref(null);
  const loading = ref(true);
  const router = useRouter();
  const headers = ref([
    {title: 'ID', align: 'start', sortable: true, value: 'id', class: 'blue lighten-5'},
    {title: 'Location', value: 'location', sortable: true },
    {title: 'New Feet?', value: 'has_new_feet', sortable: true},
    {title: 'New Mast Bearing?', value: 'has_new_mast_bearing', sortable: true},
    {title: 'With Face Camera', value: 'together_with_face_camera' , sortable: true},
    {title: 'With License Plate Camera', value: 'together_with_license_plate_camera', sortable: true},
    {title: 'With Widescreen Camera', value: 'together_with_widescreen_camera', sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  onMounted(async () => {
    console.log('IN onMounted');
    fetchInventory();
    console.log('OUT onMounted');
  });

  const showNotes = (item) => {
    console.log("IN showNotes id=" + item.id);
    router.push({name: 'notes', params: {id: item.id}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT showNotes");
  }

  const fetchInventory = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-inventory/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await axios.get(apiUrl, config);
        inventoryTable.value = response.data;
        console.log("table=" + JSON.stringify(inventoryTable))
        loading.value = false;
    } catch (e) {
        loading.value = false;
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
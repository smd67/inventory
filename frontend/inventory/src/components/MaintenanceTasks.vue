<!--
This file is the vue component implementation for an other items detail screen.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Maintenance Tasks for {{ itemName }}
        </div>
      </v-row>  
    </v-container>
    <v-container  class="table-container">
      <v-row>
        <v-data-table
          :headers="maintHeaders"
          :items="maintTable"
          :search="maintSearch"
          item-value="description"
          class="elevation-1"
          :key="maintKey"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="maintSearch"
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
            <v-btn color="primary" dark small class="ma-2" @click="addMaintTask">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
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
                <v-list-item @click="deleteMaintTask(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateMaintTask(item)">
                  <v-list-item-title>Update</v-list-item-title>
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
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import ConfirmDialog from './ConfirmDialog.vue';
  import api, {activity_log} from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const errorDialog = ref(null);
  const loading = ref(true);
  const itemRef = ref(null);
  const itemType = ref(null);
  const itemName = ref(null);
  const router = useRouter();
  const route = useRoute();
  const maintTable = ref([]);
  const maintSearch = ref('');
  const maintKey = ref(0);
  const confirmDialog = ref(null);
  
  // Table headers
  const maintHeaders = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Last Done', value: 'last_done_date' , sortable: true},
    {title: 'Due Date', value: 'due_date' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  // Properties passed in to component
  const props = defineProps({
    item_ref: {
      type: Number,
      default: "",
    },
    item_type: {
      type: String,
      default: "",
    },
    item_name: {
      type: String,
      default: "",
    }
  });
  
  // fetch the user information when params change
  watch(
    // fetch the user information when params change
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN MaintenanceTasks.watch.refresh newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      if((oldFullPath.includes("/prototype") || oldFullPath.includes("/base-unit")) && newFullPath.includes("/view-maint-tasks")){
        itemRef.value = props.item_ref;
        itemType.value = props.item_type;
        itemName.value = props.item_name;
        fetchMaintTasks();
        maintKey.value += 1;
      } else if(oldFullPath.includes("/add-maintenance-task") && newFullPath.includes("/view-maint-tasks")){ 
        fetchMaintTasks();
        maintKey.value += 1;
      } else if(oldFullPath.includes("/update-maintenance-task") && newFullPath.includes("/view-maint-tasks")){ 
        fetchMaintTasks();
        maintKey.value += 1;
      }
      console.log("OUT MaintenanceTasks.watch.refresh");
    }
  );

  // Initialize data on mount of component
  onMounted(async () => {
    console.log('IN MaintenanceTasks.onMounted');
    itemRef.value = props.item_ref;
    itemType.value = props.item_type;
    itemName.value = props.item_name;
    fetchMaintTasks();
    maintKey.value += 1;
    console.log('OUT MaintenanceTasks.onMounted itemRef=' + itemRef.value + '; itemType=' + itemType.value);
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN MaintenanceTasks.goBack");
    router.back();
    console.log("OUT MaintenanceTasks.goBack");
  };

  // Add a note to the database
  const addMaintTask = () => {
    console.log("IN MaintenanceTasks.addMaintTask");
    router.push({name: 'add-maintenance-task', params: {item_type: itemType.value, item_ref: itemRef.value, item_name: itemName.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT MaintenanceTasks.addMaintTask");
  }

  // Delete a maintenance task from the database
  const deleteMaintTask = async (item) => {
    console.log("IN MaintenanceTasks.deleteMaintTask item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this task?',
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
          const response = await api.post('/delete-maintenance-task', requestBody, config);
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
      fetchMaintTasks();
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT MaintenanceTasks.deleteMaintTask");
  };

  // Update a maintenance task
  const updateMaintTask = (item) => {
    console.log("IN MaintenanceTasks.updateMaintTask. item=" + JSON.stringify(item));
    router.push({name: 'update-maintenance-task', params: {id: item.id, description: item.description, item_type: 'Base Unit', item_name: name.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT MaintenanceTasks.updateMaintTask");
  };

  // Retrieve maintenance tasks from the database through a REST call.
  const fetchMaintTasks = async () => {
    console.log("IN MaintenanceTasks.fetchMaintTasks");

    const config = {
        headers: {
          'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: itemType.value,
      item_ref: itemRef.value,
    };
    try {
        const response = await api.post('/get-maint-tasks', requestBody, config);
        maintTable.value = response.data;
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
    console.log("OUT MaintenanceTasks.fetchMaintTasks");
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
  .my-button {
    cursor: pointer;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-radius: 6px; /* */
    font-weight: 700;
  }
  .detail-container {
    border: 1px solid green;
    width: 70%;
  }

  .detail-sheet { 
    width: 95%;
  }

  .table-container { 
    width: 80%;
  }

  .outer-div {
    width: 80%;
    padding-top: 30px;
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
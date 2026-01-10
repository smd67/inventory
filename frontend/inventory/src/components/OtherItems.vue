<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 225px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Other Items Details
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error" style="padding-right: 250px;">
    <v-container style="border: 1px solid green" width="700">
      <v-sheet class="pa-4 text-right" width="600">
        <v-form>
          <v-text-field
            v-model="name"
            label="Name"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="location"
            label="Location"
            readonly
          ></v-text-field>
           <v-text-field
            v-model="baseUnit"
            label="Base Unit"
            readonly
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-container>
    <v-container  width="800">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Notes
      </div>
      <v-data-table
        :headers="notesHeaders"
        :items="notesTable"
        :search="notesSearch"
        item-value="date"
        class="elevation-1"
        :key="notesKey"
      >
        <!-- If you still want the default pagination controls alongside the search -->
        <template v-slot:footer.prepend>
          <v-text-field
            v-model="notesSearch"
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
          <v-btn color="primary" dark small class="ma-2" @click="addNote">
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
              <v-list-item @click="deleteNote(item)">
                <v-list-item-title>Delete</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="800">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Maintenance Tasks
      </div>
      <v-data-table
        :headers="maintHeaders"
        :items="maintTable"
        :search="maintSearch"
        item-value="status"
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
          <v-btn color="primary" dark small class="ma-2" @click="addMaintenanceTask">
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
              <v-list-item @click="deleteMaintenanceTask(item)">
                <v-list-item-title>Delete</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
  </div>
  
  <div v-else class="error-banner" style="color: red;">
    {{ error }}
  </div>
</template>

<script setup>
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import ConfirmDialog from './ConfirmDialog.vue';
  import api from "../api";

  const error = ref(null);
  const loading = ref(true);
  const id = ref(null);
  const name = ref(null);
  const baseUnit = ref(null);
  const location = ref(null);
  const router = useRouter();
  const route = useRoute();
  const notesTable = ref([]);
  const maintTable = ref([]);
  const notesSearch = ref('');
  const maintSearch = ref('');
  const notesKey = ref(0);
  const maintKey = ref(0);
  const confirmDialog = ref(null);
  
  const notesHeaders = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const maintHeaders = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Status', value: 'status' , sortable: true},
    {title: 'Last Done', value: 'last_done_date' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const props = defineProps({
    id: {
      type: Number,
      default: 0,
    },
    name: {
      type: String,
      default: "",
    },
    base_unit: {
      type: String,
      default: "",
    },
    location: {
      type: String,
      default: "",
    },
  });
  
  // fetch the user information when params change
  watch(
    () => route.params.id,
    async refresh => {
      console.log("IN watch.refresh. props=" + JSON.stringify(props));
      fetchNotes();
      notesKey.value += 1;
      fetchMaintTasks();
      maintKey.value += 1;
    }
  );

  onMounted(async () => {
    console.log('IN onMounted');
    id.value = props.id;
    name.value = props.name;
    location.value = props.location;
    baseUnit.value = props.base_unit;
    fetchNotes();
    notesKey.value += 1;
    fetchMaintTasks();
    maintKey.value += 1;
    console.log('OUT onMounted id=' + id.value + '; location=' + location.value + '; base_unit=' + baseUnit.value);
  });

  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  };

  const addMaintenanceTask = () => {
    console.log("IN addMaintenanceTask");
    router.push({name: 'add-maintenance-task', params: {item_type: 'OTHER', item_ref: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT addMaintenanceTask");
  }

  const deleteMaintenanceTask = async (item) => {
    console.log("IN deleteMaintenanceTask item=" + JSON.stringify(item));
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
          const response = await api.post('/delete-maintenance-task/', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          error.value = 'Error fetching data:' + e;
      }
      fetchMaintTasks();
      console.log('Maintenance Task deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteMaintenanceTask");
  };

  const addNote = () => {
    console.log("IN addNote");
    router.push({name: 'add-note', params: {item_type: 'OTHER', item_ref: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT addNote");
  }

  const deleteNote = async (item) => {
    console.log("IN deleteNote item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this note?',
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
          const response = await api.post('/delete-note/', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          error.value = 'Error fetching data:' + e;
      }
      console.log('Note deleted!');
      fetchNotes();
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteNote");
  };

  const fetchNotes = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: 'OTHER',
      item_ref: id.value,
    };
    try {
        const response = await api.post('/get-notes/', requestBody, config);
        notesTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

  const fetchMaintTasks = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: 'OTHER',
      item_ref: id.value,
    };
    try {
        const response = await api.post('/get-maint-tasks/', requestBody, config);
        maintTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
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
  .my-button {
    cursor: pointer;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-radius: 6px; /* */
    font-weight: 700;
  }
</style>